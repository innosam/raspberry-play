import gevent
from collections import deque
from flask import Flask
from flask import request
from multiprocessing import Process, Pipe
from gevent.subprocess import Popen, PIPE
from gevent import monkey
from gevent.socket import wait_read, wait_write
from flask import render_template, send_from_directory
from omxdbus import OmxDbus
import json

monkey.patch_socket()

a, b = Pipe()
c, d = Pipe()
e, f = Pipe()


dbusIfaceProp = None
dbusIfaceKey = None
done = 0

app = Flask(__name__)
sub = None

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('fonts', path)


@app.route('/omxplayer', methods=['GET','POST'])
def omxplayer():
    cmd = request.args.get('cmd','')
    if cmd:
        c.send(cmd)
        return ""

    video_url = request.args.get('video_url', '')
    a.send(video_url)
    return ""

@app.route('/omxplayer/status', methods=['GET'])
def omxplayer_status():
    e.send("get_status")
    wait_read(e.fileno())
    status = e.recv()
    return status

@app.route('/')
def raspberry():
    return render_template('rasp.html');



def videomanager():
    gevent.spawn(cmd_thread)
    gevent.spawn(status_thread)
    vidMgrQueue = deque([])
    while True:
        wait_read(b.fileno())
        vidMgrQueue.append(b.recv())
        if vidMgrQueue:
            video_url = vidMgrQueue.popleft()
            print "Playing %s"%video_url
            cmd=['youtube-dl', '-g','-f best',video_url]
            temp = Popen(cmd, stdout=PIPE)
            out, err = temp.communicate()
            video_direct = out
            cmd=['omxplayer', '-o', 'hdmi',  '--vol', '-2000', video_direct[:-1]]
            print " ".join(cmd)
            sub = Popen(cmd, stdin=PIPE)
	    omxdbus = OmxDbus()
            sub.wait()
            print "done running the process"


def cmd_thread():
    cmdQueue = deque([])
    while True:
        wait_read(d.fileno())
        cmdQueue.append(d.recv())
        if cmdQueue:
            cmd = cmdQueue.popleft()
            OmxDbus().send_cmd(cmd)

def status_thread():
    statusQueue = deque([])
    while True:
        wait_read(f.fileno())
        statusQueue.append(f.recv())
        if statusQueue:
            status = statusQueue.popleft()
            result = ""
            if(OmxDbus.is_initialized()):
                result = json.dumps(OmxDbus().get_status())
            f.send(result)
           
 
 
if __name__ == '__main__':
    proc = Process(target=videomanager)
    proc.start()
    app.run(host='0.0.0.0', port=80)


