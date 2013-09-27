$(document).ready(function() {
setInterval(function(){
  var pending = $("#pending").html();
 if ( pending == 0 ) {
 location.reload();
	}
},3000);
$.ajaxSetup({ cache: false });
});
