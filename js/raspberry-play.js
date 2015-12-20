$('#Play').click(function(){
      var video_url = $('#Video_Url_Input').val(); 
      $.get("omxplayer?video_url=" + video_url);
        });   

$('#Stop').click(function(){ 
           $.get("omxplayer?cmd=" + "EXIT" );
        });   

$('#Volumeplus').click(function(){ 
                $.get("omxplayer?cmd=" + "INCREASE_VOLUME"  );
        });   

$('#Pause').click(function(){ 
         $.get("omxplayer?cmd=" + "PAUSE", function(){
                $('#Pause').prop('value', 'Play'); 
         } );       
        });   

$('#Volume-').click(function(){ 
         $.get("omxplayer?cmd=" + "DECREASE_VOLUME" );
        });   

$(document).on('touchstart.tap click','#progressDiv' , function (ev) {
    ev.stopPropagation(); ev.preventDefault();
    var $div = $(ev.target);
    var offset = $div.offset();
    var x = ev.clientX - offset.left;
    $('#progressBar').width(x);
});

var status_update = function () {
       $.get("omxplayer/status", function(data){
               var status = JSON.parse(data);
               if(status["Duration"] && status["Position"] && status["PlaybackStatus"]){
                       var x = (status["Position"]/status["Duration"])*100;
                       $("#progressBar").attr('aria-valuenow', x);
                       $("#progressBar").css('width', x + '%');
               }
       });
}

window.setInterval(status_update, 5000);

