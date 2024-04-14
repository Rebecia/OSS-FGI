import shutil

from audit import audits
from pretreatment.unzip import ungzip_file
from pretreatment.unzip import un_gz
from pretreatment.search import search_files
from pretreatment.search import searchdep_rb
from pretreatment.search import searchdep_rb_detail
import json, logging
import os
import signal
from subprocess import PIPE, Popen
from pretreatment import search
from func_timeout import func_timeout, FunctionTimedOut
import sys
import re

# Installation Instructions
def get_pm_install_cmd(pm_name, pkg_name, ver_str, quiet=True):
    if pm_name == 'pypi':
        base_cmd = 'pip3 install '
        quiet_args = '--quiet --no-warn-script-location --disable-pip-version-check '
        ver_cmd = f'=={ver_str}'
    elif pm_name == 'npm':
        base_cmd = f'npm install'
        quiet_args = ' --silent --no-progress --no-update-notifier '
        ver_cmd = f'@{ver_str}'
    elif pm_name == 'rubygems':
        base_cmd = 'gem install --user-install'
        quiet_args = ' --silent '
        ver_cmd = f' -v {ver_str}'
        local = '-l '
    else:
        raise Exception(f'Package manager {pm_name} is not supported')

    cmd = base_cmd
    if quiet:
        cmd += quiet_args
    cmd += pkg_name
    return cmd


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

filecnt = 0
allcnt = 0 
# Batch Function
def cir(list, path, pm_name, model):
    global filecnt
    global allcnt
    filecnt=filecnt+1
    if(filecnt<=allcnt):
        print("Current progress : "+str(filecnt-1)+"/ "+str(allcnt))
    metadatapath = ""
    if (list):
        try:
            for doc in list:
                dep = []
                if pm_name == 'npm' and model == 'audit-offline':
                    filepath = ungzip_file(doc, path + '/unzip')
                    # Obtain The Dependencies Required For The Software Package
                    dep = search.searchdep_npm(pm_name, filepath)
                    for item in dep:
                        # Generate Installation Dependent Instructions
                        installdep_cmd = get_pm_install_cmd(pm_name, item, dep[item])
                        print(f'now cmd : {installdep_cmd}')
                        # Installation Dependencies
                        stdout, stderr, error = exec_command("install-dep", installdep_cmd.split(), redirect_mask=3)
                        if error:
                            print("error.")
                        print('Finished!')
                elif pm_name == 'pypi' and model == 'audit-offline':
                    # pypi: No Need To Install Dependencies
                    filepath = ungzip_file(doc, path + '/unzip')
                    nowp = filepath.split('/')
                    filepath = filepath + '/' + nowp[-1]
                elif pm_name == 'rubygems' and model == 'audit-offline':
                    filepath = ungzip_file(doc, path + '/unzip')
                    metadatapath = un_gz(filepath + '/metadata.gz')
                    dep = searchdep_rb(pm_name, metadatapath)
                    print(searchdep_rb_detail(pm_name, metadatapath))
                    for item in dep:
                        installdep_cmd = get_pm_install_cmd(pm_name, item, dep[item])
                        print(f'now cmd : {installdep_cmd}')
                        stdout, stderr, error = exec_command("install-dep", installdep_cmd.split(), redirect_mask=3)
                        if error:
                            print("error.")
                        print('Finished!')

                else:  # Online Mode
                    filepath = doc
                myargv = ['main1.py', model, '-t', '-p', pm_name + ':' + filepath]
                sys.argv = myargv

                sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
                audits.main()
                sys.exit(0)
        finally:
            # Write The Dependency Names Of Rubygems Into The Json File Here
            if pm_name == 'rubygems' and model == 'audit-offline':
                file = open('./audit_tmp_file', 'r')
                tmp_path = file.readline()
                os.chmod(tmp_path, 0o777)
                file.close()
                with open(tmp_path, 'r') as fp:
                    data = json.load(fp)
                data['dependencies'] = searchdep_rb_detail(pm_name, metadatapath)
                with open(tmp_path, 'w') as fo:
                    json.dump(data, fo, indent=4, ensure_ascii=False)
                os.remove('/home/rebekah/do/audit_tmp_file')

            # Recursion
            list = list[1:]
            cir(list, path, pm_name, model)
    print("Current progress : " + str(filecnt-1) + "/ " + str(allcnt))
    return 0


def main_start():
    # Parameter Reading;Mode Selection
    model = sys.argv[1]
    pm_name = sys.argv[2]
    path = sys.argv[3]

    if model == 'audit-offline':
        if os.path.exists(path + '/unzip'):
            shutil.rmtree(path + '/unzip')
        os.makedirs(path + '/unzip')
    list = search_files(model, path, pm_name)
    global allcnt
    allcnt = len(list)
    cir(list, path, pm_name, model)
    #global filecnt
    #global allcnt
    #print("Current progress : " + str(filecnt) + "/ " + str(allcnt))
