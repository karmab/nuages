function addparam() {
  if ( ( $('#newparameter-name').length != 0 ) && ( $('#newparameter-name').val() != "" ) ) {
   var paramname     =  $('#newparameter-name').val();
   var paramtype     =  $('#newparameter-type').val();
   var paramdefault  =  $('#newparameter-default').val();
   var paramrequired =  $('#newparameter-required').prop("checked");
   var required = '';
   if ( paramrequired == true ) {
    required = "checked" ;
    }
   newattr = '<tr id="'+paramname+'"><td>'+paramname+'</td><td id="'+paramname+'-type">'+paramtype+'</td><td><input type="text" id="'+paramname+'-default" '+'value="'+paramdefault+'"></td><td><input id="'+paramname+'-required" '+'type="checkbox" '+required+'></td>'+'<td><input type="submit" class="btn btn-danger" value="remove" onclick="removeparam(\''+paramname+'\');"></td></tr>';
   $('#newparameter').replaceWith(newattr);
   if ( $('#parameters').html() == "" ) {
   $('#parameters').append(paramname);
   $('#parameters').hide();
   }
   else {
   $('#parameters').append(" "+paramname);
   $('#parameters').hide();
   }
   $('#forminfo').append('<tr id="newparameter" ><td><input type="text" id="newparameter-name" ></td><td><select id="newparameter-type"><option value="CharField">CharField</option><option value="ChoiceField">ChoiceField</option><option value="IntegerField">IntegerField</option></select></td><td><input type="text" id="newparameter-default"></td><td><input id="newparameter-required" type="checkbox"></td><td><input type="submit" class="btn btn-danger" value="remove" onclick="removenewparam();"></td</tr>');
  }
  else if ( $('#newparameter-name').val() == "" ) {
   $("#result").html("<div class='alert alert-error'><button type='button' class='close' data-dismiss='alert'>&times;</button>Name required for your new parameter!</div>");
   $("#results").show(200);
  }
  else {
   $('#forminfo').append('<tr id="newparameter" ><td><input type="text" id="newparameter-name" ></td><td><select id="newparameter-type"><option value="CharField">CharField</option><option value="ChoiceField">ChoiceField</option><option value="IntegerField">IntegerField</option></select></td><td><input type="text" id="newparameter-default"></td><td><input id="newparameter-required" type="checkbox"></td><td><input type="submit" class="btn btn-danger" value="remove" onclick="removenewparam();"></td</tr>');
  }

}

function customformcreate() {
   $('#parameters').replaceWith('<div id="parameters"></div>');
   $('#for_newtype').remove();
   $('#id_newtype').remove();
   $('#forminfo').replaceWith('<label id="for_newtype">New type name:</label><input type="text" id="id_newtype" ><table id="forminfo" border="1" class="alert alert-info table table-condensed table-bordered"><tr><td>Attribute</td><td>Type</td><td>Value(s)</td><td>Required</td></tr>');
   $('#forminfo').append('<tr id="newparameter" ><td><input type="text" id="newparameter-name" ></td><td><select id="newparameter-type"><option value="CharField">Charfield</option><option value="ChoiceField">ChoiceField</option><option value="IntegerField">IntegerField</option></select></td><td><input type="text" id="newparameter-default"></td><td><input id="newparameter-required" type="checkbox"></td><td><input type="submit" class="btn btn-danger" value="remove" onclick="removenewparam();"></td</tr>');
   $('#forminfo').append('<input type="submit"  class="btn btn-info" value="add parameter" onclick="addparam();"></table><p>');
 }

function removeparam(element) {
   $('#'+element).hide();
   parameters = $('#parameters').html().replace(element,"");
   $('#parameters').replaceWith('<div id="parameters" style="display: none;">'+parameters+'</div>');
   $('#parameters').hide();
}


function removenewparam() {
  $('#newparameter').remove();
}

function modifyparam(element) {
  alert(element);
}

