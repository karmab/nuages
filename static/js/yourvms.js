$(document).ready(function() {
setInterval(function(){
   var refresh = $('#refresh');
   if ( refresh.prop('checked') == false ) {
    return;
    }
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
            //$("body").html(data);
	    $("#yourvms").html(data);
            $("#yourvms").show(400);
	    $("#yourvmsinitial").replaceWith('<p id="yourvmsinitial"><p>');

	    $("#refreshpending").replaceWith('<div id="refreshpending" class="hidden">0</div>');
		}
	});
},5000);
$.ajaxSetup({ cache: false });
});
