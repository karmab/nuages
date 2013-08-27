function customformget() {
  $("#forminfo").hide();
  var type = $('#id_type').val();
  $.ajax({  
        type: "POST",
        url: '/nuages/customforms/',
        data: { 'type' : type },
        success: function(data) {
        $('#forminfo').replaceWith("<table id='forminfo' border='1' class='alert alert-info'><tr><td>Attribute</td><td>Type</td><td>Default Value</td><td>Required</td></tr>");
        var attributesinfo = '';
        $.each(data, function(index, parameter) {
        newattr = '<tr><td>'+parameter[0]+'</td><td>'+parameter[1]+'</td><td>'+parameter[2]+'</td><td>'+parameter[3]+'</td></tr>';
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
        $('#forminfo').replaceWith("<table id='forminfo' border='1' class='alert alert-info'><tr><td>Attribute</td><td>Type</td><td>Default Value</td><td>Required</td></tr>");
        var attributesinfo = '';
        $.each(data, function(index, parameter) {
  	var required = '';
	if ( parameter[3] == true ) {
	required = "checked" ;
	}
        newattr = '<tr><td><input type="text" value="'+parameter[0]+'"</></td><td><input type="text" value="'+parameter[1]+'"</></td><td><input type="text" value="'+parameter[2]+'"</></td><td><input type="checkbox" '+required+'></td></tr>';
        attributesinfo = attributesinfo+newattr;
        });
        $('#forminfo').append(attributesinfo);
        $('#forminfo').append('</table><p>');
        $("#forminfo").show(500);
        $("#validate").show(500);
        },
        error: function(jqXHR, textStatus, errorThrown) {
                alert(errorThrown);
        }
        });
}
