var chart = AmCharts.makeChart("chartdiv5", {
			"type": "serial",
			"theme": "light",
			"legend": {
				"equalWidths": false,
				"useGraphSettings": true,
				"valueAlign": "left",
				"valueWidth": 120
			},
			"dataLoader": { 
			"url": "index_page/chart.json",  
			"format": "json"
			},  

			"valueAxes": [{
				"id": "distanceAxis",
				"axisAlpha": 0,
				"gridAlpha": 0,
				"position": "left",
				"title": "Total Customers"
			}, 
			{
				"id": "latitudeAxis",
				"axisAlpha": 0,
				"gridAlpha": 0,
				"labelsEnabled": false,
				"position": "left"
			}, 

			{
				"id": "durationAxis",
				"axisAlpha": 0,
				"gridAlpha": 0,
				"inside": false,
				"labelsEnabled": true,
				"position": "right",
				"title": "Total Subcriber"
			},

			{
				"id": "duration2Axis",
				"axisAlpha": 0,
				"gridAlpha": 0,
				"inside": false,
				"labelsEnabled": false,
				"position": "left",
			}

			],
			"graphs": [{
				"balloonText": "Total Customers [[value]]",
				"dashLengthField": "dashLength",
				"fillAlphas": 0.7,
				"legendPeriodValueText": "[[value.sum]] people",
				"legendValueText": "[[value]] people",
				"title": "Total Customer",
				"type": "column",
				"valueField": "totalCustomer",
				"valueAxis": "distanceAxis"
			}, 

			{
				"balloonText": "New customers:[[value]]",
				"bullet": "round",
				"bulletBorderAlpha": 1,
				"useLineColorForBulletBorder": true,
				"bulletColor": "#FFFFFF",
				"dashLengthField": "dashLength",
				"legendPeriodValueText": "[[value.sum]] people",
				"labelPosition": "right",
				"legendValueText": "[[value]] people",
				"title": "New Customers",
				"fillAlphas": 0,
				"valueField": "newCustomer",
				"valueAxis": "latitudeAxis"
			}, 

			{
				"balloonText": "Total Subcriber:[[value]]",
				"bullet": "square",
				"bulletBorderAlpha": 1,
				"bulletBorderThickness": 1,
				"dashLengthField": "dashLength",
				"legendPeriodValueText": "[[value.sum]] people",
				"legendValueText": "[[value]] people",
				"title": "Total Subcriber",
				"fillAlphas": 0,
				"valueField": "currentSuccess",
				"valueAxis": "durationAxis"
			},

			{
				"balloonText": "New Subcriber:[[value]]",
				"bullet": "square",
				"bulletBorderAlpha": 1,
				"bulletBorderThickness": 1,
				"dashLengthField": "dashLength",
				"legendValueText": "[[value]] people",
				"legendPeriodValueText": "[[value.sum]] people",
				"title": "Total New Subcriber",
				"fillAlphas": 0,
				"valueField": "successNewCustomer",
				"valueAxis": "duration2Axis"
			}

			],
			"chartCursor": {
				"cursorAlpha": 0.1,
				"cursorColor":"#052963",
				 "fullWidth":true,
				"valueBalloonsEnabled": false,
				"zoomable": false
			},
			"categoryField": "month",
			"axisColor": "#555555",
			"gridAlpha": 0.1,
			"gridColor": "#FFFFFF",
			"export": {
				"enabled": true
			 }
		});