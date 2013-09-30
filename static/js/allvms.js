$(document).ready(function() {
setInterval(function(){
  var virtualprovider = $('#id_virtualprovider').val();
  var data = { 'virtualprovider' : virtualprovider } ; 
  var actionpending = $("#actionpending").html();
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
        url: '/nuages/allvms/',
        data: data,
        success: function(data) {
            $("#allvms").html(data);
            $("#allvms").show(400);
	    $("#refreshpending").replaceWith('<div id="refreshpending" class="hidden">0</div>');
		}
	});
},5000);
$.ajaxSetup({ cache: false });
});

function getvms(){
  var virtualprovider = $('#id_virtualprovider').val();
  var data = { 'virtualprovider' : virtualprovider } ;
  var actionpending = $("#actionpending").html();
  if ( actionpending == 1 ) {
       return;
  }
  var refreshpending = $("#refreshpending").html();
  if ( refreshpending == 1 ) {
       return;
  }
  var refreshpending = $("#refreshpending");
  refreshpending.html('1');
  $("#actionwheel").show();
  $.ajax({
        type: "POST",
        url: '/nuages/allvms/',
        data: data,
        success: function(data) {
  	    $("#actionwheel").hide();
            $("#allvms").html(data);
            $("#allvms").show(400);
            $("#refreshpending").replaceWith('<div id="actionpending" class="hidden">0</div>');
                }
        });
}
