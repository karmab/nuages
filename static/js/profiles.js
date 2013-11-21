function getprofile(){
  baseurl = '';
  path = location.pathname.split('/');
  if ( path.length == 4 ) {
    baseurl = '/'+location.pathname.split('/')[1];
  }
  var profile = $('#id_profile').val();
  var data = { 'profile' : profile } ; 
  $.ajax({  
        type: "POST",
        url:  baseurl+'/profiles/',
        data: data,
        success: function(data) {
                $("#profileinfo").hide();
                $("#profileinfo").html(data);
                $("#profileinfo").show(500);
        },
        error: function(jqXHR, textStatus, errorThrown) {
                alert(errorThrown);
        }
        });
}

function profilecopy(){
  baseurl = '';
  path = location.pathname.split('/');
  if ( path.length == 4 ) {
    baseurl = '/'+location.pathname.split('/')[1];
  }
  var profile = $('#id_profile').val();
  var newprofile = $('#id_newprofile').val();
  var data = { 'profile' : profile , 'newprofile' : newprofile} ;
  $.ajax({
        type: "POST",
        url:  baseurl+'/profilecopy/',
        data: data,
        success: function(data) {
                $("#profileinfo").hide();
                $("#profileinfo").html(data);
                $("#profileinfo").show(500);
        },
        error: function(jqXHR, textStatus, errorThrown) {
                alert(errorThrown);
        }
        });
}
