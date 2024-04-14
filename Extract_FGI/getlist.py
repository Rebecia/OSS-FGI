import json
import os

file=open('do/audit/audit_tmp_file.json','r')
data=json.load(file)
file.close()
fw=open('list_of_all.html','w')
fw.write('<html>')
fw.write('\n')
fw.write('<meta charset="utf-8">')
fw.write('\n')
fw.write('<head>')
fw.write('\n')
fw.write('<title>')
fw.write('\n')
fw.write('List_of_all')
fw.write('\n')
fw.write('</title>')
fw.write('\n')
fw.write('</head>')
fw.write('\n')
cssdata="""
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
    
    .box {
        display: inline-block;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: #ffffff;
        margin: 20px;
        padding: 20px;
        width: 80%;
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
    table {
        border-collapse: collapse;
        text-align: center;
        width: 100%;
        max-width: 800px;
        margin: 0 auto;
        font-family: Arial, sans-serif;
      }
      
      th, td {
        padding: 10px;
        text-align: left;
        text-align: center;
        border: 1px solid #ddd;
      }
      td{
        font-size: 17px;
      }
      th {
        background-color: #1F4E79;
        font-weight: bold;
        font-size: 25px;
        color: #ffffff;
      }
      
      a {
        color: #007bff;
        text-decoration: none;
      }
      
      a:hover {
        text-decoration: underline;
      }
    .leftbox{
        width:25%;
        margin-top:20px;
        margin-left:140px;
        margin-bottom:20px;
        font-size: larger;
        font-weight: 600;
    }
    .rightbox{
        width:44%;
        margin-top:20px;
        margin-right:100px;
        margin-bottom:20px;
    }

</style>
"""
fw.write(cssdata)
fw.write('\n')
fw.write('<body>')
fw.write('\n')
tophtml = """
<div class="top-back">
        <div class="top-word">
            SSCparser A Security Analysis Tool For Software Supply Chain
        </div>
        <div class="top-smallword">
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A professional software security analysis tool.
        </div>
    </div>
"""
fw.write(tophtml)
fw.write('\n')
fw.write('<div id="wordbox21"style="height:auto;"class="box1">'+'\n')
fw.write(f'<div style="font-size:larger;text-align: center;">We have successfully processed {str(len(data))} packages</div>')
fw.write('\n')
fw.write('<hr style="border-top: 1px solid #ccc;margin-top: 50px;"> '+'\n')
fw.write('</div>'+'\n')
fw.write('<hr style="border-top: 1px solid #ccc;">'+'\n')

tabletop="""
<div class="box">
    <table>
        <thead>
        <tr>
            <th>Package</th>
            <th>jump to</th>
        </tr>
        </thead>
        <tbody>
"""
fw.write(tabletop)
fw.write('\n')

for key in data:
    fw.write('<tr>'+'\n')
    fw.write(f'<td>{key}</td>')
    fw.write('\n')
    fw.write(f'<td><a href="javascript:window.location.href=\'http://localhost:8080/{data[key]}\'"> details </a></td>')
    fw.write('\n'+'</tr>'+'\n')
fw.write('</tbody>'+'\n')
fw.write('</table>'+'\n')
fw.write('</div>'+'\n')
fw.write('</body>'+'\n')
fw.write('</html>')
fw.write('\n')
fw.close()