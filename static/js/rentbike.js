
function popup(){

	$("#fade").slideDown("slow", function () {
		$("#container").fadeIn("slow");
	});
}

$(document).ready(function(){
	$("#rent-bike").click(function(){
		$("#popUpMessage").text("You have successfully rented the bike");


		popup();
	});

	$("#return-bike").on("click", function () {
		$("#popUpMessage").text("You have successfully returned the bike");
		popup();
	});

	$("#report-bike").on("click", function () {
		$("#popUpMessage").text("You have successfully reported the bike");
		popup();
	});

	$("#out").click(function(){

		$(".container").fadeOut("slow", function () {
			$(".fade").slideUp("slow");
		});

	});
});