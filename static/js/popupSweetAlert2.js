document.addEventListener('DOMContentLoaded', function () {
    var myButton = document.getElementById('btn-confirm');

    myButton.addEventListener('click', function () {
        Swal.fire({
            title: 'Are you sure?',
            text: "This will replace the old password",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes!'
        }).then((result) => {
            if (result.isConfirmed) {
                const buttonConfirm = document.querySelectorAll('.changePasswordHidden');
                buttonConfirm.forEach(button => {
                    button.classList.remove('hidden');
                });
            }
        })
    });
});

document.addEventListener('DOMContentLoaded', function () {
    var myButton = document.getElementById('saveCreateBacapres');

    myButton.addEventListener('click', function () {
        Swal.fire({
            icon: 'success',
            title: 'Bacapres has been added',
            showConfirmButton: false,
            timer: 3000
        })
    });
});

document.addEventListener('DOMContentLoaded', function () {
    var myButton = document.getElementById('saveEditBacapres');

    myButton.addEventListener('click', function () {
        Swal.fire({
            icon: 'success',
            title: 'Bacapres has been Edited',
            showConfirmButton: false,
            timer: 1500
        })
    });
});

document.addEventListener('DOMContentLoaded', function () {
    var myButton = document.getElementById('saveEditUser');

    myButton.addEventListener('click', function () {
        Swal.fire({
            icon: 'success',
            title: 'User has been Edited',
            showConfirmButton: false,
            timer: 1500
        })
    });
});

document.addEventListener('DOMContentLoaded', function () {
    var myButton = document.getElementById('deleteAllBacapres');

    myButton.addEventListener('click', function () {
        Swal.fire({
            title: "Are you sure?",
            text: "You won't be able to revert this!",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: "Yes, delete All!",
        }).then((result) => {
            if (result.isConfirmed) {
                const url = `/sentiment/history/delete/all/`;
                $.ajax({
                    url: url,
                    type: "POST",
                    headers: { "X-CSRFToken": getCookie("csrftoken") },
                    success: function (response) {
                        Swal.fire('Deleted!', 'Your data has been deleted.', 'success');
                        location.reload()
                        // Lakukan tindakan tambahan setelah penghapusan data berhasil
                    },
                    error: function (xhr, status, error) {
                        Swal.fire('Error!', 'An error occurred while deleting the data.', 'error');
                        // Lakukan tindakan tambahan jika terjadi kesalahan saat menghapus data
                    }
                });
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    var myButton = document.getElementById('deleteAllHistory');

    myButton.addEventListener('click', function () {
        console.log("deleteAllHistory")
        Swal.fire({
            title: "Are you sure?",
            text: "You won't be able to revert this!",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: "Yes, delete All!",
        }).then((result) => {
            if (result.isConfirmed) {
                const url = `/sentiment/history/delete/all/`;
                $.ajax({
                    url: url,
                    type: "POST",
                    headers: { "X-CSRFToken": getCookie("csrftoken") },
                    success: function (response) {
                        Swal.fire('Deleted!', 'Your data has been deleted.', 'success');
                        setTimeout(function() {
                            // Reload the current page
                            location.reload();
                          }, 1500);
                        // Lakukan tindakan tambahan setelah penghapusan data berhasil
                    },
                    error: function (xhr, status, error) {
                        Swal.fire('Error!', 'An error occurred while deleting the data.', 'error');
                        // Lakukan tindakan tambahan jika terjadi kesalahan saat menghapus data
                    }
                });
            }
        });
    });
});

// Helper function to get the value of a cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        // Check if the cookie name matches the given name
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }