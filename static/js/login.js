function login(){
    let email = $('#emailLogin').val();
    let password = $('#password').val();

    if (email === ""){
        alert("Email can not be empty");
        return 0;
    }else if(password === ""){
        alert("Password can not be empty");
        return 0;
    }else{
        //window.location.href = "../../project/index.html";
        return 1;
    }
}

function signup(){
    let email = $('#emailSignup').val();
    let firstName = $('#firstName').val();
    let surname = $('#surname').val();
    let password = $('#passwordSignup').val();
    let passwordConfirm = $('#passwordConfirm').val();

    if (email === ""){
        alert("Email can not be empty");
        return 0;
    }else if(firstName === ""){
        alert("First name can not be empty");
        return 0;
    }else if(surname === ""){
        alert("Surname can not be empty");
        return 0;
    }else if(password < 8){
        alert("Password can not be less than 8 characters long");
        return 0;
    }else if(password !== passwordConfirm){
        alert("Passwords do not match");
        return 0;
    }else{
        //alert("You have signed up! Now Login!");
        return 1;
    }
}

$(document).ready(function () {

    $("#openSignup").on("click", function () {
        $("#loginForm").fadeOut('fast', function () {
            $('#signupForm').fadeIn();
        });

    });

    $('#openLogin').on('click', function () {
       $('#signupForm').fadeOut('fast', function () {
          $('#loginForm').fadeIn();
       });
    });

    //$('#loginButton').on('click', function () {
    //    login();
    //});

    //$('#signupButton').on('click', function () {
    //   signup();
    //});

    // Attach a submit handler to the form
    $( "#loginButton" ).click(function( event ) {
		// Stop form from submitting normally
        event.preventDefault();
        if (login() == 0)
            return;
        else{
            $.ajax({
                type:'POST',
                url: '/api/dologin',
                data: JSON.stringify({
                    emailLogin: $('#emailLogin').val(), password :$('#password').val()
                    }),
                success: function(data){ 
                    if (data.token == ''){
                    alert(data.retstatus) ;
                    }else{
                        var form = $('<form action="' + '/Home' + '" method="get">' +
                        '<input type="text" name="token" value="' + data.token + '" />' +
                        '</form>');
                        $('body').append(form);
                        form.submit();
                    };
                },
                contentType: "application/json",
                dataType: 'json'
            });
        }
      });
      
      $( "#signupButton" ).click(function( event ) {
		// Stop form from submitting normally
        event.preventDefault();
        if (signup() == 0)
            return;
        else{
            $.ajax({
                type:'POST',
                url: '/api/doregistration',
                data: JSON.stringify({
                    fname: $('#firstName').val(), lname :$('#surname').val(),
                    email: $('#emailSignup').val(), password :$('#passwordSignup').val(),
                    }),
                success: function(data){alert(data.retstatus) ;$('#openLogin').click()},
                contentType: "application/json",
                dataType: 'json'
            });
        }
	  });
});