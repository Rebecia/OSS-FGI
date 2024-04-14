const http  = require('http');
const fs = require('fs')
var url = require('url')
const { spawn } = require('child_process');
console.log('Please click : http://localhost:8080')

var childProcess,childProcess2;

var word="";
http.createServer(function(req,res){
    res.writeHead(200,{"content-type":"text/html;charset=utf-8"});
    var nowurl=req.url;
    if(nowurl=="/results"){
        fs.readFile('./list_of_all.html',function(err,data){
            res.end(data);
        });
    }else if(nowurl.substring(0,3)=='/do'){
        console.log("."+nowurl);
        fs.readFile("."+nowurl,function(err,data){
            res.end(data);
        });
    }else{
        fs.readFile('./public/index.html',function(err,data){
            res.end(data);
        });
    }
    /*// abandon it because we use websocket to do it
    var arg = url.parse(req.url).query;
    if(arg){// do not use it any more
      ppp=arg.split('=')[1]
      ppp='do/main.py_'+ppp
      data=ppp.split('_')
      txt=data.join(' ')
      childProcess = spawn('python3',data);
      console.log("000000")
      spawn('python3',['getlist.py']);
      console.log("111111");
      //spawn('firefox',['list_of_all.html','&']);
      console.log("222222")
      childProcess.stdout.on('data', (data) => {
        console.log(`stdout: ${String(data)}`);
        list=String(data).split("\n");
        for(var now in list){
          //console.log(list[now])
          var snow=list[now];
          if(snow[0]=='C' && snow[1]=='u'){
            console.log(`now: ${snow}`);
            tdata=snow;
          }
        }
      });

      childProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
      });

      childProcess.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
      });
    }
    */
}).listen(8080);



var ws = require("ws"); 

var wsServer = new ws.Server({
    host: "127.0.0.1",
    port: 2333,
});
console.log('WebSocket sever is listening at port localhost:2333');

function on_server_client_comming (wsObj) {
    //console.log("request comming");
    websocket_add_listener(wsObj);
}
wsServer.on("connection", on_server_client_comming);
var tdata="none:0/0";
function websocket_add_listener(wsObj) {
    wsObj.on("message", function(data) {
        console.log("request data:"+data);
      if (data == "showMalwareStats") {
        // Handle the request to show malware stats

        // Send a response to trigger redirection
        wsObj.send("redirect");
      }
        if(data=="ask"){
          console.log(tdata);
          resDATA=tdata;
          var list=tdata.split(":")[1].split("/");
          if(list[0]==list[1]){
            tdata="none:0/0";
          }
          wsObj.send(resDATA)
        }else{
          console.log(data)
          var list=String(data).split(" ");
          if(list[0]=="data0"){
              word="do/main.py";
          }else if(list[0]=="data1"){
            word=word+" "+list[1];
          }else if(list[0]=="data2"){
            word=word+" "+list[1];
          }else if(list[0]=="data3"){
            word=word+" "+list[1];
          }else if(list[0]=="do"){
            var ppp=word.split(" ");
            childProcess = spawn('python3',ppp)
            childProcess.stdout.on('data', (data) => {
              console.log(`stdout: ${String(data)}`);
              list=String(data).split("\n");
              for(var now in list){
                //console.log(list[now])
                var snow=list[now];
                if(snow[0]=='C' && snow[1]=='u'){
                  console.log(`now: ${snow}`);
                  tdata=snow;
                }
              }
            });
            childProcess.stderr.on('data', (data) => {
              console.error(`stderr: ${data}`);
            });
            childProcess.on('close', (code) => {
              console.log(`child process exited with code ${code}`);
              childProcess2 = spawn('python3',['getlist.py']);
              childProcess2.stderr.on('data', (data) => {
                console.error(`stderr: ${data}`);
              });
              childProcess2.on('close', (code) => {
                console.log(`child process exited with code ${code}`);
                console.log("send-alldone")
                wsObj.send("alldone")
              });
            });

            //spawn('firefox',['list_of_all.html','&']);   it will open a html on the servers instead of in the front of the users
            //fs.readFile('./list_of_all.html',function(err,data){
            //  res.end(data);
            //});
          }
        }

    });

    wsObj.on("close", function() {
        console.log("request close");
    });

    wsObj.on("error", function(err) {
        console.log("request error", err);
    });
}