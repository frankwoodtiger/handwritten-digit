$(function() {
	// The DOM is ready!
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