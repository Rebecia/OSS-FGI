import gzip
import logging
import os
import json
import shutil
import stat
import tarfile
import pandas as pd
import openpyxl
from collections import Counter


endan = []
# 0-npm 1-pypi 2-ruby
flag = 1 
development_dependencies = Counter()
runtime_dependencies = Counter()
dependency_counts = []
total_dependencies = 0
category_stats = {
    "FILES": Counter(),
    "network": Counter(),
    "process": Counter(),
}
OSS_folder = ' '

def ungzip_file(gz_filename, tagpath):
    """
    :param gz_filename: The File Name To Be Decompressed
    :return:
    """
    ungz_filename = gz_filename.replace('.tgz', '').replace('.tar.gz', '').replace('.gem', '')

    tmp = ungz_filename.split('/')
    name = tmp[-1]
    ungz_filename = tagpath + '/' + name + 'zzz'

    print(ungz_filename)
    if os.path.exists(ungz_filename):
        shutil.rmtree(ungz_filename)
    try:
        f_gz = tarfile.open(gz_filename)  
        f_gz.extractall(ungz_filename)

    except Exception as e:
        print('error')
        return 0
    finally:

        print("success")
    return ungz_filename

# Unzip Gz File
def un_gz(file_name):
    """ungz zip file"""
    f_name = file_name.replace(".gz", "")
    g_file = gzip.GzipFile(file_name)
    f = open(f_name, "wb+")
    f.write(g_file.read())
    g_file.close()  
    f.close()
    return f_name

# Statistical Dynamic Api
def count_messages_and_ip_addresses(data):

    contains = ''

    for entry in data.get('network', []):
        msg = entry.get('msg')
        ip_address = entry.get('ip_address')
        print(msg)
        print(ip_address)
        if ip_address is not None:
            contains = contains + ip_address + ','
        elif msg is not None:
            contains = contains + msg + ','
        else:
            contains = contains

    for entry in data.get('files', []):
        msg = entry.get('msg')
        contains = contains + msg + ','

    for entry in data.get('process', []):
        msg = entry.get('msg')
        contains = contains + msg + ','

    return contains

# Classification Of Dependency Names Required To Obtain Ruby Packages
def searchdep_rb_detail(pm_name, dir_path):
    result = dict()
    result['development'] = list()
    result['runtime'] = list()
    file = open(dir_path, 'r')
    now_is = False
    name = ""
    version = ""
    notall = False
    typenow = ""
    tmp = dict()
    try:
        while True:
            line = file.readline()
            if line:
                notall = True
            else:
                break
            if line[0] != '-' and line[0] != ' ':
                now_is = False
            if line[:12] == 'dependencies':
                now_is = True
            if now_is == True:
                if line[:6] == '  name':
                    name = line[7:-1]
                    tmp['name'] = name
                if line[:8] == '    - - ':
                    typenow = line[9:-1]
                    ppp = typenow
                    typenow = ""
                    for c in ppp:
                        if c != '\"':
                            typenow += c
                if line[:15] == '        version':
                    version = line[16:-1]
                    ppp = ""
                    for c in version:
                        if c.isdigit() or c == '.':
                            ppp += c
                    version = ppp
                    tmp['requirements'] = typenow + version
                if line[:9] == '  type: :':
                    ppp = line[9:-1]
                    result[ppp].append(tmp)
                    tmp = dict()
    finally:
        file.close()
    return result


# npm

