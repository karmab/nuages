function start(vm,provider){
  $("#results").replaceWith('<div id="results"></div>');
  $("#actionwheel").show();
  var actionpending = $("#actionpending");
  actionpending.html('1');
  data = { 'name': vm , 'virtualprovider': provider } ;
  $.ajax({  
	
       type: "POST",
        url: '/nuages/vms/start',
        data: data,
        success: function(data) {
            $("#actionwheel").hide();
            $("#results").hide();
            $("#results").addClass("alert alert-success");
            //$("#results").html(data);
            $("#results").html("<button type='button' class='close' data-dismiss='alert'>&times;</button>");
            $("#results").append(data);
            $("#results").show(200);
  	    $("#actionpending").replaceWith('<div id="actionpending" class="hidden">0</div>');
		}
	});
}

function stop(vm,provider){
  $("#results").replaceWith('<div id="results"></div>');
  $("#actionwheel").show();
  var actionpending = $("#actionpending");
  actionpending.html('1');
  data = { 'name': vm , 'virtualprovider': provider } ;
  $.ajax({  
	
        type: "POST",
        url: '/nuages/vms/stop',
        data: data,
        success: function(data) {
            $("#actionwheel").hide();
            $("#results").hide();
            $("#results").addClass("alert alert-success");
            //$("#results").html(data);
            $("#results").html("<button type='button' class='close' data-dismiss='alert'>&times;</button>");
            $("#results").append(data);
            $("#results").show(200);
  	    $("#actionpending").replaceWith('<div id="actionpending" class="hidden">0</div>');
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
  $("#results").replaceWith('<div id="results"></div>');
var sure = confirm(vm+" will be deleted!!!Sure?");
if (sure) {
 $("#actionwheel").show();
 var actionpending = $("#actionpending");
 actionpending.html('1');
 data = { 'name': vm , 'provider' : provider } ;
 $.ajax({  
  type: "POST",
  url: '/nuages/vms/kill',
  data: data,
  success: function(data) {
            $("#actionwheel").hide();
            $("#results").hide();
            $("#results").addClass("alert alert-success");
            //$("#results").html(data);
            $("#results").html("<button type='button' class='close' data-dismiss='alert'>&times;</button>");
            $("#results").append(data);
            $("#results").show(200);
  	    actionpending.html('0');
  	    $("#actionpending").replaceWith('<div id="actionpending" class="hidden">0</div>');
		}
	});
 }
 else {
 return;
 }
}

function dbremove(vmid,vmname){
var sure = confirm(vmname+" will be removed from db!!!Sure?");
if (sure) {
 $("#actionwheel").show();
 var actionpending = $("#actionpending");
 actionpending.html('1');
 data = { 'id': vmid , 'name' : vmname } ;
 $.ajax({  
  type: "POST",
  url: '/nuages/vms/dbremove',
  data: data,
  success: function(data) {
 	    $("#actionwheel").hide();
            $("#results").hide();
            $("#results").addClass("alert alert-success");
            //$("#results").html(data);
            $("#results").html("<button type='button' class='close' data-dismiss='alert'>&times;</button>");
            $("#results").append(data);
            $("#results").show(200);
  	    actionpending.html('0');
  	    $("#actionpending").replaceWith('<div id="actionpending" class="hidden">0</div>');
		}
	});
 }
 else {
 return;
 }
}
