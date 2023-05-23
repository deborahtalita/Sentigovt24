let currentId = null;
let currentChart = null;

function getId(Id) {
    if (currentId && currentChart) {
        delete currentId;
        currentChart.destroy();
    }

    currentId = Id;
    console.log(currentId);

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
            series: response.series[currentId],
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
        const chart = new ApexCharts(document.getElementById('chart-display'), options);
        chart.render();
        currentChart = chart;
    })
}

// Menampilkan Chart untuk Tren All Tweet
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
        categories: ["01/05/2023", "02/05/2023", "03/05/2023", "04/05/2023", "05/05/2023", "06/05/2023", "07/05/2023"],
    }
};

var chart = new ApexCharts(document.querySelector("#chart-display-Total"), options);
chart.render();


// Menampilkan grafik default saat halaman dimuat
document.addEventListener("DOMContentLoaded", function () {
    getId(1);
});