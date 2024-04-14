#!/usr/bin/env python
import json
import os
import tempfile
from util.files_util import write_to_file, write_json_to_file

from django.template import Template, Context
html_template = """
<!DOCTYPE html>
 <html>
 <head>
 	<title>
 		SSCParser security audit report
 	</title>
 </head>
 <style type="text/css">
    body{
        margin: 0;
        background-color: rgb(248, 248, 248);
    }
    .top-back{
        margin-top: 0;
        width: 100%;
        height: 45px;
        background-color: rgb(255, 255, 255);
        box-shadow: 0 2px 10px 0 rgba(0,0,0,.1);
    }
    .top-word{
        color: rgb(5, 109, 232);
        font-size:x-large;
        font-weight: 550;
        font-style: oblique;
        margin-top: 6px;
        margin-left: 26px;
        width: fit-content;
        float: left;
    }
    .top-smallword{
        font-size:small;
        font-weight: 360;
        font-style:italic;
        margin-top: 18px;
        width: fit-content;
        float: left;
    }
    .main{
        width: 100%;
        flex-wrap: wrap;
        display: flex;
        margin: auto;
        margin-top: 15px;
        /* background-color: white; */
    }
    .allword{
        padding-top: 18px;
        width: fit-content;
    }
    .buttonbox1{
        float: right;
        height: 100%;
        text-align: center;
        background-color: rgb(255, 255, 255);
        width: 100px;
        margin-right: 2px;
        font-display: auto;
    }
    .buttonbox2{
        float: right;
        height: 100%;
        text-align: center;
        background-color: rgb(244, 244, 244);
        width: 100px;
        margin-right: 2px;
        font-display: auto;
    }
    .box {
        display: inline-block;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: #ffffff;
        margin: 20px;
        padding: 20px;
        width: 40%;
        border-radius: 40px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    }
    .boxco3{
        background-color: #0070C0;
    }
    .boxco1{
        background-color:#BDD6EE;
    }
    .boxco2{
        background-color:#9CC2E5;
    }
    .box1 {
        display: inline-block;
        align-items: center;
        justify-content: center;
        margin: 20px;
        padding: 20px;
        width: 90%;
        
    }
    input[type="text"] {
        padding: 10px;
        border: 2px solid #ccc;
        border-radius: 5px;
        font-size: 18px;
        color: #333;
        width: 300px;
        margin: 20px auto;
        display: inline-block;        
        align-items: center;
        justify-content: center;
        
    }
    .hh{
        font-weight: bold;
        font-size: 25px;
        color: #333;
        text-align: center;
        margin: 15px;
    }
    .hh2{
        font-size: 17px;
        color: #333;
        text-align: center;
        margin: 15px;
    }
    body{
        display:flex;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
    }
    .tag-icon {
        display: inline-block;
        width: 23px;
        height: 23px;
        margin-right: 10px;
        vertical-align: middle;
      }
</style>
 <body>
     <div class="top-back">
         <div class="top-word">
             SSCParser
         </div>
         <div class="top-smallword">
             &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A professional software security analysis tool.
         </div>
     </div>
     
	<div id="details">
        <div class="main">
            
                <div id="wordbox21"style="height:auto;"class="box1">
                    
                        <div style="font-size:larger;">
                            Find <a style="font-weight: 600;text-align:center;">{{ num_risky_deps }} </a >Risk Items
                            
                        </div>
                        <div style="font-size:larger;">
                        The Model Predicts is <a style="font-weight: 600;text-align:center;">{{ kind }} </a >
                         </div>
                </div>
                <div style="width:92%;margin: auto;">
                <hr style="border-top: 1px solid #ccc;">
                {% for item in data %}
                <br></br>
            <div style="height: auto;width:94%;display: table; border-spacing: 40px 20px;">
                <div id="wordbox22"style="height:auto;display:table-cell;"class="box">
                    <div class="hh">Ecosystem</div>
                    <div class="hh2">{{ item.pm_name }}</div>
                    <div class="hh">name</div>
                    <div class="hh2">{{ item.pkg_name }}</div>
                    <div class="hh">version</div>
                    <div class="hh2">{{ item.pkg_ver }}</div>
                    <div class="hh">description</div>
                    <div class="hh2">{{ item.description }}</div>
                    <div class="hh">author</div>
                    {% for nowperson in item.authors %}
                        {% for key,val in nowperson.items %}
                            <div class="hh2"> · {{ key }} : {{ val }}</div>
                        {% endfor %}
                    {% endfor %}
                 </div>
                <div id="wordbox23"style="height:auto;display:table-cell;"class="box">
                    
                    <div class="hh">File Composition</div>
                    {% for key,val in item.composition.items %}
                        <div class="hh2"> · {{ key }} : {{ val }}</div>
                    {% endfor %}
                    <div class="hh">CVE</div>
                    {% for key in item.vulnerabilities.items %}
                        <div class="hh2"> · {{ key }}</div>
                    {% endfor %}
                    
                    <div class="hh">Depdencies</div>
                    {% for key,val in item.dependencies.items %}
                        <div class="hh2"> · {{ key }} : {{ val }}</div>
                    {% endfor %}
                </div>

            </div>
            <div style="height: auto;width:94%;display: table;border-spacing: 40px 20px;">
                <div id="wordbox24"style="height:auto;display:table-cell;"class="box">
                    <div class="hh">Static APIs</div>
                    {% for key,val in item.apis.items %}
                        <div class="hh2"> · {{ key }} : {{ val }}</div>
                    {% endfor %}
                </div>
                <div id="wordbox25"style="height:auto;display:table-cell;"class="box">
                    <div class="hh">Dynamic APIs</div>
                    {% for key,val in item.trace.items %}
                        <div class="hh2"> · {{ key }} : {{ val }}</div>
                    {% endfor %}
                </div>
            </div>
            <div style="height: auto;width:94%;display: table;border-spacing: 40px 20px;">
                <div id="wordbox26"style="height:auto;width:100%;display:table-cell;"class="box">
                    <div class="hh">Risks</div>
                    {% for key,val_list in item.risks.items %}
                        {% for val in val_list %}
                            <div class="hh2"> · {{ val }}</div>
                        {% endfor %}
                    {% endfor %}
                </div>
            </div>
               
                {% endfor %}
                <div id="nothing" style="height:60px"></div>
            </div>
        </div>
    </div>
</body>
</html>
 """


