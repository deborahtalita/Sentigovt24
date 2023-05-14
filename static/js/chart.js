let currentDisplay = 'chart-display1';

function displayChart(id) {
    const currentDisplayElement = document.getElementById(currentDisplay);
    currentDisplayElement.classList.add('hidden');

    const selectedDisplayElement = document.getElementById(id);
    selectedDisplayElement.classList.remove('hidden');
    currentDisplay = id;
}

// Menampilkan chart yang berbeda
let currentChart = null; // Grafik yang sedang ditampilkan

const chartOptions1 = {
    // Konfigurasi grafik 1
    chart: {
        width: "100%",
        height: "90%",
        type: "area",
    },
    dataLabels: {
        enabled: false
    },
    series: [{
            name: "Positive",
            data: [45, 52, 38, 45, 19, 23, 2]
        },
        {
            name: "Neutral",
            data: [10, 25, 12, 32, 41, 20, 36]
        },
        {
            name: "Negative",
            data: [30, 20, 15, 40, 45, 50, 5]
        }
    ],
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
        categories: [
            "01/05/2023",
            "02/05/2023",
            "03/05/2023",
            "04/05/2023",
            "05/05/2023",
            "06/05/2023",
            "07/05/2023"
        ]
    },
    colors: ['#00FF0A', '#7B7B7B', '#FF0000'],
    strokeColors: ['#00FF0A', '#7B7B7B', '#FF0000'],
};

const chartOptions2 = {
    // Konfigurasi grafik 2
    series: [{
        name: 'Positive',
        data: [45, 52, 38, 45, 19, 23, 2]
    }, {
        name: 'Neutral',
        data: [30, 20, 15, 40, 45, 50, 5]
    }, {
        name: 'Negative',
        data: [10, 25, 12, 32, 41, 20, 36]
    }],
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
        categories: ["01/05/2023", "02/05/2023", "03/05/2023", "04/05/2023", "05/05/2023", "06/05/2023", "07/05/2023"],
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

function displayChart(chartId) {
    if (currentChart) {
        currentChart.destroy(); // Menghancurkan grafik yang sedang ditampilkan sebelumnya
    }

    if (chartId === 'chart-display1') {
        // Membuat grafik 1
        const chart1 = new ApexCharts(document.getElementById('chart-display'), chartOptions1);
        chart1.render();
        currentChart = chart1;
    } else if (chartId === 'chart-display2') {
        // Membuat grafik 2
        const chart2 = new ApexCharts(document.getElementById('chart-display'), chartOptions2);
        chart2.render();
        currentChart = chart2;
    }

    // Memperbarui kelas aktif pada tombol yang dipilih
    const buttons = document.querySelectorAll('.chart-button');
    buttons.forEach(button => {
        button.classList.remove('active');
        if (button.id === chartId) {
            button.classList.add('active');
        }
    });
}

// Menampilkan grafik default saat halaman dimuat
displayChart('chart-display1');