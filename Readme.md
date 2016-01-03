Raspberry Play: Turns any HDMI supported T.V to a media player controller by web browser

- Plays video on raspberry pi
- Play videos for sites supported by youtube-dl
  https://rg3.github.io/youtube-dl/supportedsites.html
- Video player(GUI): Supports seek, play controls, playlist 
- Firefox plugin to add video urls to the reaspberry-play directly.
  https://github.com/innosam/rasp-play-addon

Optimize the status bar, while auto updating the postion without querying the server
- every second, update the position
- after 10 seconds, realign the position based on server status

Add playlist support
- Use mongdb
- Develop Backend API's for playlist
- Enhance frontend to use the API's

Add firefox plugin to send songs to raspberry with a single click
