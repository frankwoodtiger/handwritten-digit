$(function() {
	// extract the necessary variables and function from JQuery global scope
	var context = $.context;
	var small_context = $.small_context;
	var colorToGrayscale = $.colorToGrayscale
	$(document).on("click", ".button-submit",function() { 
		$(".msg").remove();
		small_context.drawImage(context.canvas , 0, 0, 28, 28); // draw the image on small canvas
		var imageData_gs_1d = colorToGrayscale(small_context, small_context.canvas);
		// console.log(small_context.getImageData(0, 0, 28, 28).data);
		$.ajax({
			url: '/cgi-bin/feedforward-prediction-cgi.py', 
			type: 'post',
			data: {"imageData_gs_1d":JSON.stringify(imageData_gs_1d)},
			success: function(data, status) {
				// data = JSON.parse(data); // parse JSON string into JSON object
				if (data) {
					$("#canvas-div").append("<p class=\"msg\">Prediction from Neural Network:" + data + "</p>");
				}
				// console.log(data.size());
			},
			error: function(xhr, desc, err) {
				console.log(xhr);
				console.log("Details: " + desc + "\nError:" + err);
			}
		});
	});
	
	$(document).on("click", ".button-save",function() { 
		$(".msg").remove();
		small_context.drawImage(context.canvas , 0, 0, 28, 28); // draw the image on small canvas
		var imageData_gs_1d = colorToGrayscale(small_context, small_context.canvas);
		// console.log(small_context.getImageData(0, 0, 28, 28).data);
		// console.log(imageData_gs_1d);
		$.ajax({
			url: '/cgi-bin/save-grayscale-to-mat-cgi.py', 
			type: 'post',
			data: {"imageData_gs_1d":JSON.stringify(imageData_gs_1d)},
			success: function(data, status) {
				// data = JSON.parse(data); // parse JSON string into JSON object
				if (data){
					$("#canvas-div").append("<p class=\"msg\">Saved!</p>");	
				}
				else {
					$("#canvas-div").append("<p class=\"msg\">No data returned!</p>");	
				}
				// console.log(data);
			},
			error: function(xhr, desc, err) {
				console.log(xhr);
				console.log("Details: " + desc + "\nError:" + err);
			}
		});
	});
	
	$(document).on("click", ".button-train",function() { 
		$(".msg").remove();
		$.ajax({
			url: '/cgi-bin/train-handwritten-digit-cgi.py', 
			type: 'post',
			data: {"iter": $("#iter-num").text()},
			success: function(data, status) {
				// data = JSON.parse(data); // parse JSON string into JSON object
				if (data){
					$("#canvas-div").append("<p class=\"msg\">" + data + "</p>");	
				}
				else {
					$("#canvas-div").append("<p class=\"msg\">No data returned!</p>");	
				}
				// console.log(data);
			},
			error: function(xhr, desc, err) {
				console.log(xhr);
				console.log("Details: " + desc + "\nError:" + err);
			}
		});
	});
});