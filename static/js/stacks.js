$( document ).ready(function() {
  baseurl = '';
  path = location.pathname.split('/');
  if ( path.length == 4 ) {
          baseurl = '/'+location.pathname.split('/')[1];
  }

 $('#numvms').change(function(){
	//$("#result").hide();
	//var parameters      = $('#id_parameters_'+String(numvm));
    var parameterslabel = $('#id_parameterslabel');
 	parameterslabel.show(400);
 	var numvms = $('#numvms').val();
    for (var numvm = 1; numvm <= 10; numvm++) {
		var name            = $('#id_name_'+String(numvm));
		var namelabel       = $('#id_namelabel_'+String(numvm));
		var profile         = $('#id_profile_'+String(numvm));
		var profilelabel    = $('#id_profilelabel_'+String(numvm));
		var hostgroup         = $('#id_hostgroup_'+String(numvm));
		var hostgrouplabel    = $('#id_hostgrouplabel_'+String(numvm));
 		name.hide();
 		namelabel.hide();
 		profile.hide();
 		profilelabel.hide();
 		hostgroup.hide();
 		hostgrouplabel.hide();
    }
    for (var numvm = 1; numvm <= numvms; numvm++) {
		var name            = $('#id_name_'+String(numvm));
		var namelabel       = $('#id_namelabel_'+String(numvm));
		var profile         = $('#id_profile_'+String(numvm));
		var profilelabel    = $('#id_profilelabel_'+String(numvm));
		var hostgroup         = $('#id_hostgroup_'+String(numvm));
		var hostgrouplabel    = $('#id_hostgrouplabel_'+String(numvm));
 		name.show(400);
 		namelabel.show(400);
 		profile.show(400);
 		profilelabel.show(400);
 		hostgroup.show(400);
 		hostgrouplabel.show(400);
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
  var details = { 'name': name, 'numvms' : numvms, 'name1' : name1 , 'profile1' : profile1 , 'name2' : name2 , 'profile2' : profile2 , 'name3' : name3 , 'profile3' : profile3 , 'name4' : name4 , 'profile4' : profile4 , 'name5' : name5 , 'profile5' : profile5 ,  'name6' : name6 , 'profile6' : profile6 , 'name7' : name7 , 'profile7' : profile7 , 'name8' : name8 , 'profile8' : profile8 , 'name9' : name9 , 'profile9' : profile9 , 'name10' : name10 , 'profile10' : profile10, 'parameters' : parameters  } ;
  //CHECK VALUES ARE THERE
  if ( ( name == "" ) || ( numvms == 0 )  ) {
    $("#result").hide();
    $("#result").html("<div class='alert alert-error' ><button type='button' class='close' data-dismiss='alert'>&times;</button>Stack Name cant be blank and numvms has to be more than 0 !</div>");
    $("#result").show(500);
    return ;
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