function customformget() {
  baseurl = '';
  path = location.pathname.split('/');
  if ( path.length == 4 ) {
          baseurl = '/'+location.pathname.split('/')[1];
  }
  $("#forminfo").hide();
  var type = $('#id_type').val();
  if ( type == '' ) {
  return;
  }
  $.ajax({  
        type: "POST",
        url: baseurl+'/customforms/',
        data: { 'type' : type },
        success: function(data) {
        $('#forminfo').replaceWith("<table id='forminfo' border='1' class='alert alert-info table table-condensed table-bordered'><tr><td>Attribute</td><td>Type</td><td>Value(s)</td><td>Required</td></tr>");
        var attributesinfo = '';
        $.each(data, function(index, parameter) {
	choices=parameter[2];
        if ( parameter[1] == 'Choice' ){
	 var choices = '<select>';
        $.each(parameter[2], function(num,choice) {
	  choices = choices+'<option>'+choice+'</option>'; 	
  	   });
	  choices = choices+'</select>'; 	
	}
        newattr = '<tr><td>'+parameter[0]+'</td><td>'+parameter[1]+'</td><td>'+choices+'</td><td>'+parameter[3]+'</td></tr>';
        attributesinfo = attributesinfo+newattr;
        });
        $('#forminfo').append(attributesinfo);
        $('#forminfo').append('</table><p>');
        $("#forminfo").show(1000);
        },
        error: function(jqXHR, textStatus, errorThrown) {
                alert(errorThrown);
        }
        });
}

function customformedit() {
  baseurl = '';
  path = location.pathname.split('/');
  if ( path.length == 4 ) {
          baseurl = '/'+location.pathname.split('/')[1];
  }
  $('#for_newtype').remove();
  $('#id_newtype').remove();
  $("#forminfo").hide();
  var type = $('#id_type').val();
  if ( type == '' ) {
  return;
  }
  $.ajax({  
        type: "POST",
        url: baseurl+'/customformedit/',
        data: { 'type' : type },
        success: function(data) {
        $('#forminfo').replaceWith("<table id='forminfo' border='1' class='alert alert-info table table-condensed table-bordered '><tr><td>Attribute</td><td>Type</td><td>Value(s)</td><td>Required</td><td>Actions</td></tr>");
        var attributeslist = '';
        var attributesinfo = '';
        $.each(data, function(index, parameter) {
        if ( index == 0 ) {
        attributeslist = parameter[0];
        } else {
        attributeslist = attributeslist+" "+parameter[0];
        }
  	var required = '';
	if ( parameter[3] == true ) {
	required = "checked" ;
	}
       //newattr = '<tr id="'+parameter[0]+'"><td>'+parameter[0]+'</td><td>'+parameter[1]+'</td><td><input type="text" value="'+parameter[2]+'"></td><td><input type="checkbox" '+required+'></td>'+'<td><input type="submit" class="btn btn-info" value="remove" onclick="removeparam(\''+parameter[0]+'\');"></td></tr>';
       newattr = '<tr id="'+parameter[0]+'"><td>'+parameter[0]+'</td><td id="'+parameter[0]+'-type">'+parameter[1]+'</td><td><input type="text" id="'+parameter[0]+'-default" '+'value="'+parameter[2]+'"></td><td><input id="'+parameter[0]+'-required" '+'type="checkbox" '+required+'></td>'+'<td><input type="submit" class="btn btn-danger" value="remove" onclick="removeparam(\''+parameter[0]+'\');"></td></tr>';
        attributesinfo = attributesinfo+newattr;
        });
        $('#forminfo').append(attributesinfo);
        $('#forminfo').append('<input type="submit"  class="btn btn-info" value="add parameter" onclick="addparam();"></table><p>');
        $("#forminfo").show(500);
        $('#parameters').html(attributeslist);
   	$('#parameters').hide();
        },
        error: function(jqXHR, textStatus, errorThrown) {
                alert(errorThrown);
        }
        });
}

