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
