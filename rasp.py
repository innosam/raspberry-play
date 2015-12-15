import gevent
from collections import deque
from flask import Flask
from flask import request
from multiprocessing import Process, Pipe
from gevent.subprocess import Popen, PIPE
from gevent import monkey
monkey.patch_socket()
from gevent.socket import wait_read, wait_write
from flask import render_template, send_from_directory

a, b = Pipe()
c, d = Pipe()

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



def cmd_thread():
    cmdQueue = deque([])
    while True:
        wait_read(d.fileno())
        cmdQueue.append(d.recv())
        if cmdQueue:
            cmd = cmdQueue.popleft()
            print "cmd_ran %s"%cmd
            global sub
            print sub
            if cmd == 'plus':
                cmd = '+'
            if sub and cmd:
                sub.stdin.write(cmd) 
                sub.stdin.flush()
                print "write succesful"
          

def videomanager():
    gevent.spawn(cmd_thread)
    vidMgrQueue = deque([])
    while True:
        wait_read(b.fileno())
	vidMgrQueue.append(b.recv())
        if vidMgrQueue:
            video_url = vidMgrQueue.popleft()
            print "Playing %s"%video_url
	    cmd=['omxplayer -o hdmi --vol -2000 "$(youtube-dl -g \'%s\')"&'%video_url]
            cmd=['youtube-dl', '-g', video_url]
            temp = Popen(cmd, stdout=PIPE)
            out, err = temp.communicate()
            print str(out.split("\n")[1])
            video_direct = out.split("\n")[1]
            cmd=['omxplayer', '-o', 'hdmi',  '--vol', '-2000', video_direct]
            print " ".join(cmd)
	    global sub
            sub = Popen(cmd, stdin=PIPE)
            sub.wait()
            print "done  running the process"



@app.route('/omxplayer', methods=['GET','POST'])
def omxplayer():
    cmd = request.args.get('cmd','')
    if cmd:
        c.send(cmd)
        return 'cmd succesfully ran'

    video_url = request.args.get('video_url', '')
    a.send(video_url)
    return "video is added to the queue"


@app.route('/')
def raspberry():
    return render_template('rasp.html');



if __name__ == '__main__':
    proc = Process(target=videomanager)
    proc.start()
    app.run(host='0.0.0.0')
