$(document).ready(function() {
setInterval(function(){
  var virtualprovider = $('#id_virtualprovider').val();
  var data = { 'virtualprovider' : virtualprovider } ; 

  $.ajax({  
        type: "POST",
        url: '/nuages/allvms/',
        data: data,
        success: function(data) {
            //$("#allvms").hide();
            $("#allvms").html(data);
            $("#allvms").show(400);
		}
	});
},3000);
$.ajaxSetup({ cache: false });
});
