import json
import logging
import re
import os
import inspect
import requests
import dateutil.parser
from util.job_util import exec_command
from audit.pm_metadata.pm_base import PackageManagerProxy


class RubygemsProxy(PackageManagerProxy):
    def __init__(self, registry=None, cache_dir=None, isolate_pkg_info=False):
        super(RubygemsProxy, self).__init__()
        self.registry = registry
        self.cache_dir = cache_dir
        self.isolate_pkg_info = isolate_pkg_info
        self.metadata_format = 'json'
        self.dep_format = 'json'
        self.name = "rubygems"

    def __parse_string_for_dep_info(self, line):
        try:
            name_re = re.search(r"(.*)\(", line)
            assert name_re, "No name match found"
            name = name_re.group(0).replace('(', '')

            version_re = re.search(r"\((.*?)\)", line)
            assert version_re, "No version match found"
            version = version_re.group(0).replace('(', '').replace(')', '')

            return (name, version)
        except Exception as e:
            logging.debug("Failed to parse Gem dep %s: %s" % (line, str(e)))
            return None

    def parse_deps_file(self, deps_file):
        try:
            cwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
            if not deps_file.endswith('.lock'):
                cmd = ['bundle', 'lock', '--lockfile=SSCParser-generated-Gemfile.lock']
                stdout, stderr, error = exec_command("generate lockfile", cmd, cwd=cwd, redirect_mask=3)
                if error or not stdout:
                    logging.debug(f'failed to generate lockfile for {deps_file}:\n{stdout}\n{stderr}')
                    raise Exception(f'deps parse error {error}!')
                deps_file = dst = os.path.join(cwd, 'SSCParser-generated-Gemfile.lock')

            cmd = ['ruby', 'parse_gemfile.rb', os.path.abspath(deps_file)]
            stdout, stderr, error = exec_command("parse deps", cmd, cwd=cwd, redirect_mask=3)
            if error or not stdout:
                logging.debug(f'failed to parse {deps_file}:\n{stdout}\n{stderr}')
                raise Exception(f'deps parse error {error}!')

            dep_list = []
            for line in stdout.split('\n'):
                line = line.replace(' ', '')
                if line == '' or line.startswith('#'):
                    continue
                dep = self.__parse_string_for_dep_info(line)
                if dep:
                    dep_list.append(dep)
            return dep_list
        except Exception as e:
            logging.debug("Failed to parse RubyGems deps file %s: %s" % (deps_file, str(e)))
            return None

    def get_metadata(self, pkg_name, pkg_version=None):
        url = f'https://rubygems.org/api/v1/gems/{pkg_name}.json'
        try:
            if pkg_name.find('/') < 0:
                resp = requests.request('GET', url)
                resp.raise_for_status()
                pkg_info = resp.json()
            else:
                # print(pkg_name+'/metadata')
                fmeta = open(pkg_name + '/metadata', 'r')
                name = ""
                version = ""
                authors = []
                description = ""
                # email=""
                email = []
                notall = False
                try:
                    while True:
                        line = fmeta.readline()
                        if line:
                            notall = True
                        else:
                            break
                        if line[:4] == 'name':
                            name = line[5:-1]
                        if line[:9] == '  version' and version == "":
                            version = line[10:-1]
                        if line[:7] == 'authors':
                            line = fmeta.readline()
                            while line[0] == '-':
                                authors.append(line[1:-1])
                                line = fmeta.readline()
                        if line[:11] == 'description':
                            description = line[12:-1]
                        # if line[:5]=='email':
                        # 	email=line[6:-1]
                        if line[:5] == 'email':
                            line = fmeta.readline()
                            while line[0] == '-':
                                email.append(line[1:-1])
                                line = fmeta.readline()
                finally:
                    fmeta.close()
                pkg_info = dict()
                pkg_info['name'] = name
                pkg_info['version'] = version
                pkg_info['info'] = description
                tmp = []
                if authors:
                    if email:
                        for a, b in zip(authors, email):
                            temp = dict()
                            temp['name'] = a
                            temp['email'] = b
                            tmp.append(temp)
                    else:
                        for a in authors:
                            temp = dict()
                            temp['name'] = a
                            tmp.append(temp)
                pkg_info['authors'] = tmp
            # pkg_info['authors'] = authors
            if pkg_info:
                pkg_name = pkg_info.get('name', pkg_name)
        except Exception as e:
            logging.debug("Failed to get metadata for gem '%s' (version: %s): %s!" % \
                          (pkg_name, pkg_version if pkg_version else 'latest', str(e)))
            pkg_info = None
        finally:
            return pkg_name, pkg_info

    def get_version(self, pkg_name, ver_str=None, pkg_info=None):
        if not pkg_info:
            pkg_info = self.get_metadata(pkg_name=pkg_name, pkg_version=ver_str)
        assert pkg_info and 'version' in pkg_info, "Invalid metadata!"
        if not ver_str:
            ver_str = pkg_info['version']
        ver_info = {
            'tag': ver_str,
            'url': pkg_info.get('gem_uri', None),
            'uploaded': pkg_info.get('version_created_at', None),
            'digest': pkg_info.get('sha', None),
            'yanked': pkg_info.get('yanked', None),
        }
        return ver_info

    def get_description(self, pkg_name, ver_str=None, pkg_info=None):
        if not pkg_info:
            pkg_info = self.get_metadata(pkg_name=pkg_name, pkg_version=ver_str)
        assert pkg_info and 'version' in pkg_info, "Invalid metadata!"
        return pkg_info.get('info', None)

    def get_readme(self, pkg_name, ver_str=None, pkg_info=None):
        if not pkg_info:
            pkg_info = self.get_metadata(pkg_name=pkg_name, pkg_version=ver_str)
        assert pkg_info and 'version' in pkg_info, "Invalid metadata!"
        return pkg_info.get('documentation_uri')

    def get_versions(self, pkg_name, max_num=15, min_gap_days=30, with_time=False):
        # use rubygems API to get versions
        versions_url = f'https://rubygems.org/api/v1/versions/{pkg_name}.json'
        try:
            logging.debug("fetching versions info for %s" % (pkg_name))
            versions_content = requests.request('GET', versions_url)
            versions_info = json.loads(versions_content.text)
        except:
            logging.debug("fail in get_versions for pkg %s, ignoring!", pkg_name)
            return []
            # filter versions
        version_date = [(version_info['number'], dateutil.parser.parse(version_info['created_at']))
                        for version_info in versions_info if 'created_at' in version_info]
        return self.filter_versions(version_date=version_date, max_num=max_num, min_gap_days=min_gap_days,
                                    with_time=with_time)

    def __parse_dev_list(self, dev_list: str, dev_type: str, data=None):
        if not dev_list:
            return None
        elif isinstance(dev_list, list) and len(dev_list) and isinstance(dev_list[0], dict):
            pass
        elif isinstance(dev_list, dict):
            dev_list = [dev_list]
        elif isinstance(dev_list, str):
            dev_list = [{'name': name} for name in dev_list.split(',')]
        else:
            logging.debug("Failed to parse %s: invalid format!\n%s" % (dev_type, dev_list))
            return None
        if not data:
            data = []
        for dev in dev_list:
            if not isinstance(dev, dict):
                continue
            data.append({
                'name': dev.get('name', None),
                'email': dev.get('email', None),
                'id': dev.get('id', None),
                'handle': dev.get('handle', None),
            })

        if not len(data):
            return None
        return data

        # use rubygems API to get num gems for this author

    def get_author(self, pkg_name, ver_str=None, pkg_info=None, ver_info=None):
        if not pkg_info:
            pkg_info = self.get_metadata(pkg_name=pkg_name, pkg_version=ver_str)
        assert pkg_info and 'version' in pkg_info, "Invalid metadata!"

        authors = pkg_info.get('authors', None)
        return self.__parse_dev_list(authors, 'authors')

    def get_dependencies(self, pkg_name, ver_str=None, pkg_info=None, ver_info=None):
        # Alternatively, use gem dependency, but it is regex-based and tricky to parse.
        if not pkg_info:
            pkg_info = self.get_metadata(pkg_name=pkg_name, pkg_version=ver_str)
        assert pkg_info and 'version' in pkg_info, "Invalid metadata!"

        if 'dependencies' in pkg_info and 'runtime' in pkg_info['dependencies']:
            pkg_info_deps = pkg_info['dependencies']['runtime']
            if pkg_info_deps:
                return [dep_info['name'] for dep_info in pkg_info_deps]
        return None

    def get_release_history(self, pkg_name, pkg_info=None, max_num=-1):
        from util.dates import datetime_delta, datetime_to_date_str
        versions_url = f'https://rubygems.org/api/v1/versions/{pkg_name}.json'
        try:
            logging.debug("fetching versions info for %s" % (pkg_name))
            resp = requests.request('GET', versions_url)
            resp.raise_for_status()
            ver_list = resp.json()
        except Exception as e:
            logging.debug("Failed to get versions for rubygems package %s: %s!" % (pkg_name, str(e)))
            return None

        from util.dates import date_str_to_datetime
        ordered_data = sorted(ver_list, key=lambda x: date_str_to_datetime(x['created_at']))
        assert ordered_data, "Failed to sort release_history!"

        history = {}
        last_date = None
        for ver_data in ordered_data:
            try:
                ver_str = ver_data['number']
            except Exception as e:
                logging.warning('Failed to parse version data %s for rubygems package %s: %s' % \
                                (ver_data, pkg_name, str(e)))
                continue

            downloads = ver_data.get('downloads_count', None)

            date = ver_data.get('created_at', None)
            if date:
                date = dateutil.parser.parse(date)

            days = None
            if date and last_date:
                try:
                    days = datetime_delta(date, date2=last_date, days=True)
                except:
                    pass
            last_date = date

            # XXX yanked package versions are not available using APIs
            yanked = None

            history[ver_str] = {
                "downloads"			: downloads,
                "release_date"				: datetime_to_date_str(date),
                "days_since_last_relee"	: days,
                "yanked" 					: yanked,
            }
        return history

    def get_downloads(self, pkg_name, pkg_info):
        if not pkg_info:
            pkg_info = self.get_metadata(pkg_name=pkg_name, pkg_version=ver_str)
        assert pkg_info and 'version' in pkg_info, "Invalid metadata!"
        downloads = pkg_info.get('downloads', None)
        if downloads:
            return int(downloads)
        return None

