<!DOCTYPE html>
<html>
	<head>
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
		<link rel="stylesheet" href="https://code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
		<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
		<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
		<script src="http://code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
		<style type="text/css" media="screen">
        @import url(http://fonts.googleapis.com/css?family=Varela+Round);
        @import url(http://necolas.github.io/normalize.css/3.0.2/normalize.css);
		
		body {
            background: #ECEEEF;
            margin: 100px 600px;
            max-width: 462px;
            font: 18px normal 'Varela Round', Helvetica, serif;
            color: #777B7E;
        }
		
		#container {
			/* border: 1px solid; */
			width: 655px;
		}
		
		#canvas-div {
			background: #fff;
            border-radius: 10px;
            border: 5px solid #D5DDE4;
            padding: 40px 40px;
            margin: 10px 0px;
			width: 650px;
			height: 600px;
			float:left;
		}
		
		#canvas {
			border: 2px solid black;
			border-radius: 10px;
			margin: 70px 135px; // height and width margin
		}
		
		#small-canvas {
			border: 1px solid black;
			border-radius: 2px;
			
		}
		
		.button-submit {
			background-color:#44c767;
			-moz-border-radius:5px;
			-webkit-border-radius:5px;
			border-radius:5px;
			border:1px solid #18ab29;
			display:inline-block;
			cursor:pointer;
			color:#ffffff;
			font-family:arial;
			font-size:17px;
			padding:16px 31px;
			text-decoration:none;
			text-shadow:0px 1px 0px #2f6627;
			width: 115px;
		}
		.button-submit:hover {
			background-color:#5cbf2a;
			text-decoration:none;
		}
		.button-submit:active {
			position:relative;
			top:1px;
		}
		
		.button-save {
			background-color:#44c767;
			-moz-border-radius:5px;
			-webkit-border-radius:5px;
			border-radius:5px;
			border:1px solid #18ab29;
			display:inline-block;
			cursor:pointer;
			color:#ffffff;
			font-family:arial;
			font-size:17px;
			padding:16px 37px;
			text-decoration:none;
			text-shadow:0px 1px 0px #2f6627;
			width: 115px;
		}
		.button-save:hover {
			background-color:#5cbf2a;
			text-decoration:none;
		}
		.button-save:active {
			position:relative;
			top:1px;
		}
		
		.button-train {
			background-color:#4CD2FF;
			-moz-border-radius:5px;
			-webkit-border-radius:5px;
			border-radius:5px;
			border:1px solid #18ab29;
			display:inline-block;
			cursor:pointer;
			color:#ffffff;
			font-family:arial;
			font-size:17px;
			padding:16px 37px;
			text-decoration:none;
			text-shadow:0px 1px 0px #2f6627;
			width: 115px;
		}
		.button-train:hover {
			background-color:#00BFFF;
			text-decoration:none;
		}
		.button-train:active {
			position:relative;
			top:1px;
		}
		
		.button-clear {
			background-color:#FF7373;
			-moz-border-radius:5px;
			-webkit-border-radius:5px;
			border-radius:5px;
			border:1px solid #18ab29;
			display:inline-block;
			cursor:pointer;
			color:#ffffff;
			font-family:arial;
			font-size:17px;
			padding:16px 35px;
			text-decoration:none;
			text-shadow:0px 1px 0px #2f6627;
			width: 115px;
		}
		.button-clear:hover {
			background-color:#FF4C4C;
			text-decoration:none;
		}
		.button-clear:active {
			position:relative;
			top:1px;
		}
	</style>
	</head>
	<?php 
	?>
	<body>
		<div id="container">
			<div id="canvas-div">
				<p>Please write an handwritten digit inside the black box</p>
				<!-- Note that the size of canvas must be defined inlinely without dimension-->
				<canvas id="canvas" width="280" height="280"></canvas>
				<span style="vertical-align:25%">Actual size (28 x 28) seen in Python:</span> <canvas id="small-canvas" width="28" height="28"></canvas>
			</div>
			<a class="button-submit" type="button">submit</a> <a class="button-save" type="button">save</a> <a class="button-clear" type="button">clear</a>
			<br><br>
			<a class="button-train" type="button">train</a> <span>with <span id="iter-num"></span> iterations</span>
			<br><br>
			<div id="slider"></div>
		</div>
	</body>
	<script>
	$(function() {
		// The DOM is ready!
		
		// Paint functionality
		var context = document.getElementById('canvas').getContext("2d");
		var small_context = document.getElementById("small-canvas").getContext("2d");
		var clickX = new Array();    // The clicked x positions
		var clickY = new Array();    // The clicked y positions
		var clickDrag = new Array(); // The dragged position from the clicked x, y position
		
		
		// The boolean paint will let us know if the virtual marker is pressing down on the paper 
		// or not. If paint is true, then we record the value. Then redraw.
		var paint;

		function addClick(x, y, dragging) {
			clickX.push(x);
			clickY.push(y);
			clickDrag.push(dragging);
		}
		
		function redraw(){
			context.clearRect(0, 0, context.canvas.width, context.canvas.height); // Clears the canvas
			context.strokeStyle = "#008C23";
			context.lineJoin = "round";
			context.lineWidth = 12;
				
			for(var i=0; i < clickX.length; i++) {		
				context.beginPath();
				if(clickDrag[i] && i){
					context.moveTo(clickX[i-1], clickY[i-1]);
				}else{
					context.moveTo(clickX[i]-1, clickY[i]);
				}
				context.lineTo(clickX[i], clickY[i]);
				context.closePath();
				context.stroke();
			}
		}
		
		// Handler for clear button
		function clearCanvas() {
			context.clearRect(0, 0, context.canvas.width, context.canvas.height);
			small_context.clearRect(0, 0, small_context.canvas.width, small_context.canvas.height);
			$(".msg").remove();
		}
		
		// Turn ImageData.data into a graycale array, put it in small canvas and return the pixel data
		function colorToGrayscale(ctx, canvas) {
			var imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
			var pixels  = imgData.data;
			var grayscalePixel = new Array(pixels.length / 4);
			var j = 0;
			for (var i = 0, n = pixels.length; i < n; i += 4) {
				// The Luminance Algorithm - red x 0.3 + green x 0.59 + blue x 0.
				var grayscale = pixels[i] * .3 + pixels[i+1] * .59 + pixels[i+2] * .11;
				pixels[i] = grayscale;        // red
				pixels[i+1] = grayscale;      // green
				pixels[i+2] = grayscale;      // blue
				// There will be an alpha channel but we will not change it
				
				grayscalePixel[j] = grayscale;
				j++;
			}
			//redraw the image in black & white
			ctx.putImageData(imgData, 0, 0);
			return grayscalePixel; // You can take this if needed
		}
		
		$('#canvas').mousedown(function(e){
			var mouseX = e.pageX - this.offsetLeft;
			var mouseY = e.pageY - this.offsetTop;
				
			paint = true;
			addClick(mouseX, mouseY);
			redraw();
		});
		
		$('#canvas').mousemove(function(e){
			if(paint){
				addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop, true);
				redraw();
			}
		});
		
		$('#canvas').mouseup(function(e){
			paint = false;
		});
		
		$('.button-clear').click(function(e) {
			clickX = new Array();
			clickY = new Array();
			clickDrag = new Array();
			clickColor = new Array();
			clearCanvas();
		});

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
		
		$("#slider").slider({
			min: 100,
			max: 10000,
			step: 50,
			slide: function( event, ui ) {
				$("#iter-num").text(ui.value);
			}
		});
		$("#iter-num").text("100");
	});
	</script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
</html>