def generate_summary(reports, report_dir, args, suffix='.html'):
    host_volume, container_mountpoint, _ = args
    report_title = f'SSCParser security audit report'

    data = []
    num_risky_deps = 0
    for report in reports:
        if 'pkg_name' not in report:
            report['pkg_name']='none'
        if 'pm_name' not in report:
            report['pm_name']='none'
        if 'pkg_ver' not in report:
            report['pkg_ver']='none'
        if 'authors' not in report:
            report['authors']=[]
        if 'description' not in report:
            report['description']='none'
        if 'permissions' not in report:
            report['permissions']=dict()
            # report['permissions']['none']='none'
        if 'summary' not in report:
            report['summary']=dict()
            # report['summary']['none']='none'
        if 'composition' not in report:
            report['composition']=dict()
            report['composition']['none']='none'
        if 'version' not in report:
            report['version']=dict()
            report['version']['none']='none'
        if 'risks' not in report:
            report['risks']=dict()
            report['risks']['none']='none'
        if 'vulnerabilities' not in report:
            report['vulnerabilities']=dict()
            report['vulnerabilities']['none']='none'
        if 'dependencies' not in report:
            report['dependencies']=dict()

        if report['pm_name'] == 'rubygems' and 'dependencies' in report.keys():
            nowdep=dict()
            for key,value in report['dependencies'].items():
                for now in value:
                    if 'name' in now  and 'requirements' in now:
                        nowdep[now['name']]=now['requirements']
            report['dependencies']=nowdep

        tmpdic=dict()
        if 'permissions' in report.keys():
            for key,value in report['permissions'].items():
                for now in value:
                    if (now['api_name'],key) not in tmpdic:
                        tmpdic[(now['api_name'],key)]=1
                    else:
                        tmpdic[(now['api_name'],key)]+=1
            tmplist=[]
            for key,value in tmpdic.items():
                tmplist.append((key[0],value,key[1]))
            tmplist.sort(key=lambda x:(x[1],x[2]),reverse=True)
            tmpdic=dict()
            for i in range(0,min(10,len(tmplist))):
                tmpnow=tmplist[i][2]+' : '+tmplist[i][0]
                tmpdic[tmpnow]=tmplist[i][1]
        report['apis']=tmpdic
    
        data.append({
            'pkg_name': report['pkg_name'],
            'pm_name': report['pm_name'],
            'pkg_ver': report['pkg_ver'],
            'risks': report['risks'],
            'description': report['description'],
            'version': report['version'],
            'authors': report['authors'],
            'vulnerabilities': report['vulnerabilities'],
            'permissions': report['permissions'],
            'composition': report['composition'],
            'trace': report['summary'],
            'apis': report['apis'],
            'dependencies': report['dependencies'],
        }
        )
        if report['risks']:
            num_risky_deps += len(report['risks']['undesirable'])

        kind = 'Legitimate'
        if report['kind']:
            kind = report['kind']
        t = Template(html_template)
        c = Context({"title": report_title, "data": data, "num_risky_deps": num_risky_deps,"kind":kind})
        #_, filepath = tempfile.mkstemp(prefix=f'report_', dir=report_dir, suffix=suffix)
        filepath = report_dir+f"{report['pkg_name']}/"+f"report_{report['pkg_name']}"+suffix
        write_to_file(filepath, t.render(c))
        os.chmod(filepath, 0o444)
        if container_mountpoint:
            filepath = filepath.replace(container_mountpoint, host_volume)
        print(f'=> HTML summary available at: {filepath}')

        file=open('./do/audit/audit_tmp_file.json','r')
        detail=json.load(file)
        file.close()
        file = open('./do/audit/audit_tmp_file.json', 'w')
        if report['pkg_name'] not in detail:
            detail[report['pkg_name']]=filepath
        file.write(json.dumps(detail))
        file.close()

def generate_package_report(report, args, suffix='.json'):
    container_mountpoint, report_dir, host_volume = args

    #_, filepath = tempfile.mkstemp(prefix=f'report_', dir=report_dir, suffix=suffix)
    filepath = report_dir +f"{report['pkg_name']}/"+ f"report_{report['pkg_name']}" + suffix
    write_json_to_file(filepath, report, indent=4)

    os.chmod(filepath, 0o444)
    if container_mountpoint:
        filepath = filepath.replace(container_mountpoint, host_volume)

    print(f'=> Complete report: {filepath}')
    
