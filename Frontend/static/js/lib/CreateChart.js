//Private variables
var ctx;
var config;
var lineChart;
var chartUpdate;
var title;
var id;
var lineColor;

function CreateChart(id, title, lineColor, option, min, max, stepSize) {
    if (option ==='single') {
        var created = createChart(id, title, lineColor, min, max, stepSize);
    }
    if (option === 'multi') {
        var created = createOverviewChart(id, title, lineColor);
    }


    this.id = id;
    this.title = title;
    this.lineColor = lineColor;
    this.min = min;
    this.max = max;
    this.stepSize = stepSize;
    this.ctx = created[0];
    this.config = created[1];
    this.lineChart = created[2];
}
function createOverviewChart(id, title, lineColor) {
    //Init Chart
    var ctx_ = document.getElementById(id).getContext('2d');
    var config_ = {
        type: 'line',
        data: {
            labels: [0],
            datasets: [
                {
                    label: title[0],
                    data: [0],
                    fill: false,
                    backgroundColor: [lineColor[0]],
                    borderColor: [lineColor[0]],
                    borderWidth: 1
                },
                {
                    label: title[1],
                    data: [1],
                    fill: false,
                    backgroundColor: [lineColor[1]],
                    borderColor: [lineColor[1]],
                    borderWidth: 1
                }
            ]
        },
        options: {
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: '[s]'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Wert'
                    },
                    ticks: {
                        suggestedMin: this.min,
                        suggestedMax: this.max
                    }
                }]
            }
        }
    };

    var lineChart_ = new Chart(ctx_, config_);
    return [ctx_, config_, lineChart_];
}

function createChart(id, title, lineColor, min, max, stepSize) {
    //Init Chart
    var ctx_ = document.getElementById(id).getContext('2d');
    var config_ = {
        type: 'line',
        data: {
            labels: [0],
            datasets: [
                {
                label: title,
                data: [0],
                fontColor:'#000000',
                fill: false,
                backgroundColor: [lineColor],
                borderColor: [lineColor],
                borderWidth: 1
                }
            ]
        },
        options: {
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        fontColor:'#000000',
                        labelString: '[s]'
                    },
                     ticks: {
                        beginAtZero:true,
                        fontColor:'#000000'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        fontColor:'#000000',
                        labelString: 'Value'
                    },
                    ticks: {
                        beginAtZero:true,
                        fontColor:'#000000',
                        min: min,
                        max: max,
                        stepSize: stepSize
                    }
                }]
            }
        }
    };

    var lineChart_ = new Chart(ctx_, config_);
    return [ctx_, config_, lineChart_];
}