function customformupdate() {
  baseurl = '';
  path = location.pathname.split('/');
  if ( path.length == 4 ) {
          baseurl = '/'+location.pathname.split('/')[1];
  }
 if ( ( $('#id_type').val() == "" ) && ( $('#id_newtype').length == 0 ) ) {
 return;
 }
 else if ( ( $('#id_newtype').length != 0 ) && ( $('#id_newtype').val() != "" ) )  {
  type=$('#id_newtype').val();
 }
 else if ( $('#id_type').val() != "" ) {
  type=$('#id_type').val();
 }
 parameters = $('#parameters').html();
 data = '';
 missing = false;
 if ( parameters == '' ) {
  	$.ajax({  
	 type: "POST",
         url: baseurl+'/customformcreate/',
         data: { 'type' : type  },
         success: function(data) {
   	 $("#result").html(data);
   	 $("#results").show(200);
         $('#id_type').append('<option value="'+type+'">'+type+'</option></select><p></p>');
                                 }
              });
 	return;
 }
 var parameters = parameters.split(' ');
 $.each(parameters, function(index, paramname) {
 paramtype=$('#'+paramname+"-type").html();
 paramdefault=$('#'+paramname+"-default").val();
 paramrequired=$('#'+paramname+"-required").prop("checked");
 if ( ( paramtype  == undefined ) || ( paramdefault  == undefined ) || ( paramrequired  == undefined )  ) {
  $("#result").html("<div class='alert alert-error'><button type='button' class='close' data-dismiss='alert'>&times;</button>Missing parameters</div>");
  $("#results").show(200);
  missing = true ;
  return;
 }
 if ( index == 0 ) {
  data = paramname+";"+paramtype+";"+paramdefault+";"+paramrequired;
 } else {
  data = data+' ' +paramname+";"+paramtype+";"+paramdefault+";"+paramrequired;
 }
 });
 if ( missing == true ) {
 return;
 }
  $.ajax({  
        type: "POST",
        url: baseurl+'/customformupdate/',
        data: { 'type' : type , 'parameters' : data  },
        success: function(data) {
   	$("#result").html(data);
   	$("#results").show(200);
        $('#id_type').append('<option value="'+type+'">'+type+'</option></select><p></p>');
  }
  });

}



function customformdelete() {
 baseurl = '';
 path = location.pathname.split('/');
 if ( path.length == 4 ) {
    baseurl = '/'+location.pathname.split('/')[1];
    }
 $("#forminfo").hide();
 if ( $('#id_type').val() == ""  ) {
  return;
 }
 type=$('#id_type').val();
 $.ajax({  
        type: "POST",
        url: baseurl+'/customformdelete/',
        data: { 'type' : type  },
        success: function(data) {
   	$("#result").html(data);
   	$("#results").show(200);
   	types = $('#id_type').html().replace('<option value="'+type+'">'+type+'</option>',"");
        $('#id_type').replaceWith('<select name="type" id="id_type">'+types+'</select><p>');
  	}
  });
}
function customformcobbler() {
 baseurl = '';
 path = location.pathname.split('/');
 if ( path.length == 4 ) {
    baseurl = '/'+location.pathname.split('/')[1];
    }
 var sure = confirm("This will recreate from scratch all your customtypes from cobbler providers classes!!!Sure?");
 if (sure) {
 $.ajax({  
    type: "GET",
    url: baseurl+'/customformcobbler/',
    success: function(data) {
   	$("#result").html(data);
   	$("#results").show(200);
     }
  });

 } else {
  return;
 }

}

function customformforeman() {
 baseurl = '';
 path = location.pathname.split('/');
 if ( path.length == 4 ) {
    baseurl = '/'+location.pathname.split('/')[1];
    }
 if (sure) {
 $.ajax({  
    type: "GET",
    url: baseurl+'/customformforeman/',
    success: function(data) {
   	$("#result").html(data);
   	$("#results").show(200);
     }
  });

 } else {
  return;
 }

}







