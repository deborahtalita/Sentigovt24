document.addEventListener("DOMContentLoaded", function () {
    let currentPage = 1;
    // Fungsi untuk mengambil data dengan AJAX menggunakan getJSON
    function getDataUser(page) {
        $.getJSON(`/get-data-table-user/?page=${page}`, function (response) {
            // Mendapatkan data dari response
            const data = response.results;
            const totalPages = response.total_pages;

            // Menampilkan data di tabel
            const tableBody = $("#table-body");
            tableBody.empty();

            for (let i = 0; i < data.length; i++) {
                const row = `<tr class="border-b">
                <th scope="row" class="font-[Inter-Semibold] text-[12px] px-6 py-4 text-center font-medium text-gray-900">
                    ${data[i].no}
                </th>
                <td class="font-[Inter-Regular] text-[12px] text-black mx-10 py-4 whitespace-nowrap text-center">
                    ${data[i].name}
                </td>
                <td class="font-[Inter-Regular] text-[12px] text-black py-4 whitespace-nowrap text-center">
                    ${data[i].status}
                </td>
                <td class="font-[Inter-Regular] text-[12px] py-4 ">
                    <a id="btn-delete-User" class="flex justify-center" href="#"><img src="/static/media/icons/btn-delete.svg" alt="Delete"></a>
                </td>
                <td class="font-[Inter-Regular] text-[12px] px-6 py-4">
                    <a class="flex justify-center" href="{% url 'editUser' %}"><img src="/static/media/icons/btn-edit.svg" alt="Edit"></a>
                </td>
            </tr>`;
                tableBody.append(row);
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
            for (let i = 1; i <= totalPages; i++) {
                const button = `<button class="page-button font-[Inter-Regular] mx-1 px-2 py-1 text-sm text-gray-500 rounded-md hover:bg-gray-400 hover:text-white">${i}</button>`;
                pageButtons.append(button);
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
                    // Hapus baris dari tabel setelah penghapusan berhasil
                    const row = deleteButton.closest("tr");
                    row.remove();

                    Swal.fire(
                        'Deleted!',
                        'Your file has been deleted.',
                        'success'
                    )
                }
            });
        });
    }

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