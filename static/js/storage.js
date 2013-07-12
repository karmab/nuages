function getstorage(){
  var virtualprovider = $('#id_virtualprovider').val();
  var data = { 'virtualprovider' : virtualprovider } ; 
  $.ajax({  
        type: "POST",
        url: '/nuages/storage/',
        data: data,
        success: function(data) {
//            $("#storageinfo").hide();
//            $("#storageinfo").html(data);
//            $("#storageinfo").show(200);
//		}
//	});
//}
	$("#error").hide();
	$("#storageinfo").hide();
	$("#storageinfo0").hide();
	$("#storageinfo1").hide();
	$("#storageinfo2").hide();
	$("#storageinfo3").hide();
	$("#storageinfo4").hide();
	$("#storageinfo5").hide();
	$("#storageinfo6").hide();
	$("#storageinfo7").hide();
	$("#storageinfo8").hide();
	$("#storageinfo9").hide();
	$("#storageinfo10").hide();
	$("#storageinfo11").hide();
	var counter=0 ; 	
	$.each(data, function(key, value) {
	if ( key == 'failure' )  {
		$("#error").html(value);
                $("#error").show(500);
		return ;
	}
	var sd = "#storageinfo" + counter ; 
	counter = counter +1 ; 
        //$('#storageinfo').highcharts({
        $(sd).highcharts({
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: key
            },
            tooltip: {
        	pointFormat: '{series.name}: <b>{point.percentage}%</b>',
            	percentageDecimals: 1
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
		    showInLegend: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        color: '#000000',
                        connectorColor: '#000000',
                        formatter: function() {
                            //return '<b>'+ this.point.name +'</b>: '+ this.percentage +' %';
                            return '<b>'+  Math.round(this.y)+'GB';
                        }
                    }
                }
            },
            series: [{
                type: 'pie',
                name: 'Storage Information',
                data: [
                    ['Used',   value[0] ],
                    ['Available', value[1]  ]
                ]
            }]
        });
            $(sd).show(500);
        });
               //$("#storageinfo").html(data);
                $("#storageinfo").show(500);
        },
        error: function(jqXHR, textStatus, errorThrown) {
                alert(errorThrown);
        }

        });
}
