import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import gevent
from collections import deque
from multiprocessing import Process, Pipe
from gevent.subprocess import Popen, PIPE
from gevent import monkey
from gevent.socket import wait_read, wait_write
from gevent.queue import Queue
from omxdbus import OmxDbus
import json, cPickle
import signal, os
from models import Video
from raspberry_play.models import Video



class Player:
    def __init__(self, pipe_right, pipe_status_right):
        self.pipe_right = pipe_right
        self.pipe_status_right = pipe_status_right
        self.sub = None
        self.task = Queue()
        self.force_play_id = None

    def manager(self):
        gevent.spawn(self.status_thread)
        gevent.spawn(self.player_loop)
        print "Starting Manager"
        while True: 
            wait_read(self.pipe_right.fileno())
            print "Msg Received"
            data = self.pipe_right.recv()
            self.process_data(data)  

    def process_data(self, pickled_data):
        data = cPickle.loads(pickled_data)
  	if(data.has_key('cmd')):
           self.process_cmd(data['cmd'])

        if(data.has_key('seek')):
           self.process_seek(data['seek'])    

        if(data.has_key('notify')):
           self.process_notification(data)    

    def process_seek(self, seek_percentage):
        omxdbus = OmxDbus()
        omxdbus.seek(seek_percentage)

    def process_video(self, video_url, timestamp=None):
        print "Playing %s"%video_url
        cmd=['youtube-dl', '-g','-f best',video_url]
        temp = Popen(cmd, stdout=PIPE)
        out, err = temp.communicate()
        video_direct = out
        cmd=['omxplayer', '-o', 'hdmi',  '--vol', '-2000', video_direct[:-1]]
        print " ".join(cmd)
        self.sub = Popen(cmd, stdin=PIPE)
        omxdbus = OmxDbus()
        self.sub.communicate()
        self.sub = None
        self.task.put({'play_complete':timestamp})

    def try_get_video_name(self, video_url):
        print "Getting name for %s"%video_url
        cmd=['youtube-dl', '--get-title',video_url]
        temp = Popen(cmd, stdout=PIPE)
        out, err = temp.communicate()
        print out
        return out 

            
    def process_notification(self, data):
        print "notification received"
        notification = data['notify']
        if notification == "video_added":
           item = Video.objects(id=data['id'])[0]
           item.update(name = self.try_get_video_name(item['video_url']))
           if self.sub == None:
               self.task.put({'play': data['id']})
           return

        if notification == "video_clear":
           if self.sub != None:
               self.process_cmd("EXIT")
           return

        if notification == "video_played":
           print "video_played"
           self.task.put({'play': data['id']})


    def process_cmd(self, cmd):
        OmxDbus().send_cmd(cmd)
    
    def status_thread(self):
        statusQueue = deque([])
        while True:
            try:
                wait_read(self.pipe_status_right.fileno())
                statusQueue.append(self.pipe_status_right.recv())
            except:
                continue
            print "got status msg"
            if statusQueue:
                status = statusQueue.popleft()
                result = ""
                if(OmxDbus.is_initialized()):
                    result = json.dumps(OmxDbus().get_status())
                self.pipe_status_right.send(result)

    def player_loop(self):
       while True:
           data = self.task.get()
     	   if(data.has_key('play')):
             self.process_play(data['play'])
             continue

           if(data.has_key('play_complete')):
             self.process_play_complete(data['play_complete'])    
             continue

    def process_play(self, video_id):
        print "process play"
        item = Video.objects(id = video_id)
        if not item:
            return
        print item.to_json()
        if self.sub:
            self.force_play_id = video_id
            self.process_cmd("EXIT")
        else:
            self.play_async(item[0]['video_url'], item[0]['created_at'])
        print "process play completed"

    def play_async(self, video_url, timestamp = None):
           gevent.spawn(self.process_video, video_url, timestamp)

    def process_play_complete(self, timestamp):
       next_video = None

       if self.force_play_id:
           print "force video lined up"
           next_video = Video.objects(id = self.force_play_id)   
           self.force_play_id = None

       if not next_video:
           print "get next video based on timestamp"
           next_video = Video.objects(created_at__gt=timestamp)

       if next_video:
           self.play_async(next_video[0]['video_url'], next_video[0]['created_at'])
