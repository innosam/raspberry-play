import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import gevent
from collections import deque
from flask import Flask
from flask import request
from multiprocessing import Process, Pipe
from gevent.subprocess import Popen, PIPE
from gevent import monkey
from gevent.socket import wait_read, wait_write
from flask import render_template, send_from_directory
import json, cPickle
from player import Player
from raspberry_play import app
from raspberry_play.models import Video
monkey.patch_socket()

pipe_left, pipe_right = Pipe()
pipe_status_left, pipe_status_right = Pipe()
#app = Flask(__name__)

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

    seek_value = request.args.get('seek','')
    dict_seek = {'seek': seek_value}
    if seek_value:
        pipe_left.send(cPickle.dumps(dict_seek))
        return ""

    video_url = request.args.get('video_url', '')
    if video_url:
        add_video(request)
 
    return ""


def add_video(request):
    video_url = request.args.get('video_url', '')
    name = request.args.get('name', '')
    if not name:
      name = ""
    try:
        video = Video(
            name = name,
            video_url =  video_url
            )
        video.save()
    except:
        print "Unexpected error:", sys.exc_info()
    dict_notify = {'notify': "video_added", "id": str(video['id']) }
    pipe_left.send(cPickle.dumps(dict_notify))
    return ""


@app.route('/omxplayer/play_video', methods=['GET'])
def play_video():
    unique_id = request.args.get('unique_id', '')
    dict_notify = {'notify': "video_played", "id": unique_id }
    pipe_left.send(cPickle.dumps(dict_notify))
    return ""


@app.route('/omxplayer/delete_video', methods=['GET'])
def delete_video():
    unique_ids = request.args.get('unique_id', '')
    unique_ids = unique_ids.split(',')
    for unique_id in unique_ids:
      item = Video.objects(id = unique_id)
      item.delete()
      dict_notify = {'notify': "video_deleted", "id": unique_id }
      pipe_left.send(cPickle.dumps(dict_notify))
    return ""

@app.route('/omxplayer/clear_video', methods=['GET'])
def clear_video():
    Video.objects.delete()
    dict_notify = {'notify': "video_clear"}
    pipe_left.send(cPickle.dumps(dict_notify))
    return ""

  

@app.route('/omxplayer/get_videos', methods=['GET'])
def get_videos():
    videos = Video.objects.order_by("created_by").to_json()
    return videos

@app.route('/omxplayer/status', methods=['GET'])
def omxplayer_status():
    pipe_status_left.send("get_status")
    wait_read(pipe_status_left.fileno())
    status = pipe_status_left.recv()
    return status

@app.route('/')
def raspberry():
    return render_template('rasp.html');
 
def Server():
    proc = Process(target = Player(pipe_right, pipe_status_right).manager)
    proc.start()
    app.run(host='0.0.0.0', port=80)

