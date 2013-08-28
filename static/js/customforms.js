function customformget() {
  $("#forminfo").hide();
  var type = $('#id_type').val();
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
  $.ajax({  
        type: "POST",
        url: '/nuages/customformedit/',
        data: { 'type' : type },
        success: function(data) {
        $('#forminfo').replaceWith("<table id='forminfo' border='1' class='alert alert-info'><tr><td>Attribute</td><td>Type</td><td>Value(s)</td><td>Required</td><td>Actions</td></tr>");
        var attributesinfo = '';
        $.each(data, function(index, parameter) {
  	var required = '';
	if ( parameter[3] == true ) {
	required = "checked" ;
	}
        //newattr = '<tr><td>'+parameter[0]+'</td><td>'+parameter[1]+'</td><td><input type="text" value="'+parameter[2]+'"</></td><td><input type="checkbox" '+required+'></td></tr>';
        newattr = '<tr id="'+parameter[0]+'"><td>'+parameter[0]+'</td><td>'+parameter[1]+'</td><td><input type="text" value="'+parameter[2]+'"></td><td><input type="checkbox" '+required+'></td>'+'<td><input type="submit" class="btn btn-info" value="update" onclick=updateparam("'+parameter[0]+'");"><input type="submit" class="btn btn-info" value="remove" onclick=removeparam("'+parameter[0]+'");"></td></tr>';
        attributesinfo = attributesinfo+newattr;
        });
        $('#forminfo').append(attributesinfo);
        $('#forminfo').append('<input type="submit"  class="btn btn-info" value="add" onclick="addparam();"></table><p>');
        $("#forminfo").show(500);
        $("#validate").show(500);
        },
        error: function(jqXHR, textStatus, errorThrown) {
                alert(errorThrown);
        }
        });
}

function removeparam(parameter) {
  alert(parameter);
  $(parameter).hide();
}
