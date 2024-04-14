#!/usr/bin/env python

from dataclasses import dataclass
from enum import Enum
import os
import inspect
import logging
import yaml
import tempfile
from typing import Optional
import shutil

from colorama import Fore, Style
from util.job_util import download_file
from util.check_email import check_email_address
from util.formatting import human_format

from util.enum_util import PackageManagerEnum, LanguageEnum
from util.job_util import exec_command, in_docker, in_podman
from audit.static.parse_apis_composition import parse_api_usage
from audit.static.parse_apis_composition import parse_package_composition
from audit.audit_util import get_pm_enum, get_pm_install_cmd, get_pm_proxy
from audit.static.static_util import get_static_proxy_for_language
from audit.static.static_proxy.static_base import Language2Extensions

from audit.dynamic.parse_strace import parse_trace_file
from audit.dynamic.parse_strace import count_messages_and_ip_addresses
from audit.report import generate_package_report
from audit.report import generate_summary

THREAT_MODEL = {}

import pickle
from sklearn.ensemble import RandomForestClassifier


# Five Output Functions Are Designed Here
def msg_info(x, end='\n', flush=True, indent=0):
    while indent > 0:
        x = '   ' + x
        indent -= 1
    if end != '\n':
        while len(x) < 40:
            x += '.'
        print(f'{Style.BRIGHT}[+]{Style.RESET_ALL} {x}', end=end, flush=flush)
    else:
        print(x, end=end, flush=flush)


def msg_ok(x):
    if len(x) > 50:
        x = ''.join(x[0:46]) + ' ...'
    msg_info(f'{Style.BRIGHT}{Fore.GREEN}PASS{Style.RESET_ALL} [{Fore.BLUE}{x}{Style.RESET_ALL}]')


def msg_fail(x):
    msg_info(f'{Style.BRIGHT}{Fore.YELLOW}FAIL{Style.RESET_ALL} [{x}]')


def msg_alert(x):
    msg_info(f'{Style.BRIGHT}{Fore.RED}RISK{Style.RESET_ALL} [{x}]')


def msg_warn(x):
    msg_info(f'{Style.BRIGHT}{Fore.YELLOW} N/A{Style.RESET_ALL} [{Fore.MAGENTA}{x}{Style.RESET_ALL}]')


def build_threat_model(filename):
    try:
        with open(filename) as f:
            config_data = yaml.safe_load(f)

        if 'audit' in config_data and 'alerts' in config_data['audit'] and config_data['audit']['alerts']:
            for category, category_data in config_data['audit']['alerts'].items():
                for sub_category, sub_data in category_data.items():
                    for item in sub_data:
                        if item.get('enabled', None) == True:
                            THREAT_MODEL[sub_category] = category
                            break
    except Exception as e:
        raise Exception(f'Failed to parse {filename}: {str(e)}')

    if len(THREAT_MODEL) == 0:
        raise Exception("No threat items in {filename} has been enabled")


def alert_user(alert_type, threat_model, reason, risks):
    if alert_type in threat_model:
        risk_cat = threat_model[alert_type]
        if risk_cat not in risks:
            risks[risk_cat] = []
        item = f'{alert_type}: {reason}'
        if item not in risks[risk_cat]:
            risks[risk_cat].append(item)
    return risks


def analyze_pkg_descr(pm_proxy, pkg_name, ver_str, pkg_info, risks, report):
    try:
        msg_info('Checking package description...', end='', flush=True, indent=1)
        descr = pm_proxy.get_description(pkg_name, ver_str=ver_str, pkg_info=pkg_info)
        if not descr:
            reason = 'Missing Package Description'
            alert_type = 'Missing Package Description'
            risks = alert_user(alert_type, THREAT_MODEL, reason, risks)
            msg_alert(reason)
        else:
            msg_ok(descr)
        report['description'] = descr
    except Exception as e:
        msg_fail(str(e))
    finally:
        return risks, report


def analyze_version(ver_info, risks, report):
    try:
        msg_info('Checking version...', end='', flush=True)

        assert ver_info, 'no data!'
        msg_ok(f'ver {ver_info["tag"]} ')
        # report['version'] = ver_info
    except Exception as e:
        msg_fail(str(e))
    finally:
        return risks, report


