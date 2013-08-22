$( document ).ready(function() {
 var virtualprovider = $('#id_virtualprovider');
 var virtualproviderlabel = $('label[for="id_virtualprovider"]');
 var cobblerprovider = $('#id_cobblerprovider');
 var cobblerproviderlabel = $('label[for="id_cobblerprovider"]');
 var foremanprovider = $('#id_foremanprovider');
 var foremanproviderlabel = $('label[for="id_foremanprovider"]');
 var ip1 = $('#id_ip1');
 var mac1 = $('#id_mac1');
 var mac1label = $('label[for="id_mac1"]');
 var ip2 = $('#id_ip2');
 var ip2label = $('label[for="id_ip2"]');
 var mac2 = $('#id_mac2');
 var mac2label = $('label[for="id_mac2"]');
 var ip3 = $('#id_ip3');
 var ip3label = $('label[for="id_ip3"]');
 var mac3 = $('#id_mac3');
 var mac3label = $('label[for="id_mac3"]');
 var ip4 = $('#id_ip4');
 var ip4label = $('label[for="id_ip4"]');
 var mac4 = $('#id_mac4');
 var mac4label = $('label[for="id_mac4"]');
 var extravmsfieldset = $('#id_extravmsfieldset');
 var iso = $('#id_iso');
 var isolabel = $('label[for="id_iso"]');
 var extracontent = $('#extracontent');
 var apache = $('#apache');
 var oracle = $('#oracle');
 var rac = $('#rac');
 var sap = $('#sap');
 var weblogic = $('#weblogic');
 var puppetclasseslabel = $('label[for="id_puppetclasses"]');
 var puppetclasses = $('#id_puppetclasses');
 var parameterslabel = $('label[for="id_parameters"]');
 var parameters      = $('#id_parameters');
 var ipilo = $('#id_ipilo');
 var ipilolabel = $('label[for="id_ipilo"]');
 var hostgroup = $('#id_hostgroup');
 var hostgrouplabel = $('label[for="id_hostgroup"]');
 var partitioningfieldset = $('#id_partitioningfieldset');
 var rootvg = $('#id_rootvg');
 var rootvglabel = $('label[for="id_rootvg"]');
 var rootsize = $('#id_rootsize');
 var rootsizelabel = $('label[for="id_rootsize"]');
 var varsize = $('#id_varsize');
 var varsizelabel = $('label[for="id_varsize"]');
 var homesize = $('#id_homesize');
 var homesizelabel = $('label[for="id_homesize"]');
 var tmpsize = $('#id_tmpsize');
 var tmpsizelabel = $('label[for="id_tmpsize"]');
 var swapsize = $('#id_swapsize');
 var swapsizelabel = $('label[for="id_swapsize"]');
 var storagedomain = $('#id_storagedomain');
 var storagedomainlabel = $('#id_storagedomainlabel');
 extravmsfieldset.hide();
 mac1.hide();
 mac1label.hide();
 iso.hide();
 isolabel.hide();
 apache.hide();
 oracle.hide();
 rac.hide();
 weblogic.hide();
 extracontent.hide();
 puppetclasseslabel.hide() ;
 puppetclasses.hide() ;
 parameterslabel.hide() ;
 parameters.hide() ;
 ipilo.hide();
 ipilolabel.hide();
 hostgroup.hide();
 hostgrouplabel.hide();
 partitioningfieldset.hide();
 rootvg.hide();
 rootvglabel.hide();
 rootsize.hide();
 rootsizelabel.hide();
 varsize.hide();
 varsizelabel.hide();
 tmpsize.hide();
 tmpsizelabel.hide();
 homesize.hide();
 homesizelabel.hide();
 swapsize.hide();
 swapsizelabel.hide();
 storagedomain.hide();
 storagedomainlabel.hide();
 virtualprovider.hide();
 virtualproviderlabel.hide();
 cobblerprovider.hide();
 cobblerproviderlabel.hide();
 foremanprovider.hide();
 foremanproviderlabel.hide();

 $('#numvms').change(function(){
	$("#result").hide();
	var numinterfaces ;
 	var numvms = $('#numvms').val();
  	var physical = $('#id_physical');
  	if ( ( physical.prop('checked') == true ) && ( numvms > 1 ) ) {
  	$("#result").hide();
	$("#result").html("<div class='alert alert-error'><button type='button' class='close' data-dismiss='alert'>&times;</button>Physical machines can only be created from one to one!</div>");
	$("#result").show(500);
	return;
 	}
 	var profile = $('#id_profile').val();
	if ( (profile =='' ) || ( virtualprovider == '' ) ) {
		$("#result").html("<div class='alert alert-error'><button type='button' class='close' data-dismiss='alert'>&times;</button>Set first profile!</div>");
		$("#result").show(500);
		return;
	}
  	extravmsfieldset.hide();
   for (var numvm = 2; numvm <= 10; numvm++) {
		var additionalname = $('#id_name_'+String(numvm));
		var additionalnamelabel = $('#id_namelabel_'+String(numvm));
 		additionalname.hide();
 		additionalnamelabel.hide();
   	for (var numif = 1; numif <= 3; numif++) {
		var additionalip = $('#id_ip'+String(numif)+"_"+String(numvm));
		var additionaliplabel = $('#id_iplabel'+String(numif)+"_"+String(numvm));
 		additionalip.hide();
 		additionaliplabel.hide();
		}
 		}
 if ( (profile != "" ) && ( numvms > 1 ) ) {
 $.ajax({  
   type: 'POST',
   url: '/nuages/profileinfo/',
   data: { 'profile' : profile  } ,
   success: function(data) {
   profiletype= '' ; 
   $.each(data, function(index, parameter) {
    if ( index == 0 ) {
	profiletype = parameter ;
	}
    if ( index == 6 ) {
   	numinterfaces = parameter ; 
  	extravmsfieldset.show(400);
   	for (var numvm = 2; numvm <= numvms; numvm++) {
			var additionalname = $('#id_name_'+String(numvm));
			var additionalnamelabel = $('#id_namelabel_'+String(numvm));
 			additionalname.show(400);
 			additionalnamelabel.show(400);
   		for (var numif = 1; numif <= numinterfaces; numif++) {
			var additionalip = $('#id_ip'+String(numif)+"_"+String(numvm));
			var additionaliplabel = $('#id_iplabel'+String(numif)+"_"+String(numvm));
 			additionalip.show(400);
 			additionaliplabel.show(400);
			if ( profiletype == 'ilo' ) {
				var additionalmac = $('#id_mac'+String(numif)+"_"+String(numvm));
				var additionalmaclabel = $('#id_maclabel'+String(numif)+"_"+String(numvm));
 				additionalmac.show(400);
 				additionalmaclabel.show(400);
				}
	}}
   }
   });
   }
   });
 }
  });


 $('#id_profile').change(function(){
  var result = $("#result");
  var ip1 = $('#id_ip1');
  var mac1 = $('#id_mac1');
  var mac1label = $('label[for="id_mac1"]');
  var ipilo = $('#id_ipilo');
  var ipilolabel = $('label[for="id_ipilo"]');
  var iso = $('#id_iso');
  var isolabel = $('label[for="id_iso"]');
  var profile = $('#id_profile').val();
  var physical = $('#id_physical');
  var virtualprovider = $('#id_virtualprovider');
  var virtualproviderlabel = $('label[for="id_virtualprovider"]');
  var cobblerprovider = $('#id_cobblerprovider');
  var cobblerproviderlabel = $('label[for="id_cobblerprovider"]');
  var foremanprovider = $('#id_foremanprovider');
  var foremanproviderlabel = $('label[for="id_foremanprovider"]');
  var hostgroup = $('#id_hostgroup');
  var hostgrouplabel = $('label[for="id_hostgroup"]');
  var puppetclasseslabel = $('label[for="id_puppetclasses"]');
  var puppetclasses = $('#id_puppetclasses');
  hostgroup.hide();
  hostgrouplabel.hide();
  mac1.hide(300);
  mac1label.hide(300);
  ipilo.hide(300);
  ipilolabel.hide(300);
  iso.hide(300);
  isolabel.hide(300);
  puppetclasseslabel.hide(300) ;
  puppetclasses.hide(300) ;
  parameterslabel.hide(300) ;
  parameters.hide(300) ;
  cobblerprovider.hide(300) ;
  cobblerproviderlabel.hide(300) ;
  foremanprovider.hide(300) ;
  foremanproviderlabel.hide(300) ;
  virtualprovider.hide(300) ;
  virtualproviderlabel.hide(300) ;
  ip2.hide(300);
  ip2label.hide(300);
  ip3.hide(300);
  ip3label.hide(300);
  ip4.hide(300);
  ip4label.hide(300);
  iso.hide(300);
  isolabel.hide(300);
  partitioningfieldset.hide();
  extravmsfieldset.hide();
  rootvg.hide();
  rootvglabel.hide();
  rootsize.hide();
  rootsizelabel.hide();
  varsize.hide();
  varsizelabel.hide();
  tmpsize.hide();
  tmpsizelabel.hide();
  homesize.hide();
  homesizelabel.hide();
  swapsize.hide();
  swapsizelabel.hide();
  storagedomain.hide();
  storagedomainlabel.hide();
  result.hide();
  var profile = $('#id_profile').val();
  var ipiloval = $('#id_ip1').val();
  var isoslist = '';
  var macslist = '';
  foreman = false;
  cobbler = false;
  hide    = false;
  if ( ( physical.prop('checked') == true ) && ( ipiloval == '' ) ) {
  	$("#result").hide();
	$("#result").html("<div class='alert alert-error'><button type='button' class='close' data-dismiss='alert'>&times;</button>Ip1 is required to be set to Ilo ip if physical is checked!</div>");
	$("#result").show(500);
	return;
  }
  $('#id_mac1').replaceWith('<input style="display: none;" id="id_mac1" name="mac1" maxlength="20" type="text"><p>');
  $('#id_iso').replaceWith('<select style="display: none;" name="iso" id="id_iso">');
  $('#id_partitioning').replaceWith('<div id="id_partitioning" value=""/>');
  $.ajax({  
   type: 'POST',
   url: '/nuages/profileinfo/',
   data: { 'profile' : profile , 'ipilo' : ipiloval , 'physical' : physical.prop('checked') } ,
   success: function(data) {
   profiletype = '' ;
   $.each(data, function(index, parameter) {
    if ( index == 0 )  {
	profiletype = parameter ;
	if ( profiletype == 'noilo' ) {
  		$("#result").hide();
		$("#result").html("<div class='alert alert-error'><button type='button' class='close' data-dismiss='alert'>&times;</button>Profile without physical provider associated.report to administrator!</div>");
		$("#result").show(500);
		return false;
	}
	}
    if ( ( index == 1 ) && ( parameter == true ) )  {
	hide = true;
	}
    if ( index == 2 ) {
	$('#id_virtualprovider').replaceWith('<select name="virtualprovider" id="id_virtualprovider">');
 	providerid = parameter.split(',')[0];
        providername= parameter.split(',')[1];
	newprovider = '<option value="' + providerid +'">'+providername+'</option>';
	$('#id_virtualprovider').html(newprovider);
	$('#id_virtualprovider').append('</select><p>');
	virtualproviderlabel.show(400);
	$('#id_virtualprovider').show(400) ;
	if ( hide == true ) {
		virtualproviderlabel.hide();
		$('#id_virtualprovider').hide() ;
			    }
	}
    if ( index == 3 ) {
	switch (profiletype){
	case 'ilo':
		if ( parameter != "" ) {
		$('#id_mac1').replaceWith('<select name="mac1" id="id_mac1">');	
		$.each(parameter, function(index, value){
			macname = value.split('=')[0];
			mac= value.split('=')[1];
			mac = '<option value="' + mac +'">'+macname+' : '+mac+'</option>';
        		macslist = macslist+mac;
		});
        	$('#id_mac1').html(macslist);
        	$('#id_mac1').append('</select><p>');
		}
		ipilo.val( ipiloval );
        	ipilolabel.show(400) ;
        	ipilo.show(400) ;
		ip1.val('');
        	mac1label.show(400) ;
        	$('#id_mac1').show(400);
		break;	
	case 'iso':
		$('#id_iso').replaceWith('<select name="iso" id="id_iso">');	
		$.each(parameter, function(index, value){
		newiso = '<option value="' + value +'">'+value+'</option>';
        	isoslist = isoslist+newiso;
		});
        	$('#id_iso').html(isoslist);
        	$('#id_iso').append('</select><p>');
        	isolabel.show(400) ;
        	iso.show(400) ;
		break;	
	}
	}
    if ( ( index == 4 )  && ( parameter == true ) ) {
	foreman = true;
 	parameterslabel.show() ;
        }
    if ( ( index == 5 )  && ( parameter == true ) ) {
	cobbler = true;
	parameterslabel.show(400) ;
         }
    if ( ( index == 6 )  && ( parameter == true ) ) {
  	partitioningfieldset.show(400);
 	$('#id_partitioning').replaceWith('<div id="id_partitioning" value="true"/>');
 	$('#id_partitioning').show();
 	rootvg.show(400);
 	rootvglabel.show(400);
 	rootsize.show(400);
 	rootsizelabel.show(400);
 	varsize.show(400);
 	varsizelabel.show(400);
 	tmpsize.show(400);
 	tmpsizelabel.show(400);
 	homesize.show(400);
 	homesizelabel.show(400);
 	swapsize.show(400);
 	swapsizelabel.show(400);
         }
    if ( index == 7 )  {
	if ( parameter >= 2 ) {
 	ip2label.show(400);
 	ip2.show(400);
	if ( profiletype == 'ilo' ) {
	if ( macslist != "" ) {
		$('#id_mac2').replaceWith('<select name="mac2" id="id_mac2">');	
        	$('#id_mac2').html(macslist);
        	$('#id_mac2').append('</select><p>');
			      }
 	mac2label.show(400);
        $('#id_mac2').show(400);
	}
	}
	if ( parameter >= 3 ) {
 	ip3label.show(400);
 	ip3.show(400);
	if ( profiletype == 'ilo' ) {
	if ( macslist != "" ) {
	$('#id_mac3').replaceWith('<select name="mac3" id="id_mac3">');	
        $('#id_mac3').html(macslist);
        $('#id_mac3').append('</select><p>');
	}
 	mac3label.show(400);
 	mac3.show(400);
        $('#id_mac3').show(400);
	}
	}
	if ( parameter >= 4 ) {
 	ip4label.show(400);
 	ip4.show(400);
	if ( profiletype == 'ilo' ) {
	if ( macslist != "" ) {
	$('#id_mac4').replaceWith('<select name="mac4" id="id_mac4">');	
        $('#id_mac4').html(macslist);
        $('#id_mac4').append('</select><p>');
	}
 	mac4label.show(400);
        $('#id_mac4').show(400);
	}
 	}
 	var numvms = $('#numvms').val();
	if ( numvms > 1 ) {
  	extravmsfieldset.show(400);
	}
	numinterfaces = parameter ;
   	for (var numvm = 2; numvm <= numvms; numvm++) {
			var additionalname = $('#id_name_'+String(numvm));
			var additionalnamelabel = $('#id_namelabel_'+String(numvm));
 			additionalname.show(400);
 			additionalnamelabel.show(400);
   		for (var numif = 1; numif <= numinterfaces; numif++) {
			var additionalip = $('#id_ip'+String(numif)+"_"+String(numvm));
			var additionaliplabel = $('#id_iplabel'+String(numif)+"_"+String(numvm));
 			additionalip.show(400);
 			additionaliplabel.show(400);
			if ( profiletype == 'ilo' ) {
			var additionalmac = $('#id_mac'+String(numif)+"_"+String(numvm));
			var additionalmaclabel = $('#id_maclabel'+String(numif)+"_"+String(numvm));
 			additionalmac.show(400);
 			additionalmaclabel.show(400);
			}
	}}
	}
    if ( index == 8 )  {	
  	storagedomain.html('<select id="id_storage"/>');
   	$.each(parameter, function(index, stor) {
  	var stor = '<option value="' + stor +'">'+stor+'</option>';
	storagedomain.append(stor);
	});
	storagedomain.append('</select><p>');
	storagedomain.show(400) ;
	storagedomainlabel.show(400) ;
	}
    if ( ( index == 9 ) && ( cobbler == true ) )  {	
	$('#id_cobblerprovider').replaceWith('<select name="cobblerprovider" id="id_cobblerprovider">');
 	providerid = parameter.split(',')[0];
        providername= parameter.split(',')[1];
	newprovider = '<option value="' + providerid +'">'+providername+'</option>';
	$('#id_cobblerprovider').html(newprovider);
	$('#id_cobblerprovider').append('</select><p>');
	cobblerproviderlabel.show(400);
	$('#id_cobblerprovider').show(400) ;
	if ( hide == true ) {
		cobblerproviderlabel.hide();
		$('#id_cobblerprovider').hide();
			    }
	}
    if ( ( index == 10 ) && ( foreman == true ) )  {	
	$('#id_foremanprovider').replaceWith('<select name="foremanprovider" id="id_foremanprovider">');
 	providerid = parameter.split(',')[0];
        providername= parameter.split(',')[1];
	newprovider = '<option value="' + providerid +'">'+providername+'</option>';
	$('#id_foremanprovider').html(newprovider);
	$('#id_foremanprovider').append('</select><p>');
	foremanproviderlabel.show(400);
	$('#id_foremanprovider').show(400) ;
	if ( hide == true ) {
		foremanproviderlabel.hide();
		$('#id_foremanprovider').hide() ;
			    }
	}

    if ( ( index == 11 ) && ( foreman == true ) )  {	
 	$('#id_hostgroup').replaceWith('<select name="hostgroup" id="id_hostgroup">');
 	var hostgroupslist = '';
   	$.each(parameter, function(index, value) {
	hostgroup = '<option value="' + value +'">'+value+'</option>';
        hostgroupslist = hostgroupslist+hostgroup;
	});
        $('#id_hostgroup').html(hostgroupslist);
        $('#id_hostgroup').append('</select><p>');
        $('#id_hostgroup').show(400) ;
        $('label[for="id_hostgroup"]').show(400) ;
	}

    if ( ( index == 12 ) && ( foreman == true ) )  {	
 	$('#id_puppetclasses').replaceWith('<select name="puppetclasses" id="id_puppetclasses" multiple>');
 	var puppetclasseslist = '';
   	$.each(parameter, function(index, value) {
	classe = '<option value="' + value +'">'+value+'</option>';
        puppetclasseslist = puppetclasseslist+classe;
	});
        $('#id_puppetclasses').html(puppetclasseslist);
        $('#id_puppetclasses').append('</select><p>');
        $('#id_puppetclasses').show(400) ;
        $('label[for="id_puppetclasses"]').show(400) ;
	}

	});
	}
	});
	});

  $('#id_type').change(function(){
  var type = $('#id_type option:selected').html(); 
  var newparms = '' ;
  $.ajax({  
   type: 'POST',
   url: '/nuages/type/',
   data: { 'type' : type } ,
   success: function(data) {
   $.each(data, function(index, parameter) {
    if ( index == 0 ) {
   	$.each(parameter, function(index, element) {
 	$('#'+element).hide();
	});
	}
    else if ( index == 1 ) {
    	newparms = parameter ;
	}
    else {
    newparms = newparms + ' '+ parameter ;
	 }
   });
    $("#custom").html(newparms);
    $("#custom").hide();
     }
     });
  extracontent.show();
  if ( type != 'default' ) {
   $("#"+type).show(400);
	}
  });

 ip2.hide();
 ip2label.hide();
 mac2.hide();
 mac2label.hide();
 ip3.hide();
 ip3label.hide();
 mac3.hide();
 mac3label.hide();
 ip4.hide();
 ip4label.hide();
 mac4.hide();
 mac4label.hide();
 
 puppetclasses.hide();
 puppetclasseslabel.click(function(){
 if ( puppetclasses.is(':visible') )  {
 puppetclasses.hide(300);
 }
 else {
 puppetclasses.show(300);
 }
 });

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

function createvm(){
  var type	        = $('#id_type').val();
  var storagedomain     = $('#id_storagedomain').val();
  var hostgroup         = $('#id_hostgroup').val();
  var cobblerparameters = $('#id_cobblerparameters').val();
  var name              = $('#id_name').val();
  var physical          = $('#id_physical').prop('checked');
  var virtualprovider   = $('#id_virtualprovider').val();
  var cobblerprovider   = $('#id_cobblerprovider').val();
  var foremanprovider   = $('#id_foremanprovider').val();
  var profile           = $('#id_profile').val();
  var ip1               = $('#id_ip1').val();
  var mac1              = $('#id_mac1').val();
  var mac2              = $('#id_mac2').val();
  var ip2               = $('#id_ip2').val();
  var ip3               = $('#id_ip3').val();
  var ip4               = $('#id_ip4').val();
  var iso               = $('#id_iso').val();
  var puppetclasses     = $('#id_puppetclasses').val();
  var parameters  	= $('#id_parameters').val();
  var ipilo             = $('#id_ipilo').val();
  var numvms            = $('#numvms').val();
  var name_2            = $('#id_name_2').val();
  var ip1_2             = $('#id_ip1_2').val();
  var ip2_2             = $('#id_ip2_2').val();
  var ip3_2             = $('#id_ip3_2').val();
  var ip4_2             = $('#id_ip4_2').val();
  var name_3            = $('#id_name_3').val();
  var ip1_3             = $('#id_ip1_3').val();
  var ip2_3             = $('#id_ip2_3').val();
  var ip3_3             = $('#id_ip3_3').val();
  var ip4_3             = $('#id_ip4_3').val();
  var name_4            = $('#id_name_4').val();
  var ip1_4             = $('#id_ip1_4').val();
  var ip2_4             = $('#id_ip2_4').val();
  var ip3_4             = $('#id_ip3_4').val();
  var ip4_4             = $('#id_ip4_4').val();
  var name_5            = $('#id_name_5').val();
  var ip1_5             = $('#id_ip1_5').val();
  var ip2_5             = $('#id_ip2_5').val();
  var ip3_5             = $('#id_ip3_5').val();
  var ip4_5             = $('#id_ip4_5').val();
  var name_6            = $('#id_name_6').val();
  var ip1_6             = $('#id_ip1_6').val();
  var ip2_6             = $('#id_ip2_6').val();
  var ip3_6             = $('#id_ip3_6').val();
  var ip4_6             = $('#id_ip4_6').val();
  var name_7            = $('#id_name_7').val();
  var ip1_7             = $('#id_ip1_7').val();
  var ip2_7             = $('#id_ip2_7').val();
  var ip3_7             = $('#id_ip3_7').val();
  var ip4_7             = $('#id_ip4_7').val();
  var name_8            = $('#id_name_8').val();
  var ip1_8             = $('#id_ip1_8').val();
  var ip2_8             = $('#id_ip2_8').val();
  var ip3_8             = $('#id_ip3_8').val();
  var ip4_8             = $('#id_ip4_8').val();
  var name_9            = $('#id_name_9').val();
  var ip1_9             = $('#id_ip1_9').val();
  var ip2_9             = $('#id_ip2_9').val();
  var ip3_9             = $('#id_ip3_9').val();
  var ip4_9             = $('#id_ip4_9').val();
  var name_10           = $('#id_name_10').val();
  var ip1_10            = $('#id_ip1_10').val();
  var ip2_10            = $('#id_ip2_10').val();
  var ip3_10            = $('#id_ip3_10').val();
  var ip4_10            = $('#id_ip4_10').val();
  var partitioning      = $('#id_partitioning').attr('value');
  custom 		=  $('#custom').html() ;
  var rootvg = $('#id_rootvg').val();
  var rootsize = $('#id_rootsize').val();
  var varsize = $('#id_varsize').val();
  var homesize = $('#id_homesize').val();
  var tmpsize = $('#id_tmpsize').val();
  var swapsize = $('#id_swapsize').val();
  if ( custom != '' ) {
  var custom = custom.split(' ');
  $.each(custom, function(index, parameter) {
    var value  = $("#id_"+parameter).val();
    if ( parameters == "" ) {
    parameters = parameter +"="+ value;
    }else {
    parameters = parameters + " "+ parameter +"="+ value;
	  }
    });
    }

   //handle partitioning
  if ( partitioning != '' ) {
  partitioning = " rootvg="+rootvg+" rootsize="+rootsize+" varsize="+varsize+" homesize="+homesize+" tmpsize="+tmpsize+" swapsize="+swapsize+" ";
  parameters = parameters +partitioning ;
	}
  //CHECK VALUES ARE THERE
  if ( ( name == "" ) || ( profile == "" ) || ( hostgroup == "" )  ) {
	$("#result").hide();
	$("#result").html("<div class='alert alert-error' ><button type='button' class='close' data-dismiss='alert'>&times;</button>Name/Profile/Hostgroup  cant be blank!</div>");
	$("#result").show(500);
	return ;
  }
  if (numvms >1 ){
   	for (var numvm = 2; numvm <= numvms; numvm++) {
			var additionalname = $('#id_name_'+String(numvm)).val();
			var additionalip = $('#id_ip_'+String(numvm)).val();
  			if  ( additionalname == "" )   {
				$("#result").hide();
				$("#result").html("<div class='alert alert-error'><button type='button' class='close' data-dismiss='alert'>&times;</button>Additional Name cant be blank!</div>");
				$("#result").show(500);
				return ;
  				}
	}
 }	
  var details = { 'name' : name , 'physicalprovider' : virtualprovider, 'virtualprovider' : virtualprovider , 'physical' : physical , 'cobblerprovider' : cobblerprovider , 'foremanprovider' : foremanprovider ,  'profile' : profile , 'ip1' : ip1 , 'mac1' : mac1 , 'ip2' : ip2 , 'mac2' : mac2 ,'ip3' : ip3 , 'ip4' : ip4 , 'iso' : iso , 'hostgroup' : hostgroup , 'type' : type, 'puppetclasses' : puppetclasses , 'parameters' : parameters , 'ipilo' : ipilo , 'name_2': name_2 , 'ip1_2' : ip1_2 ,'ip2_2' : ip2_2  , 'ip3_2' : ip3_2 , 'ip4_2' : ip4_2  , 'name_3': name_3 , 'ip1_3' : ip1_3 ,'ip2_3' : ip2_3  , 'ip3_3' : ip3_3 , 'ip4_3' : ip4_3  ,'name_4': name_4 , 'ip1_4' : ip1_4 ,'ip2_4' : ip2_4  , 'ip3_4' : ip3_4 , 'ip4_4' : ip4_4  ,'name_5': name_5 , 'ip1_5' : ip1_5 ,'ip2_5' : ip2_5  , 'ip3_5' : ip3_5 , 'ip4_5' : ip4_5  ,'name_6': name_6 , 'ip1_6' : ip1_6 ,'ip2_6' : ip2_6  , 'ip3_6' : ip3_6 , 'ip4_6' : ip4_6  ,'name_7': name_7 , 'ip1_7' : ip1_7 ,'ip2_7' : ip2_7  , 'ip3_7' : ip3_7 , 'ip4_7' : ip4_7  ,'name_8': name_8 , 'ip1_8' : ip1_8 ,'ip2_8' : ip2_8  , 'ip3_8' : ip3_8 , 'ip4_8' : ip4_8  ,'name_9': name_9 , 'ip1_9' : ip1_9 ,'ip2_9' : ip2_9  , 'ip3_9' : ip3_9 , 'ip4_9' : ip4_9  ,'name_10': name_10 , 'ip1_10' : ip1_10 ,'ip2_10' : ip2_10  , 'ip3_10' : ip3_10 , 'ip4_10' : ip4_10  , 'numvms' : numvms , 'storagedomain': storagedomain };
  	$.ajax({  
		type: 'POST',
		url: '/nuages/vms/',
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
