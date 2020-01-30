$(document).ready(function(){
	$(".btn").click(function(){
		alert("Downloaded Successfully");
	});
});


$(document).ready(function(){
	$(".datepicker").datepicker({
		dateFormat: "yy-mm-dd",
		changeMonth: true,
		changeYear: true
	});
});