#
# strace usage: strace -f -ttt -T -o strace.log <cmd>
#
import json
import logging
import os
import tempfile

from audit.dynamic.strace_parser.strace import StraceInputStream
from audit.dynamic.strace_parser.syscalls import syscall_table


def array_safe_get(array, index):
    if 0 <= index < len(array):
        return array[index]
    else:
        return ""


def parse_trace_file(input_file, tempdir):
    infile = open(input_file, "r")
    strace_stream = StraceInputStream(infile)

    summary = {}
    for entry in strace_stream:
        ts = entry.timestamp
        name = entry.syscall_name

        try:
            return_value = int(entry.return_value)
        except:

            if 'exit' in name:
                return_value = entry.return_value
            else:
                continue

        if name in ['newfstatat', 'EXIT']:
            continue

        num_args = len(entry.syscall_arguments)
        args = []

        for idx in range(num_args):
            arg = array_safe_get(entry.syscall_arguments, idx)
            args.append(arg)

        args_str = ','.join(args)

        syscall_info = syscall_table.get(name.upper(), None)
        if not syscall_info:
            continue

        parser = syscall_info.get("parser", None)
        category = syscall_info.get("category", None)
        if parser and category:
            data = parser(ts, name, args_str, args, return_value)
            if not data:
                continue
            if category not in summary:
                summary[category] = []
            summary[category].append(data)

    infile.close()
    strace_stream.close()

    try:
        _, summary_filepath = tempfile.mkstemp(prefix='summary_', dir=tempdir, suffix='.json')
        with open(summary_filepath, mode='w+') as f:
            f.write(json.dumps(summary, indent=4))
        os.chmod(summary_filepath, 0o444)
    except Exception as e:
        logging.debug(f'Failed to generate trace summary file: {str(e)}')

    return summary


def count_messages_and_ip_addresses(data):
    msg_counts = {}
    ip_address_counts = {}

    for entry in data.get('network', []):
        msg = entry.get('msg')
        ip_address = entry.get('ip_address')

        if msg:
            if 'network' not in msg_counts:
                msg_counts['network'] = {}
            if msg not in msg_counts['network']:
                msg_counts['network'][msg] = 0
            msg_counts['network'][msg] += 1

        if ip_address:
            if 'network' not in ip_address_counts:
                ip_address_counts['network'] = {}
            if ip_address not in ip_address_counts['network']:
                ip_address_counts['network'][ip_address] = 0
            ip_address_counts['network'][ip_address] += 1

    for entry in data.get('files', []):
        msg = entry.get('msg')

        if msg:
            if 'files' not in msg_counts:
                msg_counts['files'] = {}
            if msg not in msg_counts['files']:
                msg_counts['files'][msg] = 0
            msg_counts['files'][msg] += 1

    for entry in data.get('process', []):
        msg = entry.get('msg')

        if msg:
            if 'system_call' not in msg_counts:
                msg_counts['system_call'] = {}
            if msg not in msg_counts['system_call']:
                msg_counts['system_call'][msg] = 0
            msg_counts['system_call'][msg] += 1

    return msg_counts, ip_address_counts


