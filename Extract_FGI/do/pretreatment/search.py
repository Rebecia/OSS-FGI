import os


def search_files(model, dir_path, pm_name):

    result = []
    if model == 'audit-offline':
        file_list = os.listdir(dir_path)  
        for file_name in file_list:
            tmp = file_name.split('.')
            complete_file_name = os.path.join(dir_path, file_name)  
            if os.path.isdir(complete_file_name) and tmp[-1] != 'gem':  
                result.extend(search_files(model, complete_file_name, pm_name))  
            if os.path.isfile(complete_file_name):  
                if pm_name == 'npm' and tmp[-1] == 'tgz' or pm_name == 'pypi' and tmp[-1] == 'gz' and tmp[
                    -2] == 'tar' or pm_name == 'rubygems' and tmp[-1] == 'gem':
                    result.append(complete_file_name)  
    else:
        file = open(dir_path, 'r')
        try:
            while True:
                line = file.readline()
                line = line[0:-1]
                if line:
                    result.append(line)
                else:
                    break
        finally:
            file.close()

    return result



def searchdep_npm(pm_name, dir_path):
    """
    获取所有文件
    :param dir_path:文件夹路径
    :return: 该文件夹下的所有文件的列表
    """
    import json
    result = dict()
    file_list = os.listdir(dir_path)  
    for file_name in file_list:
        complete_file_name = os.path.join(dir_path, file_name)  
        if os.path.isdir(complete_file_name):  
            tmp = searchdep_npm(pm_name, complete_file_name)  
            for item in tmp:
                if item in result:
                    if result[item] < tmp[item]:
                        result[item] = tmp[item]
                else:
                    result[item] = tmp[item]
        if os.path.isfile(complete_file_name):  
            if file_name == 'package.json':
                with open(complete_file_name) as f:
                    now = json.load(f)
                    if 'dependencies' in now:
                        dep = now['dependencies']
                        for item in dep:
                            if item in result:
                                if result[item] < dep[item]:
                                    result[item] = dep[item]
                            else:
                                result[item] = dep[item]
                    if 'devDependencies' in now:
                        dep = now['devDependencies']
                        for item in dep:
                            if item in result:
                                if result[item] < dep[item]:
                                    result[item] = dep[item]
                            else:
                                result[item] = dep[item]
    return result


def searchdep_rb(pm_name, dir_path):

    result = dict()
    file = open(dir_path, 'r')
    now_is = False
    name = ""
    version = ""
    notall = False
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
                if line[:15] == '        version':
                    version = line[16:-1]
                    ppp = ""
                    for c in version:
                        if c.isdigit() or c == '.':
                            ppp += c
                    version = ppp
                    if name not in result:
                        result[name] = version
    finally:
        file.close()
    return result



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


if __name__ == '__main__':
    list1 = search_files(r'./12')
    print(list1)
    print(len(list1))  
