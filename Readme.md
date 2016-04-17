#Raspberry Player 

##### Plays videos remotely on a display using a Raspberry PI 2.
##### Or, just play audo remotely on speakers.
##### All controlled by webapp. [CHECK OUT THE FRONTEND](http://innosam.github.io/raspberry-play/templates/rasp.html)

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
