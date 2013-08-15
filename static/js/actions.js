function start(vm,provider){
  $("#wheel2").show();
  data = { 'name': vm , 'virtualprovider': provider } ;
  $.ajax({  
	
       type: "POST",
        url: '/nuages/vms/start',
        data: data,
        success: function(data) {
            $("#results").hide();
            $("#results").addClass("alert alert-success");
            $("#results").html(data);
            $("#results").show(200);
            $("#wheel2").hide();
		}
	});
}

function stop(vm,provider){
  $("#wheel2").show();
  data = { 'name': vm , 'virtualprovider': provider } ;
  $.ajax({  
	
        type: "POST",
        url: '/nuages/vms/stop',
        data: data,
        success: function(data) {
            $("#results").hide();
            $("#results").addClass("alert alert-success");
            $("#results").html(data);
            $("#results").show(200);
            $("#wheel2").hide();
		}
	});
}

function console(){

  var virtualprovider = $('#id_virtualprovider').val();
  var data = { 'virtualprovider' : virtualprovider } ;
  $.ajax({
        type: "GET",
        url: '/nuages/vms/console',
        data: data,
        success: function(data) {
            $("#console").hide();
            $("#console").html(data);
            $("#console").show(200);
                }
        });
}

function kill(vm,provider){
var sure = confirm(vm+" will be killed.Sure?");
if (sure) {
 $("#wheel2").show();
 data = { 'name': vm , 'provider' : provider } ;
 $.ajax({  
  type: "POST",
  url: '/nuages/vms/kill',
  data: data,
  success: function(data) {
	    $("#wheel2").hide();
            $("#results").hide();
            $("#results").addClass("alert alert-success");
            $("#results").html(data);
            $("#results").show(200);
		}
	});
 }
 else {
 return;
 }
}
