
class SourceDataDemo:

    def __init__(self):
        
        self.title = 'title'
        
        self.counter = {'name': 'Malicious', 'value': 988}
        self.counter2 = {'name': 'Legitimate', 'value': 50136}
        
        self.echart1_data = {
            'title': 'Malware Dependency Top10(NPM)',
            'data': [
                {"name": "eslint", "value": 65},
                {"name": "typescript", "value": 33},
                {"name": "@types/node", "value": 22},
                {"name": "webpack", "value": 19},
                {"name": "eslint-config-google", "value": 17},
                {"name": "prettier", "value": 15},
                {"name": "eslint-plugin-import", "value": 14},
                {"name": "discord.js-docgen", "value": 13},
                {"name": "tslint", "value": 13},
                {"name": "tslint-config-typings", "value": 13}
            ]
        }
        self.echart2_data = {
            'title': 'Malware Dependency Top10(RubyGems)',
            'data': [
                {"name": "rake", "value": 26},
                {"name": "bundler", "value": 19},
                {"name": "rspec", "value": 16},
                {"name": "minitest", "value": 6},
                {"name": "webmock", "value": 4},
                {"name": "sqlite3", "value": 4},
                {"name": "pry", "value": 4},
                {"name": "simplecov", "value": 2},
                {"name": "codeclimate-test-reporter", "value": 2},
                {"name": "builder", "value": 2}
            ]
        }
        
        self.echarts3_1_data = {
            'title': 'File',
            'data': [
                {"name": "open", "value": 356},
                {"name": "move", "value": 21},
                {"name": "ZipFile", "value": 18},
                {"name": "remove", "value": 11},
                {"name": "rename", "value": 10},
                {"name": "fdopen", "value": 6},
                {"name": "mkstemp", "value": 5},
                {"name": "cmp", "value": 3},
                {"name": "copy", "value": 2},
                {"name": "mkdtemp", "value": 2},
                {"name": "rmtree", "value": 2},
                {"name": "rmdir", "value": 2},
                {"name": "NamedTemporaryFile", "value": 1}

            ]
        }
        self.echarts3_2_data = {
            'title': 'Process',
            'data': [
                {"name": "getattr", "value": 254},
                {"name": "system", "value": 145},
                {"name": "getenv", "value": 94},
                {"name": "setattr", "value": 86},
                {"name": "eval", "value": 67},
                {"name": "__import__", "value": 59},
                {"name": "exit", "value": 49},
                {"name": "get", "value": 47},
                {"name": "popen", "value": 32},
                {"name": "exec", "value": 32},
                {"name": "b64decode", "value": 30},
                {"name": "Popen", "value": 28},
                {"name": "input", "value": 17},
                {"name": "Thread", "value": 11},
                {"name": "register", "value": 10},
                {"name": "run", "value": 10},
                {"name": "compile", "value": 9},
                {"name": "check_output", "value": 6},
                {"name": "clear", "value": 5},
                {"name": "ConnectRegistry", "value": 4},
                {"name": "b32decode", "value": 4},
                {"name": "WinDLL", "value": 2},
                {"name": "delattr", "value": 2},
                {"name": "Process", "value": 2},
                {"name": "spawn", "value": 2},
                {"name": "import_module", "value": 1},
                {"name": "check_call", "value": 1},
                {"name": "popen4", "value": 1},
                {"name": "Manager", "value": 1},
                {"name": "fork", "value": 1},
                {"name": "getpwuid", "value": 1}
            ]
        }
        self.echarts3_3_data = {
            'title': 'Network',
            'data': [
                {"name": "urlopen", "value": 143},
                {"name": "gethostname", "value": 60},
                {"name": "socket", "value": 57},
                {"name": "Request", "value": 37},
                {"name": "build_opener", "value": 36},
                {"name": "gethostbyname", "value": 9},
                {"name": "HTTPConnection", "value": 8},
                {"name": "HTTPServer", "value": 5},
                {"name": "getaddrinfo", "value": 1},
                {"name": "socketpair", "value": 1}
            ]
        }
        self.echart4_data = {
            'title': 'Malware Release Trends',
            'data': [
                {"name": "NPM", "value": [4,2,212,267,200]},
                {"name": "RubyGems", "value": [0,0,0,4,40]},
                {"name": "PyPI", "value": [4,10,120,118,1]}
            ],
            'xAxis': ['2015', '2016', '2017', '2018', '2019'],
        }
 
        self.echarts6_1_data = {
            'title': 'File',
            'data': [
                {"name": "Directory created", "value": 65278},
                {"name": "Hard link created", "value": 20572},
                {"name": "File read", "value": 15757},
                {"name": "File unlinked", "value": 8836},
                {"name": "Directory removed", "value": 2613},
                {"name": "symlink not handled", "value": 1790},
                {"name": "Alert: Executable found, permissions: 0775", "value": 1740},
                {"name": "File path changed", "value": 934},
                {"name": "chown not handled", "value": 892},
                {"name": "Alert: Executable found, permissions: 0100775", "value": 17},
                {"name": "File written", "value": 10},
                {"name": "mknodat not handled", "value": 6},
                {"name": "permissions changed to 0600", "value": 3},
                {"name": "permissions changed to 'lin64'", "value": 2},
                {"name": "permissions changed to 'lin386'", "value": 2},
                {"name": "renameat2 not handled", "value": 1}
            ]
            
        }
        self.echarts6_2_data = {
            'title': 'Process',
            'data': [
                {"name": "Program execution failed!", "value": 1021},
                {"name": "Program execution successful", "value": 280},
                {"name": "directory removed: '/home/rebekah/test'", "value": 1}
            ]
        }
        self.echarts6_3_data = {
            'title': 'Network',
            'data': [
                {"name": "Data sent", "value": 10016},
                {"name": "Connection attempted", "value": 2884},
                {"name": "Bind: {sa_family=AF_NETLINK, nl_pid=0, nl_groups=00000000}", "value": 2140},
                {"name": "shutdown not handled", "value": 637},
                {"name": "Bind: {sa_family=AF_INET, sin_port=htons(0), sin_addr=inet_addr('0.0.0.0')}", "value": 241}
            ]
        }
        

    @property
    def echart1(self):
        data = self.echart1_data
        echart = {
            'title': data.get('title'),
            
            'xAxis': [i.get("name") for i in data.get('data')],
            'series': [i.get("value") for i in data.get('data')]
        }
        
        return echart

    @property
    def echart2(self):
        data = self.echart2_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'series': [i.get("value") for i in data.get('data')]
        }
        return echart

    @property
    def echarts3_1(self):
        data = self.echarts3_1_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'data': data.get('data'),
        }
        return echart

    @property
    def echarts3_2(self):
        data = self.echarts3_2_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'data': data.get('data'),
        }
        return echart

    @property
    def echarts3_3(self):
        data = self.echarts3_3_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'data': data.get('data'),
        }
        return echart

    @property
    def echart4(self):
        data = self.echart4_data
        echart = {
            'title': data.get('title'),
            'names': [i.get("name") for i in data.get('data')],
            'xAxis': data.get('xAxis'),
            'data': data.get('data'),
        }
        return echart

    @property
    def echart5(self):
        data = self.echart5_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'series': [i.get("value") for i in data.get('data')],
            'data': data.get('data'),
        }
        return echart
    
    @property
    def echarts6_1(self):
        data = self.echarts6_1_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'data': data.get('data'),
        }
        return echart

    @property
    def echarts6_2(self):
        data = self.echarts6_2_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'data': data.get('data'),
        }
        return echart

    @property
    def echarts6_3(self):
        data = self.echarts6_3_data
        echart = {
            'title': data.get('title'),
            'xAxis': [i.get("name") for i in data.get('data')],
            'data': data.get('data'),
        }
        return echart

    @property
    def map_1(self):
        data = self.map_1_data
        echart = {
            'symbolSize': data.get('symbolSize'),
            'data': data.get('data'),
        }
        return echart


class SourceData(SourceDataDemo):

    def __init__(self):

        super().__init__()
        self.title = 'Malicious Software Package Statistics'