def analyze_cves(pm_name, pkg_name, ver_str, risks, report):
    try:
        msg_info('Checking for CVEs...', end='', flush=True)
        from audit.detect_CVE import get_pkgver_vulns
        vuln_list = get_pkgver_vulns(pm_name, pkg_name, ver_str)
        if vuln_list:
            alert_type = 'Contains Known Vulnerabilities'
            vulnerabilities = ','.join(vul['id'] for vul in vuln_list)
            reason = f'Contain {vulnerabilities}'
            risks = alert_user(alert_type, THREAT_MODEL, reason, risks)
            msg_alert(f'{len(vuln_list)} found')
        else:
            vuln_list = []
            msg_ok('none found')
        report['vulnerabilities'] = vuln_list
    except Exception as e:
        msg_fail(str(e))
    finally:
        return risks, report


def analyze_deps(pm_proxy, pkg_name, ver_str, pkg_info, ver_info, risks, report):
    try:
        msg_info('Checking dependencies...', end='', flush=True)
        deps = pm_proxy.get_dependencies(pkg_name, ver_str=ver_str, pkg_info=pkg_info, ver_info=ver_info)

        if 'devDependencies' in pkg_info:
            deps = deps.append(pkg_info['devDependencies'])

        report['dependencies'] = deps

        if deps and len(deps) > 10:
            alert_type = 'Having Too Many Dependencies'
            reason = f'Discover Dependencies{len(deps)}个'
            risks = alert_user(alert_type, THREAT_MODEL, reason, risks)
            msg_alert(reason)
        else:
            msg_ok(f'{len(deps)} direct' if deps else 'none found')
    except Exception as e:
        msg_fail(str(e))
    finally:
        return risks, report


def analyze_release_history(pm_proxy, pkg_name, pkg_info, risks, report, release_history=None):
    try:
        msg_info('Checking release history...', end='', flush=True, indent=1)

        # get package release history
        if not release_history:
            release_history = pm_proxy.get_release_history(pkg_name, pkg_info=pkg_info)
            assert release_history, 'no data!'

        if release_history:
            release_history['num_releases'] = len(release_history)
            report['version'] = release_history
        # import json
        # msg_info(json.dumps(release_history, indent=4))

        if len(release_history) <= 2:
            reason = f'{len(release_history)} '
            alert_type = 'Too Few Historical Versions'
            risks = alert_user(alert_type, THREAT_MODEL, reason, risks)
            msg_alert(reason)
        else:
            msg_ok(f'{len(release_history)} version(s)')
        # report['num_releases'] = len(release_history)
    except Exception as e:
        msg_fail(str(e))
    finally:
        return risks, report, release_history


def analyze_downloads(pm_proxy, pkg_name, pkg_info, risks, report):
    try:
        msg_info('Checking downloads...', end='', flush=True)
        ret = pm_proxy.get_downloads(pkg_name, pkg_info)
        # Put The Download Count Into The Report
        if ret:
            temp = str(ret) + " Weekly"
            report['download numbers'] = temp

        assert ret is not None, "N/A"
        if ret < 1000:
            reason = f'{ret} weekly'
            alert_type = 'Too Few Downloads'
            risks = alert_user(alert_type, THREAT_MODEL, reason, risks)
        msg_ok(f'{human_format(ret)} weekly')
    except Exception as e:
        msg_fail(str(e))
    finally:
        return risks, report


