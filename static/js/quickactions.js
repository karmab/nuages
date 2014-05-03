function start(vm,provider){
  baseurl = '';
  path = location.pathname.split('/');
  if ( path.length == 4 ) {
    baseurl = '/'+location.pathname.split('/')[1];
    }
  $("#quickresults").replaceWith('<div id="quickresults"></div>');
  $("#actionwheel").show();
  data = { 'name': vm , 'virtualprovider': provider } ;
  $.ajax({  
	
       type: "POST",
        url: baseurl+'/vms/start',
        data: data,
        success: function(data) {
            $("#actionwheel").hide();
            $("#quickresults").hide();
            $("#quickresults").addClass("alert alert-success");
            $("#quickresults").html("<button type='button' class='close' data-dismiss='alert'>&times;</button>");
            $("#quickresults").append(data);
            $("#quickresults").show(200);
		}
	});
}

function stop(vm,provider){
  baseurl = '';
  path = location.pathname.split('/');
  if ( path.length == 4 ) {
    baseurl = '/'+location.pathname.split('/')[1];
    }
  $("#quickresults").replaceWith('<div id="quickresults"></div>');
  $("#actionwheel").show();
  data = { 'name': vm , 'virtualprovider': provider } ;
  $.ajax({  
	
        type: "POST",
        url: baseurl+'/vms/stop',
        data: data,
        success: function(data) {
            $("#actionwheel").hide();
            $("#quickresults").hide();
            $("#quickresults").addClass("alert alert-success");
            $("#quickresults").html("<button type='button' class='close' data-dismiss='alert'>&times;</button>");
            $("#quickresults").append(data);
            $("#quickresults").show(200);
		}
	});
}

function kill(vm,profile){
baseurl = '';
path = location.pathname.split('/');
if ( path.length == 4 ) {
    baseurl = '/'+location.pathname.split('/')[1];
}
$("#quickresults").replaceWith('<div id="quickresults"></div>');
sure = confirm(vm+" will be deleted!!!Sure?");
if (sure) {
 $("#actionwheel").show();
 data = { 'name': vm , 'profile' : profile } ;
 $.ajax({  
  type: "POST",
  url: baseurl+'/vms/kill',
  data: data,
  success: function(data) {
            $("#actionwheel").hide();
            $("#quickresults").hide();
            $("#quickresults").addClass("alert alert-success");
            $("#quickresults").html("<button type='button' class='close' data-dismiss='alert'>&times;</button>");
            $("#quickresults").append(data);
            $("#quickresults").show(200);
		}
	});
 }
 else {
 return;
 }
}

function dbremove(vmid,vmname){
baseurl = '';
path = location.pathname.split('/');
if ( path.length == 4 ) {
    baseurl = '/'+location.pathname.split('/')[1];
}
sure = confirm(vmname+" will be removed from db!!!Sure?");
if (sure) {
 $("#actionwheel").show();
 data = { 'id': vmid , 'name' : vmname } ;
 $.ajax({  
  type: "POST",
  url: baseurl+'/vms/dbremove',
  data: data,
  success: function(data) {
 	    $("#actionwheel").hide();
            $("#quickresults").hide();
            $("#quickresults").addClass("alert alert-success");
            $("#quickresults").html("<button type='button' class='close' data-dismiss='alert'>&times;</button>");
            $("#quickresults").append(data);
            $("#quickresults").show(200);
		}
	});
 }
 else {
 return;
 }
}
