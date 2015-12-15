$('#Play').click(function(){
      var video_url = $('#Video_Url_Input').val(); 
      $.get("omxplayer?video_url=" + video_url);
        });   

$('#Stop').click(function(){ 
           $.get("omxplayer?cmd=" + "q" );
        });   

$('#Volumeplus').click(function(){ 
                $.get("omxplayer?cmd=" + "plus" );
        });   

$('#Pause').click(function(){ 
         $.get("omxplayer?cmd=" + "p" );

        });   

$('#Volume-').click(function(){ 
         $.get("omxplayer?cmd=" + "-" );
        });   