if flag == 0:
    for foldername in os.listdir(OSS_folder):
        folder_path = os.path.join(OSS_folder, foldername)

        # Initialize
        name_n = 'None'
        des = 'None'
        # auth_main = 'The number of author or maintainer is 0.'
        author = 0
        maintainers = 0
        url_git = 'not contain a homepage URL.'
        dep_num = 'The number of dependencies is 0.'
        # Static Api
        static_APIs = 'not get' 
        # Dynamic Api
        Dynamic_APIs = 'not get'

        # Check If The Folder Is Valid And Starts With Packj Audit
        #  and foldername.startswith('packj_audit')
        if os.path.isdir(folder_path):
            # Check If The Folder Is Empty
            if not os.listdir(folder_path):
                print(f"Folder '{foldername}' is empty. Skipping...")
                continue

            # Searching For Compressed Files
            for filename in os.listdir(folder_path):
                if filename.endswith('.tgz'):
                    try:
                        untgzfile = ungzip_file(folder_path + '/' + filename, folder_path)
                    except PermissionError:
                        print(f"File not permission: {json_file_path}")
                        break
                    if untgzfile==0:
                        break
                    untgzfile = untgzfile + '/package'
                    print(folder_path)
                    for file in os.listdir(untgzfile):
                        if file == 'package.json':
                            json_file_path = os.path.join(untgzfile, file)

                            try:
                                with open(json_file_path, 'r') as file:
                                    try:
                                        data = json.load(file)
                                    except json.JSONDecodeError:
                                        print(
                                            f"Failed to load JSON from file: {json_file_path}")
                                    except FileNotFoundError:
                                        print(f"File not found: {json_file_path}")
                                    except PermissionError:
                                        print(f"File not permission: {json_file_path}")
                                        pass
                                    if not data:
                                        print(f"File '{filename}' is empty. Skipping...")
                                        continue

                                    # Metadata

                                    if 'name' in data:
                                        name_n = data['name']

                                    if 'description' in data:
                                        des = data['description']

                                    if 'author' in data:
                                        author = data['author']
                                    else:
                                        author = 0
                                    if 'maintainers' in data:
                                        maintainers = data['maintainers']
                                    else:
                                        maintainers = 0


                                    if 'repository' in data:
                                        res = data['repository']
                                        if (isinstance(res, dict) and 'type' in res and res['type'] == 'git') or 'git' in res :
                                            url_git = 'contain a homepage URL and a Github URL.'
                                        else:
                                            url_git = 'contain a homepage URL but not a Github URL.'
                                    else:
                                        url_git = 'contain a homepage URL but not a Github URL.'
                                    
                                    development_count = 0
                                    runtime_count = 0

                                    if 'devDependencies' in data:
                                        devDependencies = data['devDependencies']
                                        for dependency in devDependencies:
                                            name = dependency
                                            if name:
                                                development_dependencies[name] = development_dependencies.get(
                                                    name, 0) + 1
                                        development_count = len(devDependencies)

                                    if 'dependencies' in data:
                                        dependencies = data['dependencies']
                                        for dependency in dependencies:
                                            name = dependency
                                            if name:
                                                runtime_dependencies[name] = runtime_dependencies.get(
                                                    name, 0) + 1
                                        runtime_count = len(dependencies)

                                    total_count = development_count + runtime_count
                                    dep_num = 'The number of dependencies is ' + f'{total_count}'+'.'
                                    
                            except PermissionError:
                                print(f"File not permission: {json_file_path}")
                                pass
                
                if filename.startswith('report') and filename.endswith('.json'):
                    json_file_path = os.path.join(folder_path, filename)
                    print(json_file_path)

                    try:
                        with open(json_file_path, 'r') as file:
                            try:
                                data = json.load(file)
                            except json.JSONDecodeError:
                                print(f"Failed to load JSON from file: {json_file_path}")
                            except FileNotFoundError:
                                print(f"File not found: {json_file_path}")
                            except PermissionError:
                                print(f"File not permission: {json_file_path}")
                                pass
                    except PermissionError:
                        print(f"File not permission: {json_file_path}")
                        pass

                    if not data:
                        print(f"File '{filename}' is empty. Skipping...")
                        continue

                    if 'pkg_name' in data:
                        name_n = data['pkg_name']
                    
                    if 'permissions' in data:
                        permissions = data.get("permissions", {})
                        temp = ''
                        for category, apis in permissions.items():
                            oneby = ''
                            for api in apis:
                                oneby = oneby + api["api_name"] + ', '
                            temp = temp + oneby
                        # print(temp)
                        static_APIs = temp
                        
                if filename.startswith('summary') and filename.endswith('.json'):
                    json_file_path = os.path.join(folder_path, filename)
                    print(json_file_path)
                    
                    try:
                        with open(json_file_path, 'r') as file:
                            try:
                                data = json.load(file)
                            except json.JSONDecodeError:
                                print(f"Failed to load JSON from file: {json_file_path}")
                            except FileNotFoundError:
                                print(f"File not found: {json_file_path}")
                            except PermissionError:
                                print(f"File not permission: {json_file_path}")
                                pass
                    except PermissionError:
                        print(f"File not permission: {json_file_path}")
                        pass

                    if not data:
                        print(f"File '{filename}' is empty. Skipping...")
                        continue
                    Dynamic_APIs = count_messages_and_ip_addresses(data)
        # endan.append([name_n, 'npm',des, author, maintainers, url_git, dep_num, static_APIs, Dynamic_APIs])
        endan.append([name_n, static_APIs])

