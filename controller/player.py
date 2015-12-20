import gevent
from collections import deque
from multiprocessing import Process, Pipe
from gevent.subprocess import Popen, PIPE
from gevent import monkey
from gevent.socket import wait_read, wait_write
from omxdbus import OmxDbus
import json, cPickle


class Player:
     
    def __init__(self, pipe_right, pipe_status_right):
        self.pipe_right = pipe_right
        self.pipe_status_right = pipe_status_right
        gevent.spawn(self.status_thread)
        self.sub = None

    def manager(self):
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

        if(data.has_key('video_url')):
           self.process_video_url(data['video_url'])    

    def process_video_url(self, video_url):
        print "Playing %s"%video_url
        cmd=['youtube-dl', '-g','-f best',video_url]
        temp = Popen(cmd, stdout=PIPE)
        out, err = temp.communicate()
        video_direct = out
        cmd=['omxplayer', '-o', 'hdmi',  '--vol', '-2000', video_direct[:-1]]
        print " ".join(cmd)
        self.sub = Popen(cmd, stdin=PIPE)
        omxdbus = OmxDbus()
     
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
 
