$(document).ready(function(){
	$("#btn1").click(function(){
		alert("Password Changed Successfully");
	});

	//$("#btn2").click(function(){
	//	alert("Account Closed Successfully");
	//});

	$("#show").click(function(){
		$("#show").removeClass("far fa-eye-slash").addClass("far fa-eye");
		if($(".pwd").attr("type") === "password"){
			$("#show").removeClass("far fa-eye-slash").addClass("far fa-eye");
			$(".pwd").attr("type","text");
		}
		else{
			$("#show").removeClass("far fa-eye").addClass("far fa-eye-slash");
			$(".pwd").attr("type","password");
		}
	});

	$("#show1").click(function(){
		$("#show1").removeClass("far fa-eye-slash").addClass("far fa-eye");
		if($(".pwd").attr("type") === "password"){
			$("#show1").removeClass("far fa-eye-slash").addClass("far fa-eye");
			$(".pwd").attr("type","text");
		}
		else{
			$("#show1").removeClass("far fa-eye").addClass("far fa-eye-slash");
			$(".pwd").attr("type","password");
		}
	});

	$("#show2").click(function(){
		$("#show2").removeClass("far fa-eye-slash").addClass("far fa-eye");
		if($(".pwd").attr("type") === "password"){
			$("#show2").removeClass("far fa-eye-slash").addClass("far fa-eye");
			$(".pwd").attr("type","text");
		}
		else{
			$("#show2").removeClass("far fa-eye").addClass("far fa-eye-slash");
			$(".pwd").attr("type","password");
		}
	});

    // Attach a submit handler to the form
    $( "#updateprofile" ).submit(function( event ) {
		// Stop form from submitting normally
		event.preventDefault();
		$.ajax({
			  type:'POST',
			  url: '/api/updateprofile',
			  data: JSON.stringify({
				  fname: $('#fname').val(),lname: $('#lname').val(),phone: $('#phone').val(),
				  email: $('#email').val(),address: $('#address').val(),pincode: $('#pincode').val(),
				  city: $('#city').val(),country: $('#country').val()
				}),
			  success: function(data){ alert(data.retstatus)  ;},
			  contentType: "application/json",
			  dataType: 'json'
		});
  
	  });	

    // Attach a submit handler to the form
    $( "#updatecardinfo" ).submit(function( event ) {
		// Stop form from submitting normally
		event.preventDefault();
		$.ajax({
			  type:'POST',
			  url: '/api/updatecardinfo',
			  data: JSON.stringify({
				  cnum: $('#cnum').val(),cname: $('#cname').val(),cvv: $('#cvv').val(),
				  exp_mm: $('#exp_mm').val(),exp_yy: $('#exp_yy').val()
				}),
			  success: function(data){alert(data.retstatus)  ;},
			  contentType: "application/json",
			  dataType: 'json'
		});
  
	  });
	  
    // Attach a submit handler to the form
    $( "#closeuseraccount" ).submit(function( event ) {
		// Stop form from submitting normally
		event.preventDefault();
		$.ajax({
			  type:'POST',
			  url: '/api/closeuseraccount',
			  data: JSON.stringify({
				ca_email: $('#ca_email').val()
				}),
			  success: function(data){alert(data.retstatus) ;},
			  contentType: "application/json",
			  dataType: 'json'
		});
  
	  });
});