def analyze_author(pm_name, pm_proxy, pkg_name, ver_str, pkg_info, ver_info, risks, report):
    try:
        msg_info('Checking author...', end='', flush=True)

        # check author/maintainer email
        authors = pm_proxy.get_author(pkg_name, ver_str=ver_str, pkg_info=pkg_info, ver_info=ver_info)
        if not authors and pm_name == 'pypi':
            authors = list()
            tmp = dict()
            tmp['email'] = pkg_info['info']['author-email']
            authors.append(tmp)
        assert authors, 'no data!'
        assert isinstance(authors, list), "invalid format!"

        # format as a list of emails/names
        item_list = []
        for dev in authors:
            item = dev.get('name', None)
            if not item:
                item = dev.get('email', None)
            if not item:
                item = dev.get('handle', None)
            if item:
                item_list.append(item)
        data = ','.join(item_list)

        report['authors'] = authors
        msg_ok(data)
        # msg_ok(authors)
    except Exception as e:
        msg_fail(str(e))
        return risks, report

    try:
        msg_info('Checking email/domain validity...', end='', flush=True, indent=1)
        for author_info in authors:
            email = author_info.get('email', None)
            if not email:
                break
            try:
                valid, valid_with_dns = check_email_address(email)
            except Exception as e:
                logging.debug('Failed to parse email %s: %s' % (email, str(e)))
                valid = False
            if not valid or not valid_with_dns:
                break

        def get_alert_reason():
            if not email:
                # Rubygems allow devs to hide their emails
                if pm_proxy.name == 'rubygems':
                    return 'No Email May Be Hidden', True
                else:
                    return 'No Email', True
            if not valid:
                return 'The Author Email Address Is Illegal', True
            if not valid_with_dns:
                return 'The Author Email Domain Name Has Expired', True
            return None, True

        reason, must_alert = get_alert_reason()
        if reason:
            if must_alert:
                alert_type = 'The Author Email Does Not Exist Or Is Illegal'
                risks = alert_user(alert_type, THREAT_MODEL, reason, risks)
            msg_alert(reason)
        else:
            msg_ok(email)
    except Exception as e:
        msg_fail(str(e))
    finally:
        return risks, report


def analyze_composition(pm_name, pkg_name, ver_str, filepath, risks, report):
    try:
        msg_info('Checking files/funcs...', end='', flush=True)

        if pm_name == 'pypi':
            language = LanguageEnum.python
        elif pm_name == 'npm':
            language = LanguageEnum.javascript
        elif pm_name == 'rubygems':
            language = LanguageEnum.ruby
        else:
            raise Exception(f'Package manager {pm_name} is not supported!')
    except Exception as e:
        msg_fail(str(e))
        return risks, report

    # analyze package composition
    try:
        num_files, lang_files, num_funcs, total_loc = parse_package_composition(
            pkg_name,
            ver_str,
            filepath + '.out.json',
        )
        lang_file_ext = ','.join(Language2Extensions[language])

        content = (
            f'{num_files} files ({lang_files} {lang_file_ext}), '
            f'{num_funcs} funcs, '
            f'LoC: {human_format(total_loc)}'
        )
        msg_ok(content)
        report['composition'] = {
            '文件总数': num_files,
            '函数总数': num_funcs,
            f'{lang_file_ext}文件总数': lang_files,
            '总行数': total_loc,
        }
    except Exception as e:
        msg_fail(str(e))

    finally:
        return risks, report


class Risk(tuple, Enum):
    FILE_IO = 'accesses files and dirs', 'file'
    USER_IO = 'reads user input', None  # should this really be None?
    NET = 'communicates with external network', 'network'
    CODE = 'generates new code at runtime', 'codegen'
    PROC = 'forks or exits OS processes', 'process'
    HIDDEN = 'accesses obfuscated (hidden) code', 'decode'
    ENV_READ = 'accesses system/environment variables', 'envvars'
    ENV_WRITE = 'changes system/environment variables', 'envvars'


@dataclass
class Alert:
    risk: Risk
    desc: Optional[str] = None


ALERTS = {
    'SOURCE_FILE': Alert(Risk.FILE_IO, 'reads files and dirs'),
    'SINK_FILE': Alert(Risk.FILE_IO, 'writes to files and dirs'),
    'SINK_NETWORK': Alert(Risk.NET, 'sends data over the network'),
    'SOURCE_NETWORK': Alert(Risk.NET, 'fetches data over the network'),
    'SINK_CODE_GENERATION': Alert(Risk.CODE),
    'SINK_PROCESS_OPERATION': Alert(Risk.PROC, 'performs a process operation'),
    'SOURCE_OBFUSCATION': Alert(Risk.HIDDEN, 'reads hidden code'),
    'SOURCE_SETTINGS': Alert(Risk.ENV_READ, 'reads system settings or environment variables'),
    'SINK_UNCLASSIFIED': Alert(Risk.ENV_WRITE, 'modifies system settings or environment variables'),
    'SOURCE_ACCOUNT': Alert(Risk.ENV_WRITE, 'modifies system settings or environment variables'),
    'SOURCE_USER_INPUT': Alert(Risk.USER_IO),
}


