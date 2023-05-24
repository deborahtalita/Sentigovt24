let currentId = null;
let currentChart = null;

function displayChart(chartId, Id) {
    if (currentId && currentChart) {
        delete currentId;
        currentChart.destroy();
    }

    currentId = Id;
    console.log(currentId);

    if (chartId === 'chart-button1') {
        // Membuat grafik 1
        $.getJSON("/sentiment/getAllTotalSentiment/", function (response) {
            var options = {
                chart: {
                    width: "100%",
                    height: "90%",
                    type: "area",
                },
                dataLabels: {
                    enabled: false
                },
                series: response.total_sentiment_per_day[Id],
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
                colors: ['#00FF0A', '#7B7B7B', '#FF0000'],
                strokeColors: ['#00FF0A', '#7B7B7B', '#FF0000'],
            };
            const chart1 = new ApexCharts(document.getElementById('chart-display'), options);
            chart1.render();
            currentChart = chart1;
        })
    } else if (chartId === 'chart-button2') {
        // Membuat grafik 2
        $.getJSON("/sentiment/getAllTotalSentiment/", function (response) {
            var options = {
                series: response.total_sentiment_per_day[Id],
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
    $.getJSON("/sentiment/getAllTotalTweet/", function (response) {
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
            }
        };
        const chart = new ApexCharts(document.querySelector("#chart-display-Total"), options);
        chart.render();
    })  
}

document.addEventListener("DOMContentLoaded", function () {
    displayChartTotal();
});

// Menampilkan grafik default saat halaman dimuat
document.addEventListener("DOMContentLoaded", function () {
    var chartType = getCurrentChartType();
    var displayOption = getSelectedBacapresOption();
    displayChart(chartType, displayOption);
    }
);

document.querySelectorAll(".chart-button").forEach(function(button) {
    button.addEventListener("click", function() {
        var chartType = button.getAttribute("id");
        console.log(chartType)
        var displayOption = getSelectedBacapresOption();
        console.log(displayOption)
        displayChart(chartType, displayOption);
    });
});

document.querySelectorAll(".rankingButton").forEach(function(button) {
    button.addEventListener("click", function() {
        var chartType = getCurrentChartType();
        console.log(chartType)
        var displayOption = button.getAttribute("data-id");
        console.log(displayOption)
        displayChart(chartType, displayOption);
    });
});

function getCurrentChartType() {
    var activeButton = document.querySelector(".chart-button.activeTren");
    return activeButton ? activeButton.getAttribute("id") : null;
}

function getSelectedBacapresOption() {
    var activeButton = document.querySelector(".rankingButton.activeRanking");
    console.log(activeButton)
    return activeButton ? activeButton.getAttribute("data-id") : null;
}