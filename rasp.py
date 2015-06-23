from flask import Flask
from flask import request
import subprocess

app = Flask(__name__)
app.debug = True

class VideoManageri(object):
  queue = []
  def enqueue_song(video_url):
     pass
  
  def 



@app.route('/')
@app.route('/omxplayer', methods=['GET','POST'])
def omxplayer():
    video_url = request.args.get('video_url', '')
    cmd='omxplayer -o local --vol -2000 "$(youtube-dl -g \'%s\')"'%video_url
    subprocess.Popen("nohup "+ cmd, shell=True)
    return "video will start playing in a few seconds"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