def analyze_apis(pm_name, pkg_name, ver_str, filepath, risks, report):
    try:
        msg_info('Analyzing code...', end='', flush=True)
        cwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        config_dir = os.path.join(cwd, 'static/config')
        if pm_name == 'pypi':
            language = LanguageEnum.python
            configpath = os.path.join(config_dir, 'astgen_python_smt.config')
            system = 'python2'
        elif pm_name == 'npm':
            language = LanguageEnum.javascript
            configpath = os.path.join(config_dir, 'astgen_javascript_smt.config')
            system = 'python'
        elif pm_name == 'rubygems':
            language = LanguageEnum.ruby
            configpath = os.path.join(config_dir, 'astgen_ruby_smt.config')
            system = 'ruby'
        else:
            raise Exception(f'Package manager {pm_name} is not supported!')
    except Exception as e:
        msg_fail(str(e))
        return risks, report

    # analyze code for APIs
    try:
        static = get_static_proxy_for_language(language=language)  
        try:
            static.astgen(inpath=filepath, outfile=filepath + '.out', root=None, configpath=configpath,
                          pkg_name=pkg_name, pkg_version=ver_str, evaluate_smt=False)
        except Exception as e:
            logging.debug('Failed to parse: %s', str(e))
            raise Exception('parse error: is %s installed?' % (system))

        assert os.path.exists(filepath + '.out'), 'parse error!'

        perms = parse_api_usage(pm_name, filepath + '.out')
        if not perms:
            msg_ok('no perms found')
            return risks, report

        report_data = {}
        perms_needed = set()
        for p, usage in perms.items():
            alert = ALERTS[p]
            alert_type, needs_perm = alert.risk
            reason = alert.desc or alert_type

            risks = alert_user(alert_type, THREAT_MODEL, reason, risks)
            if needs_perm:
                perms_needed.add(needs_perm)

            # report
            if reason not in report_data:
                report_data[reason] = usage
            else:
                report_data[reason] += usage

        msg_alert(f'needs {len(perms_needed)} perm(s): {",".join(perms_needed)}')
        report['permissions'] = report_data
    except Exception as e:
        msg_fail(str(e))

    finally:
        return risks, report


def trace_installation(pm_enum, pkg_name, ver_str, report_dir, risks, report, mode):
    try:
        msg_info('Installing package and tracing code...', end='', flush=True)
        # look for strace binary
        check_strace_cmd = ['which', 'strace']
        stdout, stderr, error = exec_command("strace", check_strace_cmd, redirect_mask=3)
        if error:
            logging.debug(f'strace binary not found:\n{stdout}\n{stderr}')
            raise Exception(f'strace missing!')

        # check that we collected the correct binary path
        strace_bin = stdout
        if strace_bin == '':
            raise Exception('"strace" not installed!')
        if not os.path.exists(strace_bin):
            raise Exception(f'{strace_bin} not found!')

        # install package under strace and collect system call traces
        install_cmd = get_pm_install_cmd(pm_enum, pkg_name, ver_str, mode)
        # _, trace_filepath = tempfile.mkstemp(prefix='trace_', dir=report_dir, suffix='.log')
        trace_filepath = report_dir + f"{report['pkg_name']}/" + f"trace_{report['pkg_name']}" + ".log"
        strace_cmd = f'{strace_bin} -f -e trace=network,file,process -ttt -T -o {trace_filepath} {install_cmd}'
        stdout, stderr, error = exec_command("strace", strace_cmd.split(), redirect_mask=3)
        if error:
            logging.debug(f'strace failed with:\n{stdout}\n{stderr}')
            raise Exception(f'code {error}')

        # check if the trace file is generated
        if not os.path.exists(trace_filepath):
            raise Exception('no trace generated!')

        summary = parse_trace_file(trace_filepath, report_dir)
        assert summary, "parse error!"
        if 'files' not in summary:
            summary['files'] = []
        if 'process' not in summary:
            summary['process'] = []
        if 'network' not in summary:
            summary['network'] = []
        machine = dict()
        machine['files'] = len(summary['files'])
        machine['process'] = len(summary['process'])
        machine['network'] = len(summary['network'])

        msg_counts, ip_address_counts = count_messages_and_ip_addresses(summary)
        now = dict()
        if 'files' in msg_counts:
            now['file'] = msg_counts['files']
        if 'network' in msg_counts:
            now['network'] = msg_counts['network']
        if 'process' in msg_counts:
            now['process'] = msg_counts['system_call']

        report['summary'] = now

        # consolidate
        out = ','.join([f'{len(summary[k])} {k}' for k in summary.keys()])
        # msg_ok(f'found {out} syscalls')
        with open(r'./do/audit/random_forest_model.pkl', 'rb') as f:
            clf = pickle.load(f)

        # Using Models For Prediction
        # file，process，network
        X_test = [[machine['files'], machine['process'], machine['network']]]
        y_pred = clf.predict(X_test)

        if y_pred == 1:
            msg_alert(f'found {out} syscalls')
            report['kind'] = 'malware'
        else:
            msg_ok(f'found {out} syscalls')
            report['kind'] = 'legitimate'

    except Exception as e:
        msg_fail(str(e))
    finally:
        return risks, report


