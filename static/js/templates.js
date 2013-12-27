function gettemplates(){
  baseurl = '';
  path = location.pathname.split('/');
  if ( path.length == 4 ) {
    baseurl = '/'+location.pathname.split('/')[1];
  }
  $("#results").replaceWith('<div id="results"></div>');
  $("#actionwheel").show();
  var virtualprovider = $('#id_virtualprovider').val();
  var data = { 'virtualprovider' : virtualprovider } ;
  $.ajax({  
       type: "POST",
        url: baseurl+'/gettemplates/',
        data: data,
        success: function(data) {
            $("#actionwheel").hide();
            $("#results").hide();
            $("#results").addClass("alert alert-success");
            $("#results").html("<button type='button' class='close' data-dismiss='alert'>&times;</button>");
            $("#results").append(data);
            $("#results").show(200);
		}
	});
}
