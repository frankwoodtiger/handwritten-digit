$(function() {
	// Paint functionality
	var context = document.getElementById('canvas').getContext("2d");
	var small_context = document.getElementById("small-canvas").getContext("2d");
	// attach the necessay variables and function to the JQuery global scope so that
	// these are accessible in button-logic.js
	$.context = context;
	$.small_context = small_context;
	$.colorToGrayscale = colorToGrayscale
	var clickX = new Array();    // The clicked x positions
	var clickY = new Array();    // The clicked y positions
	var clickDrag = new Array(); // The dragged position from the clicked x, y position
	
	
	// The boolean paint will let us know if the virtual marker is pressing down on the paper 
	// or not. If paint is true, then we record the value. Then redraw.
	var paint;

	function addClick(x, y, dragging) {
		// console.log('In addClick:' + '('+ x + ',' + y + ')' + " with dragging as " + dragging);
		clickX.push(x);
		clickY.push(y);
		clickDrag.push(dragging); // draging is a boolean
	}
	
	/*  ----------- brush image start ------------- */
	/* var brush = new Image();
	brush.src = "brush2.png";
	var halfBrushW = brush.width/2;
	var halfBrushH = brush.height/2;
	var Trig = {
		distanceBetween2Points: function ( point1, point2 ) {
			var dx = point2.x - point1.x;
			var dy = point2.y - point1.y;
			return Math.sqrt( Math.pow( dx, 2 ) + Math.pow( dy, 2 ) );
		},

		angleBetween2Points: function ( point1, point2 ) {
			var dx = point2.x - point1.x;
			var dy = point2.y - point1.y;
			return Math.atan2( dx, dy );
		}
	}
	function drawBrush(startPt, endPt) {
		var distance = parseInt(Trig.distanceBetween2Points(startPt, endPt) );
		var angle = Trig.angleBetween2Points(startPt, endPt);
		var x,y;
		for ( var z=0; (z<=distance || z==0); z++ ) {
			x = startPt.x + (Math.sin(angle) * z) - halfBrushW;
			y = startPt.y + (Math.cos(angle) * z) - halfBrushH;
			context.drawImage(brush, x, y);
		}
	} */
	/*  ----------- brush image end ------------- */
	
	function redraw(){
		context.clearRect(0, 0, context.canvas.width, context.canvas.height); // Clears the canvas
		/* ---- Ordinary Brush ----- */
		context.strokeStyle = "#008C23";
		context.lineJoin = "round";
		context.lineWidth = 12;
		for(var i=0; i < clickX.length; i++) {		
			context.beginPath();
			if(clickDrag[i] == true && i != 0) {
				// This is when the dragging occurs.
				// We then connect from previous point (clickX[i-1], clickY[i-1]) to the recent 
				// (clickX[i], clickY[i]) point
				context.moveTo(clickX[i-1], clickY[i-1]);
			}else{
				// This is when the mouse down event first occurs, clickDrag will be undefined.
				// Since there will be no path if we draw from the same point to the point
				// itself, so we give a tiny offset for the starting point in order to construct
				// a path. In simpler term, this is for a dot. 
				context.moveTo(clickX[i]-1, clickY[i]);
			}
			context.lineTo(clickX[i], clickY[i]);
			context.closePath();
			context.stroke();
		}
		
		/* ------ Use brush image -------*/
		/*
		var startPt = {};
		var endPt = {};
		for(var i=0; i < clickX.length; i++) {	
			if(clickDrag[i] && i){
				startPt['x'] = clickX[i-1];
				startPt['y'] = clickY[i-1];
			}else{
				startPt['x'] = clickX[i] - 1;
				startPt['y'] = clickY[i];
			}
			endPt['x'] = clickX[i];
			endPt['y'] = clickY[i];
			drawBrush(startPt, endPt);
		}
		*/
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
		// console.log(e.type + ':' + '('+ mouseX + ',' + mouseY + ')' + " with paint as " + paint);
		addClick(mouseX, mouseY);
		redraw();
	});
	
	$('#canvas').mousemove(function(e){
		var mouseX = e.pageX - this.offsetLeft;
		var mouseY = e.pageY - this.offsetTop;
		// console.log(e.type + ':' + '('+ mouseX + ',' + mouseY + ')' + " with paint as " + paint);
		// Only record location when mouse is down, i.e. paint is true
		if(paint == true){
			addClick(mouseX, mouseY, true);
			redraw();
		}
	});
	
	$('#canvas').mouseup(function(e){
		// console.log(e.type);
		// Set paint to false to notify that drawing is done
		paint = false;
	});
	
	$('.button-clear').click(function(e) {
		clickX = new Array();
		clickY = new Array();
		clickDrag = new Array();
		clickColor = new Array();
		clearCanvas();
	});
});