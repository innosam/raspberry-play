$('#Play').click(function(){
      var video_url = $('#Video_Url_Input').val(); 
      $.get("omxplayer?video_url=" + video_url);
      pause_update(2000);
        });   

$('#Stop').click(function(){ 
           $.get("omxplayer?cmd=" + "EXIT" );
      pause_update(300);

       });   

$('#Volumeplus').click(function(){ 
                $.get("omxplayer?cmd=" + "INCREASE_VOLUME"  );
        });   

$('#Pause').click(function(){ 
         $.get("omxplayer?cmd=" + "PAUSE", function(){
          $.get("omxplayer/status", function(data){
               var status = JSON.parse(data);
               if(status["PlaybackStatus"]){
                      $('#Pause').html(status["PlaybackStatus"]);
               }});
         }); 
   pause_update(300);     
        });   

$('#Volume-').click(function(){ 
         $.get("omxplayer?cmd=" + "DECREASE_VOLUME" );
        });   


$('#playlist_remove').click(function(){ 
                var id = $( "#playlist option:selected" ).attr('id');
                $.get("omxplayer/delete_video?unique_id=" + id);
        });   



$(document).ready(function(){
          $.get("omxplayer/get_videos", function(data){
               var result = JSON.parse(data);
	       for (var i = 0; i < result.length; i++) { 
                 var option = document.createElement("option");
		 option.setAttribute("value", result[i]["video_url"]);
		 option.text = result[i]["video_url"]; 
                 option.setAttribute("id",result[i]["_id"]["$oid"]);
		 document.getElementById("playlist").appendChild(option);
	       }
});
});


$(document).on('touchstart.tap click','#progressDiv' , function (ev) {
    ev.stopPropagation(); ev.preventDefault();
    var $div = $(ev.target);
    var offset = $div.offset();
    var x = ev.clientX - offset.left;
    $('#progressBar').width(x);
    var width = this.offsetWidth;
    var percentage = (x*100)/width;
    $.get("omxplayer?seek=" + Math.floor(percentage));
 pause_update(1000);
    //alert(Math.floor(percentage));
});

var pause_update = function(time)
{
    status_update.count = -1;
    setTimeout(function(){ 
        status_update.count =0;
    }, time); 
}

var status_update = function () {
       if(typeof(arguments.callee.count) === "undefined" &&
          typeof(arguments.callee.duration) === "undefined")
          {
	    arguments.callee.count = 0;
            arguments.callee.duration = 0;
          }


          if(arguments.callee.count  === -1){
             return;
          } 
	  arguments.callee.count++;
          arguments.callee.count = arguments.callee.count%10;


	  if(arguments.callee.count === 1){
               
               $.get("omxplayer/status", function(data){
               var status = JSON.parse(data);
               status_update.duration = status["Duration"];
               if(status["Duration"] && status["Position"] && status["PlaybackStatus"]){
                       var x = (status["Position"]/status["Duration"])*100;
                       $("#progressBar").attr('aria-valuenow', x);
                       $("#progressBar").css('width', x + '%'); 
              }
                     });
         }else{
             if(!arguments.callee.duration){
             $('#progressBar').attr('aria-valuenow',0);
              $("#progressBar").css('width', 0 + '%'); 
               return;
	      } 
             var duration = arguments.callee.duration;
	     var x = $("#progressBar").attr('aria-valuenow');  
             var second_to_percentage =  100/(duration/1000000);
              var to_move = second_to_percentage +  parseFloat(x);              
	   $('#progressBar').attr('aria-valuenow', to_move); 
             $('#progressBar').css('width', to_move + '%');  
         }
}

window.setInterval(status_update, 1000);
