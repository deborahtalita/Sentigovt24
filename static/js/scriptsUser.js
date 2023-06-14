document.addEventListener("DOMContentLoaded", function () {
    let currentPage = 1;

    // Mengambil data saat halaman dimuat
    getDataUser(currentPage);

    // Event listener untuk tombol sebelumnya
    $("#prev-button").on("click", function () {
        if (currentPage > 1) {
            currentPage--;
            getDataUser(currentPage);
        }
    });

    // Event listener untuk tombol selanjutnya
    $("#next-button").on("click", function () {
        currentPage++;
        getDataUser(currentPage);
    });
});

// Fungsi untuk mengambil data dengan AJAX menggunakan getJSON
function getDataUser(page) {
    // Mendefinisikan jumlah maksimum tombol halaman yang ditampilkan sekaligus
    const maxVisibleButtons = 5;

    const searchQuery = document.getElementById('searchQuery').value;
    console.log(searchQuery)
    let url = `/account?page=${page}`

    if (searchQuery) {
        url += '&search=' + encodeURIComponent(searchQuery);
    }

    $.getJSON(url, function (response) {
        // Mendapatkan data dari response
        const data = response.results;
        const totalPages = response.total_pages;

        var currentPage = page;

        // Untuk menghitung index per tweet
        var startIndex = 10 * (currentPage - 1) + 1;
        var counter = 0;

        // Menampilkan data di tabel
        const tableBody = $("#table-body");
        tableBody.empty();

        for (let i = 0; i < data.length; i++) {
            console.log(data[i])
            index = startIndex + counter;
            const row = `<tr class="border-b">
            <th scope="row" class="font-[Inter-Semibold] text-[12px] px-6 py-4 text-center font-medium text-gray-900">
                ${index}
            </th>
            <td class="font-[Inter-Regular] text-[12px] text-black mx-10 py-4 whitespace-nowrap text-center">
                ${data[i].name}
            </td>
            <td class="font-[Inter-Regular] text-[12px] text-black py-4 whitespace-nowrap text-center">
                ${data[i].role}
            </td>
            <td class="font-[Inter-Regular] text-[12px] py-4 ">
                <a data-id="${data[i].id}" id="btn-delete-User" class="flex justify-center" href="#"><img src="/static/media/icons/btn-delete.svg" alt="Delete"></a>
            </td>
            <td class="font-[Inter-Regular] text-[12px] px-6 py-4">
                <a class="flex justify-center w-20 sm:w-full" href="account/${data[i].id}/edit"><img src="/static/media/icons/btn-edit.svg" alt="Edit"></a>
            </td>
        </tr>`;
            tableBody.append(row);
            counter = counter + 1
        }

        // Menghapus tombol halaman sebelumnya dan nomor halaman
        $(".page-button").remove();

        // Event listener untuk tombol nomor halaman
        $(document).on("click", ".page-button", function () {
            const page = parseInt($(this).text());
            if (page !== currentPage) {
                currentPage = page;
                getDataUser(currentPage);
            }
        });

        // Membuat tombol nomor halaman
        const pageButtons = $("#page-buttons");
        let startPage = Math.max(1, currentPage - Math.floor(maxVisibleButtons / 2));
        let endPage = Math.min(totalPages, startPage + maxVisibleButtons - 1);

        if (endPage - startPage + 1 < maxVisibleButtons) {
            startPage = Math.max(1, endPage - maxVisibleButtons + 1);
        }

        for (let i = startPage; i <= endPage; i++) {
            const button = `<button class="page-button font-[Inter-Regular] mx-1 px-2 py-1 text-sm text-gray-500 rounded-md hover:bg-gray-400 hover:text-white">${i}</button>`;
            pageButtons.append(button);
        }

        // Menambahkan tombol ellipsis di awal jika halaman awal tidak terlihat
        if (startPage > 1) {
            const ellipsisStart = `<button class="page-button font-[Inter-Regular] mx-1 px-2 py-1 text-sm text-gray-500 rounded-md" disabled>...</button>`;
            pageButtons.prepend(ellipsisStart);
        }

        // Menambahkan tombol ellipsis di akhir jika halaman akhir tidak terlihat
        if (endPage < totalPages) {
            const ellipsisEnd = `<button class="page-button font-[Inter-Regular] mx-1 px-2 py-1 text-sm text-gray-500 rounded-md" disabled>...</button>`;
            pageButtons.append(ellipsisEnd);
        }

        // Menambahkan event listener untuk tombol nomor halaman
        $(".page-button").on("click", function () {
            const page = parseInt($(this).text());
            if (page !== currentPage) {
                currentPage = page;
                getDataUser(currentPage);
                // Menghapus kelas "active" dari semua tombol halaman
                $(".page-button").removeClass("activePagination");
                // Menambahkan kelas "active" pada tombol halaman yang dipilih
                $(this).addClass("activePagination");
            }
        });

        // Mengatur status button prev dan next berdasarkan halaman saat ini
        $("#prev-button").prop("disabled", currentPage === 1);
        $("#next-button").prop("disabled", currentPage === totalPages);

        // Menghapus kelas "active" dari semua tombol halaman
        $(".page-button").removeClass("activePagination");
        // Menambahkan kelas "active" pada tombol halaman saat ini
        $(`.page-button:contains(${currentPage})`).addClass("activePagination");
    });

    // Menambahkan event listener untuk tombol delete
    $(document).on("click", "#btn-delete-User", function (event) {
        event.preventDefault(); // Mencegah aksi default dari link
        const deleteButton = $(this);
        const id = deleteButton.data('id');
        // Tampilkan dialog konfirmasi SweetAlert2
        Swal.fire({
            title: "Are you sure?",
            text: "You won't be able to revert this!",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: "Yes, delete it!",
        }).then((result) => {
            if (result.isConfirmed) {
                const url = `/account/${id}/delete`; // Ganti yourDataId dengan ID data yang ingin dihapus
                // Hapus baris dari tabel setelah penghapusan berhasil
                $.ajax({
                    url: url,
                    type: "POST",
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    success: function (response) {
                        Swal.fire({
                            icon: 'success',
                            title: 'Deleted!',
                            text: 'Your data has been deleted.',
                            showConfirmButton: false,
                            timer: 1500
                        });
                        setTimeout(function () {
                            // Reload the current page
                            location.reload();
                        }, 3000);
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
}

document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("updateRole");

    form.addEventListener("submit", function (e) {
        e.preventDefault(); // Prevent default form submission

        var url = form.action;
        var formData = new FormData(form);

        fetch(url, {
                method: "POST",
                body: formData
            })
            .then(function (response) {
                if (response.status === 400) {
                    return response.json();
                } else {
                    Swal.fire({
                        icon: 'success',
                        title: 'User role already updated!',
                        showConfirmButton: false,
                        timer: 1500
                    });
                    setTimeout(function () {
                        // Reload the current page
                        window.location.href = '/account'
                    }, 2000);
                }
            })
            .then(function (errors) {})
            .catch(function (error) {
                // Handle network or other errors
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