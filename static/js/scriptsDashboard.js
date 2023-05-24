const buttonsRanking = document.querySelectorAll('.rankingButton');

// Active Button Ranking
buttonsRanking.forEach(button => {
    button.addEventListener('click', () => {
        buttonsRanking.forEach(btn => {
            btn.classList.remove('activeRanking');
        });
        button.classList.add('activeRanking');
    });
});

// Multi Select
function dropdown() {
    return {
        options: [],
        selected: [],
        show: false,
        open() {
            this.show = true
        },
        close() {
            this.show = false
        },
        isOpen() {
            return this.show === true
        },
        select(index, event) {
            if (!this.options[index].selected) {
                this.options[index].selected = true;
                this.options[index].element = event.target;
                this.selected.push(index);

            } else {
                this.selected.splice(this.selected.lastIndexOf(index), 1);
                this.options[index].selected = false
            }
        },
        remove(index, option) {
            this.options[option].selected = false;
            this.selected.splice(index, 1);

        },
        loadOptions() {
            const options = document.getElementById('select').options;
            for (let i = 0; i < options.length; i++) {
                this.options.push({
                    value: options[i].value,
                    text: options[i].innerText,
                    selected: options[i].getAttribute('selected') != null ? options[i].getAttribute('selected') : false
                });
            }

        },
        selectedValues() {
            return this.selected.map((option) => {
                return this.options[option].value;
            })
        }
    }
}

document.addEventListener("DOMContentLoaded", function () {
    let currentPage = 1;
    // Mendefinisikan jumlah maksimum tombol halaman yang ditampilkan sekaligus
    const maxVisibleButtons = 5;

    // Fungsi untuk mengambil data dengan AJAX menggunakan getJSON
    function getDataDashboard(page) {
        $.getJSON(`/get-data-table-dashboard/?page=${page}`, function (response) {
            // Mendapatkan data dari response
            const data = response.results;
            const totalPages = response.total_pages;

            // Menampilkan data di tabel
            const tableBody = $("#table-body");
            tableBody.empty();
            for (let i = 0; i < data.length; i++) {
                let bgColor = "";
                if (data[i].sentiment === "Positive") {
                    bgColor = "bg-green-300";
                } else if (data[i].sentiment === "Neutral") {
                    bgColor = "bg-gray-300";
                } else if (data[i].sentiment === "Negative") {
                    bgColor = "bg-red-300";
                }

                const row = `<tr class="border-b">
                <th scope="row" class="font-[Inter-Semibold] text-[12px] px-6 py-4 text-center font-medium text-gray-900">
                    ${data[i].no}
                </th>
                <td class="font-[Inter-Regular] text-[12px] text-black mx-10 py-4 whitespace-nowrap text-center">
                    ${data[i].name}
                </td>
                <td class="font-[Inter-Regular] text-[12px] text-black px-10 py-4 whitespace-normal text-justify">
                    ${data[i].tweet}
                </td>
                <td class="font-[Inter-Regular] text-[12px] text-black py-4 text-center ">
                    <div class="${bgColor} p-1 rounded-full">
                        ${data[i].sentiment}
                    </div>
                </td>
                <td class="font-[Inter-Regular] text-[12px] text-black px-6 py-4 text-center">
                    ${data[i].date}
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
                    getDataDashboard(currentPage);
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
                    getDataDashboard(currentPage);
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
    }

    // Mengambil data saat halaman dimuat
    getDataDashboard(currentPage);

    // Event listener untuk tombol sebelumnya
    $("#prev-button").on("click", function () {
        if (currentPage > 1) {
            currentPage--;
            getDataDashboard(currentPage);
        }
    });

    // Event listener untuk tombol selanjutnya
    $("#next-button").on("click", function () {
        currentPage++;
        getDataDashboard(currentPage);
    });
});