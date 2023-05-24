

document.addEventListener('DOMContentLoaded', function () {
    var myButton = document.getElementById('btn-delete-User');

    myButton.addEventListener('click', function () {
        Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
        }).then((result) => {
            if (result.isConfirmed) {
                Swal.fire(
                    'Deleted!',
                    'Your file has been deleted.',
                    'success'
                )
            }
        })
    });
});

document.addEventListener('DOMContentLoaded', function () {
    var myButton = document.getElementById('btn-delete-history');

    myButton.addEventListener('click', function () {
        Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
        }).then((result) => {
            if (result.isConfirmed) {
                Swal.fire(
                    'Deleted!',
                    'Your file has been deleted.',
                    'success'
                )
            }
        })
    });
});

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