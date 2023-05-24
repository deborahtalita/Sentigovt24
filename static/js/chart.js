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

    if (chartId === 'chart-button1') {
        // Membuat grafik 1
        $.getJSON("/get-data/", function (response) {
            var options = {
                chart: {
                    width: "100%",
                    height: "90%",
                    type: "area",
                },
                dataLabels: {
                    enabled: false
                },
                series: response.series[Id],
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
                    categories: response.dates,
                },
                colors: ['#00FF0A', '#7B7B7B', '#FF0000'],
                strokeColors: ['#00FF0A', '#7B7B7B', '#FF0000'],
            };
            const chart1 = new ApexCharts(document.getElementById('chart-display'), options);
            chart1.render();
            currentChart = chart1;
        })
    } else if (chartId === 'chart-button2') {
        // Membuat grafik 2
        $.getJSON("/get-data/", function (response) {
            var options = {
                series: response.series[Id],
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
                colors: ['#00FF0A', '#7B7B7B', '#FF0000'],
                stroke: {
                    width: 2,
                    colors: ['#fff']
                },
                xaxis: {
                    categories: response.dates,
                    labels: {
                        formatter: function (val) {
                            return val + "K"
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
                            return val + "K"
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

    // ForEach untuk mengaktifkan button Type Chart Tren
    const buttons = document.querySelectorAll('.chart-button');
    buttons.forEach(button => {
        button.classList.remove('activeTren');
        if (button.id === chartId) {
            button.classList.add('activeTren');
        }
    });
}

// Button Event Listener untuk mengganti type Chart
document.querySelectorAll(".chart-button").forEach(function (button) {
    button.addEventListener("click", function () {
        var chartType = button.getAttribute("id");
        var displayOption = getCurrentDisplayOption();
        // Mengambil type yang berbeda
        displayChart(chartType, displayOption);
    });
});

// Button Event Listener untuk mengganti data-id bacapres
document.querySelectorAll(".rankingButton").forEach(function (button) {
    button.addEventListener("click", function () {
        var chartType = getCurrentChartType();
        var displayOption = button.getAttribute("data-id");
        // Mengambil data-id yang baru untuk chart
        displayChart(chartType, displayOption);
        // Mengambil data-id yang baru untuk jumlah tweet dan sentiment
        displayTotalTweet(displayOption)
    });
});

// function mengambil id untuk Type Chart
function getCurrentChartType() {
    var activeButton = document.querySelector(".chart-button.activeTren");
    return activeButton ? activeButton.getAttribute("id") : null;
}

// function mengambil Attribute data-id bacapres
function getCurrentDisplayOption() {
    var activeButton = document.querySelector(".rankingButton.activeRanking");
    return activeButton ? activeButton.getAttribute("data-id") : null;
}

// function menampilkan jumlah tweet dan sentiment
let currentTotal = null;
function displayTotalTweet(Id) {
    if (currentTotal) {
        delete currentTotal;
    }
    currentTotal = Id;
    $.getJSON("/get-data/", function (response) {
        // Menampilkan data total tweet
        document.getElementById("total-display").innerText = response.total_tweet[currentTotal];
        // Menampilkan data sentiment positive
        document.getElementById("total-positive").innerText = response.total_sentiment[currentTotal]['positive'];
        // Menampilkan data sentiment neutral
        document.getElementById("total-neutral").innerText = response.total_sentiment[currentTotal]['neutral'];
        // Menampilkan data sentiment negative
        document.getElementById("total-negative").innerText = response.total_sentiment[currentTotal]['negative'];
    })
}

// Grafik All Tweet
function displayChartTotal() {
    // $.getJSON("/sentiment/getAllTotalTweet/", function (response) { // Tidak bisa karena belum ada
    var options = {
        chart: {
            width: "100%",
            height: "90%",
            type: "area",
        },
        dataLabels: {
            enabled: false
        },
        series: [{
                name: "Airlangga Hartanto",
                data: [45, 52, 38, 45, 19, 40, 47]
            },
            {
                name: "Anies Baswedan",
                data: [100, 67, 38, 80, 19, 30, 79]
            },
            {
                name: "Gajar Pranowo",
                data: [58, 50, 38, 90, 64, 53, 32]
            },
            {
                name: "Khofifah Indar Parawansa",
                data: [70, 102, 38, 20, 70, 23, 20]
            },
            {
                name: "Sandiaga Uno",
                data: [20, 100, 120, 45, 100, 24, 37]
            },
            {
                name: "Prabowo Subianto",
                data: [140, 40, 38, 45, 94, 43, 60]
            },
            {
                name: "Prabowo Subianto",
                data: [140, 40, 38, 45, 94, 43, 60]
            }
        ],
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
        }
    };
    const chart = new ApexCharts(document.querySelector("#chart-display-Total"), options);
    chart.render();
    // })
}

document.addEventListener("DOMContentLoaded", function () {
    // Menampilkan total Tweet
    var idBacapres = getCurrentDisplayOption();
    displayTotalTweet(idBacapres);
});

document.addEventListener("DOMContentLoaded", function () {
    // Menampilkan grafik default Tweet saat halaman dimuat
    displayChartTotal();
});

// Menampilkan grafik default saat halaman dimuat
document.addEventListener("DOMContentLoaded", function () {
    // variabel mengambil id untuk Type Chart
    var chartType = getCurrentChartType();
    // variabel mengambil Attribute data-id bacapres
    var displayOption = getCurrentDisplayOption();
    // Menampilkan grafik default Tren saat halaman dimuat
    displayChart(chartType, displayOption);
});