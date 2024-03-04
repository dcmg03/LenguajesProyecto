// login.js

$("#loginForm").submit(function(e) {

  e.preventDefault();

  var formData = {
    username: $("#loginForm input[name='username']").val(),
    password: $("#loginForm input[name='password']").val()
  };

  $.ajax({
    type: "POST",
    url: "/login",
    data: formData,
    success: function(response) {
      console.log("Login exitoso");
      window.location.href = "/profile";
    },
    error: function(error) {
      console.log("Login fallido", error);
    }
  });

});