def audit(pm_args, pkg_name, ver_str, report_dir, extra_args):
    pm_enum, pm_name, pm_proxy = pm_args
    host_volume, container_mountpoint, install_trace = extra_args

    original_path = pkg_name

    msg_info('===============================================')
    msg_info(f'Auditing {pm_name} package {pkg_name} (ver: {ver_str if ver_str else "latest"})')
    msg_info('===============================================')

    try:
        msg_info(f"Fetching '{pkg_name}' from {pm_name}...", end='', flush=True)
        msg_warn('Details as follow')

        # getmetadata 
        pkg_name, pkg_info = pm_proxy.get_metadata(pkg_name=pkg_name, pkg_version=ver_str)  # The Subsequent Pkgname Is No Longer The Address
        assert pkg_info, 'package not found!'

        if pm_name == 'pypi' and original_path.find('/') >= 0:
            tmpp = dict()
            tmpp['info'] = pkg_info
            pkg_info = tmpp
        ver_info = pm_proxy.get_version(pkg_name, ver_str=ver_str, pkg_info=pkg_info)
        if not ver_info:
            if pm_name == 'pypi':
                ver_info = {
                    'tag': pkg_info['info']['version'],
                }
            else:
                ver_info = {
                    'tag': pkg_info['version'],
                }
        if not ver_str:
            ver_str = ver_info['tag']

    except Exception as e:
        msg_fail(str(e))
        return None

    risks = {}
    report = {
        'pm_name': pm_name,
        'pkg_name': pkg_name,
        'pkg_ver': ver_str,
    }
    if os.path.exists(report_dir + report['pkg_name']):
        shutil.rmtree(report_dir + report['pkg_name'])
    os.mkdir(report_dir + report['pkg_name'])
    # analyze metadata
    risks, report = analyze_pkg_descr(pm_proxy, pkg_name, ver_str, pkg_info, risks, report)
    risks, report = analyze_version(ver_info, risks, report)
    risks, report = analyze_author(pm_name, pm_proxy, pkg_name, ver_str, pkg_info, ver_info, risks, report)

    if original_path.find('/') < 0:
        risks, report, release_history = analyze_release_history(pm_proxy, pkg_name, pkg_info, risks, report)
        risks, report = analyze_downloads(pm_proxy, pkg_name, pkg_info, risks, report)
    risks, report = analyze_cves(pm_name, pkg_name, ver_str, risks, report)
    risks, report = analyze_deps(pm_proxy, pkg_name, ver_str, pkg_info, ver_info, risks, report)
    # # download package

    filepath = None
    if original_path.find('/') >= 0:
        # ttmp = original_path.rsplit('/', 1)[0]
        ttmp = original_path
        if pm_name == "npm":
            tmp = ttmp + ".tgz"
        elif pm_name == "pypi":
            tmp = ttmp + ".tar.gz"
        else:
            tmp = original_path + ".gem"

        shutil.copy(tmp, report_dir)
        filename = tmp.rsplit('/', 1)[-1]
        filepath = os.path.join(report_dir, filename)
        os.remove(tmp)
    else:
        try:
            ver_info = pm_proxy.get_version(pkg_name, ver_str=ver_str, pkg_info=pkg_info)
            assert ver_info, 'No version info!'
            if not ver_str:
                ver_str = ver_info['tag']
            msg_ok(f'ver {ver_str}')
        except Exception as e:
            msg_fail(str(e))
            return None
        try:
            msg_info(
                f"Downloading package from {pm_name}...",
                end='',
                flush=True
            )
            filepath, size = download_file(ver_info['url'], report_dir)
            msg_ok(f'{float(size) / 1024:.2f} KB')
        except KeyError:
            msg_fail('URL missing')
        except Exception as e:
            msg_fail(str(e))

    # perform static analysis
    if filepath:
        risks, report = analyze_apis(pm_name, pkg_name, ver_str, filepath, risks, report)
        risks, report = analyze_composition(pm_name, pkg_name, ver_str, filepath, risks, report)

    # perform dynamic analysis if requested
    if install_trace:
        # Online
        if original_path.find('/') < 0:
            risks, report = trace_installation(pm_enum, pkg_name, ver_str, report_dir, risks, report, "audit-online")
        # Offline
        else:
            ver_str = None
            if pm_name == 'npm':
                tmppart = original_path.split('/')
                newpart = tmppart[:-2]
                newpart.append(tmppart[-1] + '.tgz')
                newpath = '/'.join(newpart)
            elif pm_name == 'pypi':
                tmppart = original_path.split('/')
                newpart = tmppart[:-2]
                newpart.append(tmppart[-1] + '.tar.gz')
                newpath = '/'.join(newpart)
            else:
                tmppart = original_path.split('/')
                newpart = tmppart[:-2]
                newpart.append(tmppart[-1] + '.gem')
                newpath = '/'.join(newpart)
            risks, report = trace_installation(pm_enum, newpath, ver_str, report_dir, risks, report, "audit-offline")

    # aggregate risks
    if not risks:
        msg_info('No risks found!')
        report['risks'] = None
    else:
        msg_info(
            f'{sum(len(v) for v in risks.values())} risk(s) found, '
            f'package is {", ".join(risks.keys())}!'
        )
        report['risks'] = risks

    # generate final report
    args = (container_mountpoint, report_dir, host_volume)
    # html
    generate_package_report(report, args)

    return report


