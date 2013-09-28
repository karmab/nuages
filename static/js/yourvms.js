$(document).ready(function() {
setInterval(function(){
   	
   var actionpending = $("#actionpending").html();
   if ( actionpending == 1 ) {
	return;
   }
   var actionpending = $("#actionpending");
   actionpending.html('1');
   if ( actionpending == 1 ) {
    return;
   }
   var refreshpending = $("#refreshpending").html();
   if ( refreshpending == 1 ) {
	return;
   }
   var refreshpending = $("#refreshpending");
   refreshpending.html('1');
  $.ajax({  
        type: "POST",
        url: '/nuages/yourvms/',
        success: function(data) {
            $("body").html(data);
	    $("#refreshpending").replaceWith('<div id="refreshpending" class="hidden">0</div>');
		}
	});
},5000);
$.ajaxSetup({ cache: false });
});
