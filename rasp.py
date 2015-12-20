import gevent
from collections import deque
from flask import Flask
from flask import request
from multiprocessing import Process, Pipe
from gevent.subprocess import Popen, PIPE
from gevent import monkey
from gevent.socket import wait_read, wait_write
from flask import render_template, send_from_directory
from app.omxdbus import OmxDbus
import json, cPickle
from app.player import Player

monkey.patch_socket()

pipe_left, pipe_right = Pipe()
pipe_status_left, pipe_status_right = Pipe()


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
    dict_cmd = {'cmd': cmd}
    if cmd:
        pipe_left.send(cPickle.dumps(dict_cmd))
        return ""

    video_url = request.args.get('video_url', '')
    dict_video_url = {'video_url': video_url}
    pipe_left.send(cPickel.dumps(dict_video_url))
    return ""


@app.route('/omxplayer/add_video', methods=['GET'])
def add_video():
    video_url = request.args.get('video_url', '')
    #Add video_url to the list
    #if no song is playing
    #start the current one
    pass

@app.route('/omxplayer/delete_video', methods=['GET'])
def delete_video():
    unique_id = request.args.get('unique_id', '')
    #remove video_url from the list
    #if no song is playing
    #stop it
    pass

@app.route('/omxplayer/get_videos', methods=['GET'])
def get_videos():
    #get_video_list_in_json
    #return the list
    pass


@app.route('/omxplayer/status', methods=['GET'])
def omxplayer_status():
    pipe_status_left.send("get_status")
    wait_read(pipe_status_left.fileno())
    status = pipe_status_left.recv()
    return status


@app.route('/')
def raspberry():
    return render_template('rasp.html');

 
if __name__ == '__main__':
    proc = Process(target = Player(pipe_right, pipe_status_right).manager)
    proc.start()
    app.run(host='0.0.0.0', port=80)

