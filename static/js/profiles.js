function getprofile(){
  var profile = $('#id_profile').val();
  var data = { 'profile' : profile } ; 
  $.ajax({  
        type: "POST",
        url: '/nuages/profiles/',
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
  alert("prout");
  return;
  var profile = $('#id_profile').val();
  var newprofile = $('#id_newprofile').val();
  var data = { 'profile' : profile , 'newprofile' : newprofile} ;
  $.ajax({
        type: "POST",
        url: '/nuages/profilecopy/',
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
