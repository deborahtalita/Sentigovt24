jQuery(document).ready(function () {
    var dateStart = jQuery("#date-start");
    var dateEnd = jQuery("#date-end");

    dateStart.datepicker({
        maxDate: "15",
        dateFormat: "mm/dd/yy",
        onSelect: function (selectedDate) {
            var selected = jQuery(this).datepicker("getDate");
            selected.setDate(selected.getDate() + 7); // Menambahkan 7 hari dari tanggal yang dipilih
            dateEnd.datepicker("option", "maxDate", selected); // Mengatur tanggal maksimal pada date end
        },
        beforeShowDay: function (date) {
            var today = new Date();
            today.setHours(0, 0, 0, 0);
            return [date <= today];
        }
    });

    dateEnd.datepicker({
        maxDate: "15",
        dateFormat: "mm/dd/yy",
        onSelect: function (selectedDate) {
            var selected = jQuery(this).datepicker("getDate");
            selected.setDate(selected.getDate() - 7); // Mengurangi 7 hari dari tanggal yang dipilih
            dateStart.datepicker("option", "maxDate", selected); // Mengatur tanggal maksimal pada date start
        },
        beforeShowDay: function (date) {
            var today = new Date();
            today.setHours(0, 0, 0, 0);
            return [date <= today];
        }
    });
});

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

