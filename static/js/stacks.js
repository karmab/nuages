$( document ).ready(function() {
  baseurl = '';
  path = location.pathname.split('/');
  if ( path.length == 4 ) {
          baseurl = '/'+location.pathname.split('/')[1];
  }

 $('#numvms').change(function(){
    var parameterslabel = $('#id_parameterslabel');
 	parameterslabel.show(400);
    var stacklist = $('#id_stacklist');
 	stacklist.show(400);
 	var numvms = $('#numvms').val();
    for (var numvm = 1; numvm <= 10; numvm++) {
		var name            = $('#id_name_'+String(numvm));
		var profile         = $('#id_profile_'+String(numvm));
 		name.hide();
 		profile.hide();
    }
    for (var numvm = 1; numvm <= numvms; numvm++) {
		var name            = $('#id_name_'+String(numvm));
		var profile         = $('#id_profile_'+String(numvm));
 		name.show(400);
 		profile.show(400);
    }
  });

  var parameters      = $('#id_parameters');
  var parameterslabel = $('#id_parameterslabel');
  parameters.hide();
  parameterslabel.click(function(){
  if ( parameters.is(':visible') )  {
    parameters.hide(300);
    }
  else {
    parameters.show(300);
    }
    });

  });

 function createstack(){
  baseurl = '';
  path = location.pathname.split('/');
  if ( path.length >=4 ) {
          baseurl = '/'+location.pathname.split('/')[1];
  }
  var numvms            = $('#numvms').val();
  var parameters        = $('#id_parameters').val();
  var name              = $('#id_name').val();
  var name1             = $('#id_name_1').val();
  var name2             = $('#id_name_2').val();
  var name3             = $('#id_name_3').val();
  var name4             = $('#id_name_4').val();
  var name5             = $('#id_name_5').val();
  var name6             = $('#id_name_6').val();
  var name7             = $('#id_name_7').val();
  var name8             = $('#id_name_8').val();
  var name9             = $('#id_name_9').val();
  var name10            = $('#id_name_10').val();
  var profile1          = $('#id_profile_1').val();
  var profile2          = $('#id_profile_2').val();
  var profile3          = $('#id_profile_3').val();
  var profile4          = $('#id_profile_4').val();
  var profile5          = $('#id_profile_5').val();
  var profile6          = $('#id_profile_6').val();
  var profile7          = $('#id_profile_7').val();
  var profile8          = $('#id_profile_8').val();
  var profile9          = $('#id_profile_9').val();
  var profile10         = $('#id_profile_10').val();
  var hostgroup1        = $('#id_hostgroup_1').val();
  var hostgroup2        = $('#id_hostgroup_2').val();
  var hostgroup3        = $('#id_hostgroup_3').val();
  var hostgroup4        = $('#id_hostgroup_4').val();
  var hostgroup5        = $('#id_hostgroup_5').val();
  var hostgroup6        = $('#id_hostgroup_6').val();
  var hostgroup7        = $('#id_hostgroup_7').val();
  var hostgroup8        = $('#id_hostgroup_8').val();
  var hostgroup9        = $('#id_hostgroup_9').val();
  var hostgroup10       = $('#id_hostgroup_10').val();
  var details = { 'name': name, 'numvms' : numvms, 'name1' : name1 , 'profile1' : profile1 , 'name2' : name2 , 'profile2' : profile2 , 'name3' : name3 , 'profile3' : profile3 , 'name4' : name4 , 'profile4' : profile4 , 'name5' : name5 , 'profile5' : profile5 ,  'name6' : name6 , 'profile6' : profile6 , 'name7' : name7 , 'profile7' : profile7 , 'name8' : name8 , 'profile8' : profile8 , 'name9' : name9 , 'profile9' : profile9 , 'name10' : name10 , 'profile10' : profile10, 'hostgroup1' : hostgroup1, 'hostgroup2' : hostgroup2, 'hostgroup3' : hostgroup3, 'hostgroup4' : hostgroup4, 'hostgroup5' : hostgroup5, 'hostgroup6' : hostgroup6, 'hostgroup7' : hostgroup7, 'hostgroup8' : hostgroup8, 'hostgroup9' : hostgroup9, 'hostgroup10' : hostgroup10,  'parameters' : parameters  } ;
  if (  numvms == 0   ) {
    $("#result").hide();
    $("#result").html("<div class='alert alert-error' ><button type='button' class='close' data-dismiss='alert'>&times;</button>Numvms has to be more than 0 !</div>");
    $("#result").show(500);
    return ;
  }
  for (var numvm = 1; numvm <= numvms ; numvm++) {
		var profile         = $('#id_profile_'+String(numvm)).val();
        if (  profile == ''  ) {
         $("#result").hide();
         $("#result").html("<div class='alert alert-error' ><button type='button' class='close' data-dismiss='alert'>&times;</button>profile number"+numvm+" cant be blank !</div>");
         $("#result").show(500);
         return ;
        }
      }
  	$.ajax({  
		type: 'POST',
		url: baseurl+'/vms/stacks/',
		data: details ,
		success: function(data) {
  			$("#result").hide();
			$("#result").html(data);
			$("#result").show(500);
		},
		error: function(jqXHR, textStatus, errorThrown) {
  			alert(errorThrown);
		}
 		});
   }

 function changeprofile(num) {
  baseurl = '';
  path = location.pathname.split('/');
  if ( path.length >= 4 ) {
    baseurl = '/'+location.pathname.split('/')[1];
                      }
  var hostgroup = $('#id_hostgroup_'+num);
  hostgroup.hide();
  var profile = $('#id_profile_'+num).val();
  $.ajax({
    type: 'POST',
    url: baseurl+'/hostgroups/',
    data: { 'profile' : profile } ,
    success: function(data) {
     if ( data.length >= 1  ) {
     $('#id_hostgroup_'+num).replaceWith('<select name="hostgroup_'+num+'" id="id_hostgroup_'+num+'"><option value="" selected="selected"></option>');
     var hostgroupslist = '';
     $.each(data, function(index, value) {
        hostgroup = '<option value="' + value +'">'+value+'</option>';
        hostgroupslist = hostgroupslist+hostgroup;
        });
    $('#id_hostgroup_'+num).html(hostgroupslist);
    $('#id_hostgroup_'+num).append('</select><p>');
    $('#id_hostgroup_'+num).show(400) ;
    }
  }
  });
 }

 function kill(stack){
  baseurl = '';
  path = location.pathname.split('/');
  if ( path.length >= 4 ) {
    baseurl = '/'+location.pathname.split('/')[1];
  }
  $("#results").replaceWith('<div id="results"></div>');
  var sure = confirm(stack+" will be deleted!!!Sure?");
  if (sure) {
   $("#wheel").show();
   var actionpending = $("#actionpending");
   actionpending.html('1');
   data = { 'name': stack } ;
   $.ajax({
    type: "POST",
    url: baseurl+'/killstack/',
    data: data,
    success: function(data) {
            $("#wheel").hide();
            $("#results").hide();
            $("#results").addClass("alert alert-success");
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

 function start(stack){
  baseurl = '';
  path = location.pathname.split('/');
  if ( path.length >= 4 ) {
    baseurl = '/'+location.pathname.split('/')[1];
  }
  $("#results").replaceWith('<div id="results"></div>');
   $("#wheel").show();
   var actionpending = $("#actionpending");
   actionpending.html('1');
   data = { 'name': stack } ;
   $.ajax({
    type: "POST",
    url: baseurl+'/startstack/',
    data: data,
    success: function(data) {
            $("#wheel").hide();
            $("#results").hide();
            $("#results").addClass("alert alert-success");
            $("#results").html("<button type='button' class='close' data-dismiss='alert'>&times;</button>");
            $("#results").append(data);
            $("#results").show(200);
            actionpending.html('0');
            $("#actionpending").replaceWith('<div id="actionpending" class="hidden">0</div>');
        }
     });
  }


 function stop(stack){
  baseurl = '';
  path = location.pathname.split('/');
  if ( path.length >= 4 ) {
    baseurl = '/'+location.pathname.split('/')[1];
  }
  $("#results").replaceWith('<div id="results"></div>');
   $("#wheel").show();
   var actionpending = $("#actionpending");
   actionpending.html('1');
   data = { 'name': stack } ;
   $.ajax({
    type: "POST",
    url: baseurl+'/stopstack/',
    data: data,
    success: function(data) {
            $("#wheel").hide();
            $("#results").hide();
            $("#results").addClass("alert alert-success");
            $("#results").html("<button type='button' class='close' data-dismiss='alert'>&times;</button>");
            $("#results").append(data);
            $("#results").show(200);
            actionpending.html('0');
            $("#actionpending").replaceWith('<div id="actionpending" class="hidden">0</div>');
        }
     });
  }

 function show(stack){
  baseurl = '';
  path = location.pathname.split('/');
  if ( path.length >= 4 ) {
    baseurl = '/'+location.pathname.split('/')[1];
  }
   $("#results").replaceWith('<div id="results"></div>');
   $("#wheel").show();
   var actionpending = $("#actionpending");
   actionpending.html('1');
   data = { 'name': stack } ;
   $.ajax({
    type: "POST",
    url: baseurl+'/showstack/',
    data: data,
    success: function(data) {
            $("#wheel").hide();
            $("#results").hide();
            $("#results").addClass("alert alert-success");
            $("#results").html("<button type='button' class='close' data-dismiss='alert'>&times;</button>");
            $("#results").append(data);
            $("#results").show(200);
            actionpending.html('0');
            $("#actionpending").replaceWith('<div id="actionpending" class="hidden">0</div>');
        }
     });
  }
