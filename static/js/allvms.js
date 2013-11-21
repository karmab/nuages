$(document).ready(function() {
setInterval(function(){
  baseurl = '';
  path = location.pathname.split('/');
  if ( path.length == 4 ) {
          baseurl = '/'+location.pathname.split('/')[1];
  }
  var refresh = $('#refresh');
  if ( refresh.prop('checked') == false ) {
   return;
  }
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
        url:  baseurl+'/allvms',
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
  baseurl = '';
  path = location.pathname.split('/');
  if ( path.length == 4 ) {
          baseurl = '/'+location.pathname.split('/')[1];
  }
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
        url:  baseurl+'/allvms/',
        data: data,
        success: function(data) {
  	    $("#actionwheel").hide();
            $("#allvms").html(data);
            $("#allvms").show(400);
            $("#refreshpending").replaceWith('<div id="actionpending" class="hidden">0</div>');
                }
        });
}