# pypi
elif flag == 1:
    for foldername in os.listdir(OSS_folder):
        folder_path = os.path.join(OSS_folder, foldername)

        name_n = 'None'
        des = 'None'
        # auth_main = 'The number of author or maintainer is 0.'
        author = 0
        maintainers = 0
        url_git = 'not contain a homepage URL.'
        dep_num = 'The number of dependencies is 0.'
        # Static Api
        static_APIs = 'None' 
        # Dynamic Api
        Dynamic_APIs = 'None'

        # Check If The Folder Is Valid And Starts With Packj Audit  
        # and foldername.startswith('packj_audit')
        if os.path.isdir(folder_path):
            isnot1 = 0;  # 1 Indicates That It Is Not The First Time It Has Appeared

            if not os.listdir(folder_path):
                print(f"Folder '{foldername}' is empty. Skipping...")
                continue

            for filename in os.listdir(folder_path):
                if filename.endswith('.tar.gz'):
                    untgzfile = ungzip_file(folder_path + '/' + filename, folder_path)
                    # print(folder_path)
                    if untgzfile == 0:
                        break
                    for root, dirs, files in os.walk(untgzfile):
                        if isnot1 == 0:
                            for file in files:
                                if isnot1 == 0:
                                    if file == 'PKG-INFO':
                                        json_file_path = os.path.join(root, file)
                                        print(json_file_path)
                                        with open(json_file_path, 'r') as file:

                                            try:
                                                while True:
                                                    line = file.readline()
                                                    if line:
                                                        notall = True
                                                    else:
                                                        break
                                                    if line[:4] == 'Name':
                                                        name_n = line[5:-1]
                                                    if line[:7] == 'Author:':
                                                        author = line[8:-1]
                                                    if line[:11] == 'Maintainer:':
                                                        maintainers = line[12:-1]
                                                    if line[:7] == 'Summary':
                                                        des = line[8:-1]
                                                    if line[:10] == 'Home-page:':
                                                        homepage = line[11:-1]
                                                        if 'git' in homepage:
                                                            url_git = 'contain a homepage URL and a Github URL.'
                                                        else:
                                                            url_git = 'contain a homepage URL but not a Github URL.'
                              
                                                # if homepage != 0:
                                                #     for s in homepage:
                                                #         if s.isalpha():
                                                #             str_count += 1

                                                isnot1 = 1
                                                break

                                            except FileNotFoundError:
                                                print(f"File not found: {json_file_path}")
                                else:
                                    break
                        else:
                            break

                if filename.startswith('report') and filename.endswith('.json'):
                    json_file_path = os.path.join(folder_path, filename)
                    try:
                        with open(json_file_path, 'r') as file:
                            try:
                                data = json.load(file)
                            except json.JSONDecodeError:
                                print(f"Failed to load JSON from file: {json_file_path}")
                            except FileNotFoundError:
                                print(f"File not found: {json_file_path}")
                            except PermissionError:
                                print(f"File not permission: {json_file_path}")
                                pass
                    except PermissionError:
                        print(f"File not permission: {json_file_path}")
                        pass

                    if not data:
                        print(f"File '{filename}' is empty. Skipping...")
                        continue


                    if 'permissions' in data:
                        permissions = data.get("permissions", {})
                        temp = ''
                        for category, apis in permissions.items():
                            oneby = ''
                            for api in apis:
                                oneby = oneby + api["api_name"] + ', '
                            temp = temp + oneby
                        # print(temp)
                        static_APIs = temp
                        
                if filename.startswith('summary') and filename.endswith('.json'):
                    json_file_path = os.path.join(folder_path, filename)
                    
                    try:
                        with open(json_file_path, 'r') as file:
                            try:
                                data = json.load(file)
                            except json.JSONDecodeError:
                                print(f"Failed to load JSON from file: {json_file_path}")
                            except FileNotFoundError:
                                print(f"File not found: {json_file_path}")
                            except PermissionError:
                                print(f"File not permission: {json_file_path}")
                                pass
                    except PermissionError:
                        print(f"File not permission: {json_file_path}")
                        pass

                    if not data:
                        print(f"File '{filename}' is empty. Skipping...")
                        continue
                    Dynamic_APIs = count_messages_and_ip_addresses(data)
        endan.append([name_n, 'pypi',des, author, maintainers, url_git, dep_num, static_APIs, Dynamic_APIs])
        # endan.append([name_n, static_APIs, Dynamic_APIs])
        # endan.append([name_n, static_APIs])               

