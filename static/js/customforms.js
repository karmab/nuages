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
   newattr = '<tr id="'+paramname+'"><td>'+paramname+'</td><td>'+paramtype+'</td><td><input type="text" value="'+paramdefault+'"></td><td><input type="checkbox" '+required+'></td>'+'<td><input type="submit" class="btn btn-info" value="remove" onclick="removeparam(\''+paramname+'\');"></td></tr>';
   $('#newparameter').replaceWith(newattr);
   $('#parameters').append(" "+paramname);
   $('#forminfo').append('<tr id="newparameter" ><td><input type="text" id="newparameter-name" ></td><td><select id="newparameter-type"><option value="CharField">Char</option><option value="ChoiceField">Choice</option><option value="IntegerField">Int</option></select></td><td><input type="text" id="newparameter-default"></td><td><input id="newparameter-required" type="checkbox"></td><td><input type="submit" class="btn btn-info" value="remove" onclick="removenewparam();"></td</tr>');
  }
  else if ( $('#newparameter-name').val() == "" ) {
   $("#result").html("<div class='alert alert-error'><button type='button' class='close' data-dismiss='alert'>&times;</button>Name required for your new parameter!</div>");
   $("#results").show(200);
  }
  else {
   $('#forminfo').append('<tr id="newparameter" ><td><input type="text" id="newparameter-name" ></td><td><select id="newparameter-type"><option value="CharField">Char</option><option value="ChoiceField">Choice</option><option value="IntegerField">Int</option></select></td><td><input type="text" id="newparameter-default"></td><td><input id="newparameter-required" type="checkbox"></td><td><input type="submit" class="btn btn-info" value="remove" onclick="removenewparam();"></td</tr>');
  }
}

function removeparam(element) {
   $('#'+element).hide();
   parameters = $('#parameters').html().replace(element,"");
   $('#parameters').replaceWith('<div id="parameters">'+parameters+'</div>');
   $('#parameters').show(400);
}


function removenewparam() {
  $('#newparameter').remove();
}

function modifyparam(element) {
  alert(element);
}

function customformget() {
  $("#forminfo").hide();
  var type = $('#id_type').val();
  if ( type == '' ) {
  return;
  }
  $.ajax({  
        type: "POST",
        url: '/nuages/customforms/',
        data: { 'type' : type },
        success: function(data) {
        $('#forminfo').replaceWith("<table id='forminfo' border='1' class='alert alert-info'><tr><td>Attribute</td><td>Type</td><td>Value(s)</td><td>Required</td></tr>");
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
        $("#forminfo").show(500);
        },
        error: function(jqXHR, textStatus, errorThrown) {
                alert(errorThrown);
        }
        });
}

function customformedit() {
  $("#forminfo").hide();
  var type = $('#id_type').val();
  if ( type == '' ) {
  return;
  }
  $.ajax({  
        type: "POST",
        url: '/nuages/customformedit/',
        data: { 'type' : type },
        success: function(data) {
        $('#forminfo').replaceWith("<table id='forminfo' border='1' class='alert alert-info'><tr><td>Attribute</td><td>Type</td><td>Value(s)</td><td>Required</td><td>Actions</td></tr>");
        var attributeslist = '';
        var attributesinfo = '';
        $.each(data, function(index, parameter) {
        attributeslist = attributeslist+" "+parameter[0];
  	var required = '';
	if ( parameter[3] == true ) {
	required = "checked" ;
	}
       newattr = '<tr id="'+parameter[0]+'"><td>'+parameter[0]+'</td><td>'+parameter[1]+'</td><td><input type="text" value="'+parameter[2]+'"></td><td><input type="checkbox" '+required+'></td>'+'<td><input type="submit" class="btn btn-info" value="remove" onclick="removeparam(\''+parameter[0]+'\');"></td></tr>';
        attributesinfo = attributesinfo+newattr;
        });
        $('#forminfo').append(attributesinfo);
        $('#forminfo').append('<input type="submit"  class="btn btn-info" value="add parameter" onclick="addparam();"><input type="submit"  class="btn btn-info" value="update type" onclick="updatetype();"></table><p>');
        $("#forminfo").show(500);
        //$("#validate").show(500);
        $('#parameters').html(attributeslist);
        },
        error: function(jqXHR, textStatus, errorThrown) {
                alert(errorThrown);
        }
        });
}
