function templateslist(){
  baseurl = '';
  path = location.pathname.split('/');
  if ( path.length == 4 ) {
    baseurl = '/'+location.pathname.split('/')[1];
  }
  $('#actionwheel').show();
  var virtualprovider = $('#id_virtualprovider').val();
  var data = { 'virtualprovider' : virtualprovider } ;
  $.ajax({  
       type: 'POST',
        url: baseurl+'/templateslist/',
        data: data,
        success: function(data) {
            $('#actionwheel').hide();
            $('#id_template').hide();
            $('#id_template').replaceWith('<select id="id_template"><option value="" selected="selected">---------</option>');
            var templateslist = '';
            $.each(data, function(index, value){
                newtemplate = '<option value="' + value +'">'+value+'</option>';
                templateslist = templateslist+newtemplate;
                                               });
            $('#id_template').html(templateslist);
            $('#id_template').append('</select><p>');
            $('#id_template').show(400);
        }
	});
}

function createtemplateprofile(){
  baseurl = '';
  path = location.pathname.split('/');
  if ( path.length == 4 ) {
    baseurl = '/'+location.pathname.split('/')[1];
  }
  $('#actionwheel').show();
  var virtualprovider = $('#id_virtualprovider').val();
  var template = $('#id_template').val();
  var name = $('#name').val();
  if ( ( template == '' ) || ( name == '') ) {
    $('#actionwheel').hide();
    $('#results').hide();
    $('#results').addClass("alert alert-error");
    $('#results').html("<button type='button' class='close' data-dismiss='alert'>&times;</button>");
    $('#results').append('Template or name missing');
    $("#results").show(400);
    return;
  }
  var data = { 'virtualprovider' : virtualprovider , 'name' : name , 'template' : template } ;
  $.ajax({  
       type: 'POST',
        url: baseurl+'/createtemplateprofile/',
        data: data,
        success: function(data) {
            $('#actionwheel').hide();
            $('#results').hide();
            $('#results').addClass('alert alert-success');
            $('#results').html("<button type='button' class='close' data-dismiss='alert'>&times;</button>");
            $('#results').append(data);
            $("#results").show(400);
        }
	});
}
