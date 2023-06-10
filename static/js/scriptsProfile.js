function changePassword() {
    document.getElementById("changePassword").classList.toggle("active");
    $('body').addClass('overflow-hidden');
}

function closeModal() {
    $('body').removeClass('overflow-hidden');
}

document.addEventListener("DOMContentLoaded", function() {
    var popupContainer = document.getElementById("popup");
    var openPopupButton = document.getElementById("popup-password");
    var form = document.getElementById("change-password");
  
    form.addEventListener("submit", function(e) {
      e.preventDefault();  // Prevent default form submission
  
      var url = form.action;
      var formData = new FormData(form);
  
      fetch(url, {
        method: "POST",
        body: formData
      })
      .then(function(response) {
        if (response.status === 400) {
          return response.json();
        } else {
            window.location.href = 'profile'
        }
      })
      .then(function(errors) {
        document.getElementById("old_password_err").innerText = ""
        document.getElementById("new_password2_err").innerText = ""
        document.getElementById("new_password1_err").innerText = ""
        
        if (errors.hasOwnProperty('old_password')){
            document.getElementById("old_password_err").innerText = errors.old_password[0].message
        }
        if (errors.hasOwnProperty('new_password2')) {
            document.getElementById("new_password2_err").innerText = errors.new_password2[0].message
        }
        if (errors.hasOwnProperty('new_password1')){
            document.getElementById("new_password1_err").innerText = errors.new_password1[0].message
        }
      })
      .catch(function(error) {
        // Handle network or other errors
      });
    });
});
  