// Fungsi untuk mengambil data dengan AJAX menggunakan getJSON
function getDataDashboard(id, page) {
    // var id = getSelectedBacapresOption();
    // $.getJSON(`/sentiment/getTweets?bacapres=${id}&page=${page}`, function (response) {
    $.getJSON(`/sentiment/getTweetList?bacapres=${id}&page=${page}`, function (response) {
        
        var currentPage = page;

        // Untuk menghitung index per tweet
        var startIndex = 10 * (currentPage - 1) + 1 ;
        var counter = 0;
        // Mendefinisikan jumlah maksimum tombol halaman yang ditampilkan sekaligus
        const maxVisibleButtons = 5;

        // Mendapatkan data dari response
        const data = response.results;
        const totalPages = response.total_pages;

        // Menampilkan data di tabel
        const tableBody = $("#table-body");
        tableBody.empty();
        for (let i = 0; i < data.length; i++) {
            let bgColor = "";
            if (data[i].sentiment === "positive") {
                bgColor = "bg-green-300";
            } else if (data[i].sentiment === "neutral") {
                bgColor = "bg-gray-300";
            } else if (data[i].sentiment === "negative") {
                bgColor = "bg-red-300";
            }

            index = startIndex + counter;

            const row = `<tr class="border-b">
            <th scope="row" class="font-[Inter-Semibold] text-[12px] px-6 py-4 text-center font-medium text-gray-900">
                ${index}
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
            counter= counter + 1
        }

        // Menghapus tombol halaman sebelumnya dan nomor halaman
        $(".page-button").remove();

        // Event listener untuk tombol nomor halaman
        $(document).on("click", ".page-button", function () {
            const page = parseInt($(this).text());
            if (page !== currentPage) {
                currentPage = page;
                getDataDashboard(id, currentPage);
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
                getDataDashboard(id, currentPage);
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

// function menampilkan jumlah tweet dan sentiment
let currentTotal = null;
function displayTotalTweet(Id) {
    if (currentTotal) {
        delete currentTotal;
    }
    currentTotal = Id;
    $.getJSON(`/sentiment/getTotalTweet?bacapres=${currentTotal}`, function (response) {
        // Menampilkan data total tweet
        document.getElementById("total-display").innerText = response.bacapres_total_tweet;
        // Menampilkan data sentiment negative
        document.getElementById("total-negative").innerText = response.bacapres_total_sentiment['negative'];
        // Menampilkan data sentiment positive
        document.getElementById("total-positive").innerText = response.bacapres_total_sentiment['positive'];
        // Menampilkan data sentiment neutral
        document.getElementById("total-neutral").innerText = response.bacapres_total_sentiment['neutral'];
    })
}

document.addEventListener("DOMContentLoaded", async () => {
    let currentPage = 1;
    // Mendefinisikan jumlah maksimum tombol halaman yang ditampilkan sekaligus
    // const taskRanking = () => {
    //     return new Promise((resolve) => {
    //         getDataRanking();
    //         resolve();
    //     })
    // }
    const displayTrenTotal = () => {
        return new Promise((resolve) => {
            displayChartTotal();
            resolve();
        })
    }

    function getDataRanking() {
        $.getJSON(`/sentiment/getBacapresRanking`, function (response) {
            // Mendapatkan data dari response
            const data = response.results;
    
            // Menampilkan data di tabel
            const buttonContainerRanking = $("#buttonContainerRanking");
            buttonContainerRanking.empty();
    
            // Tambahkan event listener pada dropdown sort
            $("#dropdownSort").on("change", function() {
                const selectedSort = $(this).val();
                console.log(selectedSort)
    
                // Lakukan pengurutan sesuai dengan pilihan yang dipilih
                if (selectedSort === "abjad") {
                    data.sort((a, b) => a.name.localeCompare(b.name));
                } else if (selectedSort === "topPositive") {
                    data.sort((a, b) => b.positive - a.positive);
                } else if (selectedSort === "topNegative") {
                    data.sort((a, b) => b.negative - a.negative);
                }
    
                // Tampilkan data yang sudah diurutkan
                renderData(data, selectedSort);
            });
    
            // Render data awal
            data.sort((a, b) => a.name.localeCompare(b.name));
            renderData(data, "abjad");
        });
    }
    
    function renderData(data, selectedSort) {
        const buttonContainerRanking = $("#buttonContainerRanking");
        buttonContainerRanking.empty();
        console.log(selectedSort)
    
        for (let i = 0; i < data.length; i++) {
            const isActive = i == 0; // Menandai button pertama sebagai aktif
            const activeClass = isActive ? "bg-[#554fff] hover:bg-[#554fff] text-white" : ""; // Menambahkan kelas "active" jika button aktif

            const row = `
                <button title="buttonRankingBacapres" id="buttonRanking-${data[i].id}" data-id="${data[i].id}" class="rankingButton my-2 flex items-center w-full px-5 py-2 hover:bg-gray-100 focus:outline-none rounded-lg justify-between ${activeClass}">
                    <div class="flex items-center gap-2">
                        <img class="object-cover w-8 h-8 rounded-full" src="${data[i].img_bacapres}" alt="Photo Bacapres">
                        <h1 class="font-[poppins-regular] text-[12px] capitalize">${data[i].name}</h1>
                    </div>
                    <div class="font-[poppins-bold] text-[12px] flex gap-4">
                    ${selectedSort === "abjad" ? '<div></div>' : ''}
                    ${selectedSort === "topPositive" ? `<div class="text-[#05FF00]">${data[i].positive}</div>` : ''}
                    ${selectedSort === "topNegative" ? `<div class="text-[#FF0000]">${data[i].negative}</div>` : ''}
                    </div>
                </button>
                <hr>`;
            buttonContainerRanking.append(row);
    
            // Tambahkan event listener pada setiap button
            $(`#buttonRanking-${data[i].id}`).on("click", function() {
                // Hapus kelas "active" dari button sebelumnya
                $(".rankingButton").removeClass("bg-[#554fff] hover:bg-[#554fff] text-white");
                // Tambahkan kelas "active" pada button yang baru dipilih
                $(this).addClass("bg-[#554fff] hover:bg-[#554fff] text-white");
                displayTotalTweet(data[i].id);
                var chartType = getCurrentChartType();
                console.log(chartType)
                displayChart(chartType, data[i].id);
                getDataDashboard(data[i].id, 1)
            });
            // Setel nilai ID aktif sebagai argumen default untuk displayTotalTweet
            if (isActive) {
                var chartType = getCurrentChartType();
                displayChart(chartType, data[i].id);
                displayTotalTweet(data[i].id);
                getDataDashboard(data[i].id, 1)
            }
        }
    }

    // Mengambil data saat halaman dimuat
    getDataRanking();
    // await taskRanking();
    await displayTrenTotal();
    
    // Event listener untuk tombol sebelumnya
    $("#prev-button").on("click", function () {
        if (currentPage > 1) {
            currentPage--;
            getDataDashboard(id, currentPage);
        }
    });

    // Event listener untuk tombol selanjutnya
    $("#next-button").on("click", function () {
        currentPage++;
        getDataDashboard(id, currentPage);
    });
});

// function untuk menambahkan event listener pada chart-button dgn tetap terkait dengan rankingButton
document.querySelectorAll(".chart-button").forEach(function(button) {
    button.addEventListener("click", function() {
        var chartType = button.getAttribute("id");
        console.log("chart-button",chartType)
        var displayOption = getSelectedBacapresOption();
        console.log("display-option",displayOption)
        displayChart(chartType, displayOption);
    });
});

// function mengambil id untuk Type Chart
function getCurrentChartType() {
    var activeButton = document.querySelector(".chart-button.activeTren");
    return activeButton ? activeButton.getAttribute("id") : null;
}

// funtion untuk mengambil data-id pada rankingButton dengan class active
function getSelectedBacapresOption() {
    $(".rankingButton").each(function() {
        if ($(this).hasClass("bg-[#554fff] hover:bg-[#554fff] text-white")) {
          currentButtonId = $(this).data("id");;
          return false; // Exit the loop after finding the first matching element
        }
      });
    
      return currentButtonId;
}

