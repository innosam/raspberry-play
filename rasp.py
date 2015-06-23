from collections import deque
from flask import Flask
from flask import request
from multiprocessing import Process, Pipe
from subprocess import Popen, PIPE

a, b = Pipe()

app = Flask(__name__)

def videomanager():
    vidMgrQueue = deque([])
    while True:
	vidMgrQueue.append(b.recv())
        if vidMgrQueue:
            video_url = vidMgrQueue.popleft()
            print "Playing %s"%video_url
	    cmd='omxplayer -o local --vol -2000 "$(youtube-dl -g \'%s\')"'%video_url
            sub = Popen("nohup "+ cmd, shell=True)
            out, err = sub.communicate()


@app.route('/')
@app.route('/omxplayer', methods=['GET','POST'])
def omxplayer():
    video_url = request.args.get('video_url', '')
    a.send(video_url)
    return "video is added to the queue"

if __name__ == '__main__':
    proc = Process(target=videomanager)
    proc.start()
    app.run(host='0.0.0.0')