# ruby
else:
    for foldername in os.listdir(OSS_folder):
        folder_path = os.path.join(OSS_folder, foldername)

        name_n = 'None'
        des = 'None'
        auth_main = 'The number of author or maintainer is 0.'
        author = 0
        maintainers = 0
        url_git = 'not contain a homepage URL.'
        dep_num = 'The number of dependencies is 0.'
        static_APIs = 'None' 
        Dynamic_APIs = 'None'

        # and foldername.startswith('packj_audit')
        if os.path.isdir(folder_path) and foldername.startswith('packj_audit'):
            isnot1 = 0;  # 1 Indicates That It Is Not The First Time It Has Appeared

            if not os.listdir(folder_path):
                print(f"Folder '{foldername}' is empty. Skipping...")
                continue

            for filename in os.listdir(folder_path):
                if filename.endswith('.gem'):
                    untgzfile1 = ungzip_file(folder_path + '/' + filename, folder_path)
                    print(folder_path)
                    if untgzfile1 == 0:
                        break
                    else:
                        untgzfile = un_gz(untgzfile1 + '/metadata.gz')
                    with open(untgzfile, 'r') as file:
                        now_is = False
                        notall = False
                        try:
                            while True:
                                line = file.readline()
                                if line:
                                    notall = True
                                else:
                                    break
                                if line[:4] == 'name':
                                    name_n = line[5:-1]                                
                                if line[0] != '-' :
                                    now_is = False
                                if line[:8] == 'authors:':
                                    now_is = True
                                if now_is == True:
                                    if line[0] == '-':
                                        author = author+1
                                if line[:9] == 'homepage:':
                                    homepage = line[10:-1]
                                    if 'git' in homepage:
                                        url_git = 'contain a homepage URL and a Github URL.'
                                    else:
                                        url_git = 'contain a homepage URL but not a Github URL.'

                            auth_main = 'The number of author or maintainer is ' + f'{author}' + '.'

                            dependencies = searchdep_rb_detail(name_n,untgzfile)    
                            development = dependencies.get('development', [])
                            for dependency in development:
                                name = dependency.get('name')
                                if name:
                                    development_dependencies[name] = development_dependencies.get(
                                        name, 0) + 1

                            runtime = dependencies.get('runtime', [])
                            for dependency in runtime:
                                name = dependency.get('name')
                                if name:
                                    runtime_dependencies[name] = runtime_dependencies.get(
                                        name, 0) + 1

                            development_count = len(
                                dependencies.get('development', []))

                            runtime_count = len(dependencies.get('runtime', []))
                            total_count = development_count + runtime_count


                            print("Total count of ", filename, "is ", total_count)
                            dep_num = 'The number of dependencies is ' + f'{total_count}'+'.'

                        except FileNotFoundError:
                            print(f"File not found: {untgzfile}")
                if filename.startswith('report') and filename.endswith('.json'):
                    json_file_path = os.path.join(folder_path, filename)
                    try:
                        with open(json_file_path, 'r') as file:
                            try:
                                data = json.load(file)
                            except json.JSONDecodeError:
                                print(f"Failed to load JSON from file: {json_file_path}")
                            except FileNotFoundError:
                                print(f"File not found: {json_file_path}")
                            except PermissionError:
                                print(f"File not permission: {json_file_path}")
                                pass
                    except PermissionError:
                        print(f"File not permission: {json_file_path}")
                        pass

                    if not data:
                        print(f"File '{filename}' is empty. Skipping...")
                        continue

                    if 'description' in data:
                        des = data['description']

                    if 'permissions' in data:
                        permissions = data.get("permissions", {})
                        temp = ''
                        for category, apis in permissions.items():
                            oneby = (category + ', ' ) * len(apis)                        
                            temp = temp + oneby
                            # print(temp)
                        static_APIs = temp
                if filename.startswith('summary') and filename.endswith('.json'):
                    json_file_path = os.path.join(folder_path, filename)
                    
                    try:
                        with open(json_file_path, 'r') as file:
                            try:
                                data = json.load(file)
                            except json.JSONDecodeError:
                                print(f"Failed to load JSON from file: {json_file_path}")
                            except FileNotFoundError:
                                print(f"File not found: {json_file_path}")
                            except PermissionError:
                                print(f"File not permission: {json_file_path}")
                                pass
                    except PermissionError:
                        print(f"File not permission: {json_file_path}")
                        pass

                    if not data:
                        print(f"File '{filename}' is empty. Skipping...")
                        continue
                    Dynamic_APIs = count_messages_and_ip_addresses(data)
        endan.append([name_n, des, author, maintainers, url_git, dep_num, static_APIs, Dynamic_APIs])

excel_file_path = ''
# If The Excel File Does Not Exist Create It
if not os.path.exists(excel_file_path):
    workbook = openpyxl.Workbook()
    workbook.save(excel_file_path)
    workbook.close()
df_existing = pd.read_excel(excel_file_path)

df_new = pd.DataFrame(endan, columns=['name_n', 'OSS','des', 'author', 'maintainers', 'url_git', 'dep_num', 'static_APIs', 'Dynamic_APIs'])
# df_new = pd.DataFrame(endan, columns=['name_n','static_APIs', 'Dynamic_APIs'])
# df_new = pd.DataFrame(endan, columns=['name_n','new_static_APIs'])
df_combined = pd.concat([df_existing, df_new], ignore_index=True)
df_combined.to_excel(excel_file_path, index=False)