def __get_pm_args(pm_name):
    pm_name = pm_name.lower()
    pm_enum = get_pm_enum(pm_name)
    pm_proxy = get_pm_proxy(pm_enum, cache_dir=None, isolate_pkg_info=False)
    return pm_enum, pm_name, pm_proxy


def parse_request_args(args):
    install_trace = False
    host_volume = None
    container_mountpoint = None

    # build list of packages to audit
    audit_pkg_list = []
    for item in args.packages:
        try:
            components = item.split(':')
            assert len(components) >= 2 and len \
                (components) <= 3, f'Invalid request: {item}. Expected <pm>:<pkg>[:<ver>] (e.g., npm:react) or (e.g., npm:C:\desktop\ABC)'

            if len(components) == 2: item += ':'
            pm_name, pkg_name, ver_str = item.split(':')
            pm_enum, pm_name, pm_proxy = __get_pm_args(pm_name)

            audit_pkg_list.append(((pm_enum, pm_name, pm_proxy), pkg_name, ver_str))
        except Exception as e:
            msg_info(f'Failed to parse input "{item}" {str(e)}. Ignoring')

    # create a temp dir to host debug logs, trace logs, and final report
    try:
        report_dir = f"do/reports/"
        os.chmod(report_dir, 0o755)
    except Exception as e:
        msg_info(f'Failed to create temp dir: {str(e)}!')
        exit(1)

    # Recommend Users To Run Within The Container
    if args.trace:
        if not (in_docker() or in_podman()):
            stop = 'y'
            if stop != 'y':
                exit(0)
        install_trace = True

    return audit_pkg_list, report_dir, (host_volume, container_mountpoint, install_trace)


def main(args, config_file):
    # get user threat model
    build_threat_model(config_file)

    # parse input
    audit_pkg_list, report_dir, cmd_args = parse_request_args(args)

    # audit each package
    msg_info(f'It is {args.cmd} model now.')
    reports = []

    for pkg_info in audit_pkg_list:
        report = audit(*pkg_info, report_dir, cmd_args)
        if report:
            reports.append(report)

    # HTML Show
    msg_info('=============================================')
    generate_summary(reports, report_dir, cmd_args)
