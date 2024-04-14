import logging
import os

import signal
from subprocess import PIPE, Popen
from func_timeout import func_timeout, FunctionTimedOut
from util.dates import curr_timestamp


def in_podman():
    return os.path.exists('/run/.containerenv')


def in_docker():
    if os.path.exists('/proc/self/mountinfo'):
        with open('/proc/self/mountinfo') as file:
            line = file.readline().strip()
            while line:
                if '/docker/containers/' in line:
                    return line.split()[3]
                line = file.readline().strip()
        return None
    else:
        return None


def exec_command(cmd, args, cwd=None, env=None, timeout=6000, redirect_mask: int = 0):
    """
	Executes shell command
	redirect_mask: stdin | stdout | stderr
	"""
    current_subprocs = set()
    shutdown = False

    stdout = None
    stderr = None
    stdin = None
    err_code = None

    def handle_signal(signum, frame):
        # send signal recieved to subprocesses
        for proc in current_subprocs:
            if proc.poll() is None:
                proc.send_signal(signum)

    try:
        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)

        if redirect_mask & 4:
            stdin = PIPE
        if redirect_mask & 2:
            stdout = PIPE
        if redirect_mask & 1:
            stderr = PIPE

        pipe = Popen(args, cwd=cwd, env=env, stdin=stdin, stdout=stdout, stderr=stderr)
        current_subprocs.add(pipe)
        try:
            # print(str(pipe.communicate))
            stdout, stderr = func_timeout(timeout, pipe.communicate)
        except FunctionTimedOut as ft:
            current_subprocs.remove(pipe)
            raise Exception(f'{cmd} timed out after {timeout} seconds!')

        err_code = pipe.returncode
        if stdout and isinstance(stdout, bytes):
            stdout = stdout.decode().strip()
        if stderr and isinstance(stderr, bytes):
            stderr = stderr.decode().strip()

    except Exception as e:
        logging.debug(f'{cmd} subprocess failed {str(e)}')
        err_code = -1

    finally:
        return stdout, stderr, err_code




def download_file(url, filepath=None, mode='wb+'):
    assert url, "NULL url"
    if not filepath:
        import tempfile
        download_dir = tempfile.mkdtemp(prefix='download-%s' % (curr_timestamp()))
        try:
            filename = url.rsplit('/', 1)[-1]
        except:
            filename = "%s" % (curr_timestamp())
        filepath = os.path.join(download_dir, filename)
    else:
        try:
            filename = url.rsplit('/', 1)[-1]
        except:
            filename = "%s" % (curr_timestamp())
        filepath = os.path.join(filepath, filename)
    try:
        # fetch and write to file
        size = 0
        with open(filepath, mode) as f:
            for content in make_request_stream(url, stream_size=8192):
                f.write(content)
                size += len(content)
        return filepath, size
    except Exception as e:
        raise Exception("Failed to download %s: %s" % (url, str(e)))


def make_request_stream(url, stream_size, headers=None, params=None):
    try:
        import requests
        with requests.get(url=url, headers=headers, params=params, stream=True) as resp:
            resp.raise_for_status()
            for chunk in resp.iter_content(stream_size):
                yield chunk
    except ImportError as e:
        print("'requests' module not available. Please install.")
        exit(1)
    except Exception as e:
        raise Exception("Failed to make request: %s" % (str(e)))