// Variabel menyimpan temporary data dari Chart
let currentChart = null;
// Variabel menyimpan temporary data-id dari Chart
let currentId = null;

// Grafik Tren
function displayChart(chartId, Id) {
    if (currentId && currentChart) {
        delete currentId;
        currentChart.destroy();
    }

    currentId = Id;
    console.log(currentId);

    if (chartId === 'chart-button1') {
        // Membuat grafik 1
        $.getJSON(`/sentiment/getTrenTotalSentiment?bacapres=${Id}`, function (response) {
            var options = {
                chart: {
                    width: "100%",
                    height: "90%",
                    type: "area",
                },
                dataLabels: {
                    enabled: false
                },
                series: response.total_sentiment_per_day,
                stroke: {
                    width: [2, 2, 2], // mengatur lebar garis
                },
                fill: {
                    type: "gradient",
                    gradient: {
                        shadeIntensity: 1,
                        opacityFrom: 0,
                        opacityTo: 0,
                        stops: [0, 90, 100]
                    }
                },
                xaxis: {
                    categories: response.dates
                },
                colors: ['#FF0000', '#00FF0A', '#7B7B7B'],
                strokeColors: ['#FF0000', '#00FF0A', '#7B7B7B'],
            };
            const chart1 = new ApexCharts(document.getElementById('chart-display'), options);
            chart1.render();
            currentChart = chart1;
        })
    } else if (chartId === 'chart-button2') {
        // Membuat grafik 2
        $.getJSON(`/sentiment/getTrenTotalSentiment?bacapres=${Id}`, function (response) {
            var options = {
                series: response.total_sentiment_per_day,
                chart: {
                    type: 'bar',
                    width: "100%",
                    height: "90%",
                    stacked: true,
                },
                plotOptions: {
                    bar: {
                        horizontal: true,
                        dataLabels: {
                            total: {
                                enabled: true,
                                offsetX: 0,
                                style: {
                                    fontSize: '13px',
                                    fontWeight: 900
                                }
                            }
                        }
                    },
                },
                colors: ['#FF0000', '#00FF0A', '#7B7B7B'],
                stroke: {
                    width: 2,
                    colors: ['#fff']
                },
                xaxis: {
                    categories: response.dates,
                    labels: {
                        formatter: function (val) {
                            return val
                        }
                    }
                },
                yaxis: {
                    title: {
                        text: undefined
                    },
                },
                tooltip: {
                    y: {
                        formatter: function (val) {
                            return val
                        }
                    }
                },
                fill: {
                    opacity: 1
                },
                legend: {
                    position: 'top',
                    horizontalAlign: 'left',
                    offsetX: 40
                }
            };
            const chart2 = new ApexCharts(document.getElementById('chart-display'), options);
            chart2.render();
            currentChart = chart2;
        })
    }

    const buttons = document.querySelectorAll('.chart-button');
    buttons.forEach(button => {
        button.classList.remove('activeTren');
        if (button.id === chartId) {
            button.classList.add('activeTren');
        }
    });
}

// Grafik Tren All Tweet
function displayChartTotal() {
    $.getJSON("/sentiment/getTrenTotalTweet/", function (response) {
        var options = {
            chart: {
                width: "100%",
                height: "90%",
                type: "area",
            },
            dataLabels: {
                enabled: false
            },
            series: response.bacapres_total_tweet_per_day,
            fill: {
                type: "gradient",
                gradient: {
                    shadeIntensity: 1,
                    opacityFrom: 0,
                    opacityTo: 0,
                    stops: [0, 90, 100]
                }
            },
            stroke: {
                width: 2,
            },
            xaxis: {
                categories: response.dates,
            },
        };
        const chart = new ApexCharts(document.querySelector("#chart-display-Total"), options);
        chart.render();
    })  
}

document.addEventListener("DOMContentLoaded", function () {
    // displayChartTotal();
});

const csvButton = document.getElementById('generateCSV');
csvButton.addEventListener('click', function() {
    // Make the AJAX request using getJSON
    var id = getSelectedBacapresOption();
    var xhr = new XMLHttpRequest();
    xhr.open('GET', `/sentiment/generateCSV?bacapres=${id}`, true);
    xhr.responseType = 'blob';

    xhr.onload = function() {
        if (xhr.status === 200) {
            // Create a download link for the CSV file
            var downloadLink = document.createElement('a');
            downloadLink.href = window.URL.createObjectURL(xhr.response);
            downloadLink.download = 'data.csv';
            downloadLink.click();
        }
    };

    xhr.send();
  });