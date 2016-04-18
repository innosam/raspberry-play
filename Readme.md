#Raspberry Player 

##### Plays videos remotely on a display using a Raspberry PI 2.
##### Or, just play audio remotely on speakers.
##### All controlled by webapp. [CHECK OUT THE FRONTEND](http://innosam.github.io/raspberry-play/)

![alt tag](https://raw.githubusercontent.com/innosam/raspberry-play/master/media/rasp-frontend.PNG)


Add firefox plugin to send songs to raspberry with a single click

1. Hundreds of content providers including youtube - [supported-sites](https://rg3.github.io/youtube-dl/supportedsites.html).
2. WebApp: seek, play controls, volume control, playlist
3. Firefox plugin to add video urls to the [raspberry-play](https://github.com/innosam/rasp-play-addon) directly. 


#### Fixes/Features:
1.Optimize the status bar:
- every second, auto update the position
- after 10 seconds, realign the position based on server status

2.Add playlist support
- Use mongdb
- Develop Backend API's for playlist
- Enhance frontend to use the API's

3.Add firefox plugin to play videos remotely with a single click


#### Where this requirement is coming from? 

I am working on my laptop the entire day, and i wanted someway to remotely play videos on my television and also play music on the speakers.
Bought a raspberry pi2, wifi adapter, and installed the raspbian os. It can very easily play 1080p videos which is pretty awesome considering its size and price.
To play videos/audio i wrote a server and omxplayer python client that sits on rpi2. And finally wrote a webapp to control the server.
This works out pretty well for me and achieves my purpose.

Let me know if you have fixed similar problems in any other way.
Also, regarding the youtube/netflix player which can be controlled by the mobile app. The limitation is that the content is restricted to only netflix and youtube.
So using combination of omxplayer and youtube-dl supports lot of other content providers.

Any other way of doing this is also welcomed.
