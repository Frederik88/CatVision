var detection;
var fpsChart;
var secChart;
var mainLoopId;
var timeElapsed;
var slider;

var yoloActive;
var ssdActive;
var tinyYoloActive;
var rcnnActive;

$(document).ready(function () {
    timeElapsed = 0;
    detection = false;

    yoloActive = false;
    ssdActive = false;
    tinyYoloActive = false;
    rcnnActive = false;

    slider = document.getElementById("pwmSlider");

    //Create Charts
    fpsChart = new CreateChart(
        "fpsChart",
        "FPS",
        "#ff0000",
        "single",
        1,
        120,
        40
    );
    secChart = new CreateChart(
        "msChart",
        "Sekunden",
        "#00FF00",
        "single",
        0,
        10,
        2
    );

})

//Slider event for touch display
$(function () {
    $('#pwmSlider').bind('touchend', function () {
        $.getJSON('/slider' ,{
            post: slider.value
        }, function (data) {
            var response = data.result;
            console.log(response);
            });
        return false;
    });
});

//Slider event for mouse input
$(function () {
    $('#pwmSlider').bind('click', function () {
        $.getJSON('/slider' ,{
            post: slider.value
        }, function (data) {
            var response = data.result;
            console.log(response);
            });
        return false;
    });
});



function fetchData(delay) {
    if (detection) {
        mainLoopId = setInterval(function(){
            fetchFpsData();
            fetchSecData();
            fetchCountedData()

            timeElapsed = timeElapsed + 2;
            fpsChart.lineChart.update();
            secChart.lineChart.update();

        }, delay);
    }
}

// Fetch counted data from python
function fetchCountedData() {
    fetch('/detected')
        .then(function (response) {
            return response.json();
        }).then(function (json) {
        var obj_1 = json['ONE'];
        var obj_2 = json['TWO'];
        var obj_3 = json['THREE'];

        document.getElementById('hazNumber').innerHTML = obj_1;
        document.getElementById('walNumber').innerHTML = obj_2;
        document.getElementById('peaNumber').innerHTML = obj_3;
        console.log('Hazelnut: ', obj_1);
        console.log('Walnut: ', obj_2);
        console.log('Peanut: ', obj_3);
    });
}



// Fetch fps Data
function fetchFpsData() {
    fetch('/fps')
        .then(function (response) {
            return response.json();
        }).then(function (json) {
        var fps = json['FPS'];

        if(fps > 120){
            fps = 120;
        }
        fpsChart.config.data.labels.push(timeElapsed);
        fpsChart.config.data.datasets[0].data.push(fps);

        if(timeElapsed >= 40){
            fpsChart.config.data.labels.reverse();
            fpsChart.config.data.labels.pop();
            fpsChart.config.data.labels.reverse();
            fpsChart.config.data.datasets[0].data.reverse();
            fpsChart.config.data.datasets[0].data.pop();
            fpsChart.config.data.datasets[0].data.reverse();
        }

        console.log('FPS Jav: ', fps);
        console.log("Time: ", timeElapsed);
    });
}

// Fetch Seconds Data
function fetchSecData() {
    fetch('/sec')
        .then(function (response) {
            return response.json();
        }).then(function (json) {
        var sec = json['SEC'];

        if(sec > 10){
            sec = 10;
        }
        secChart.config.data.labels.push(timeElapsed);
        secChart.config.data.datasets[0].data.push(sec);

        if(timeElapsed >= 40){
            secChart.config.data.labels.reverse();
            secChart.config.data.labels.pop();
            secChart.config.data.labels.reverse();
            secChart.config.data.datasets[0].data.reverse();
            secChart.config.data.datasets[0].data.pop();
            secChart.config.data.datasets[0].data.reverse();
        }

        console.log('Sec Jav: ', sec);
        console.log("Time: ", timeElapsed);
    });
}

// Callback Yolo Button
$(function () {
    $('#button1').bind('click', function () {
        $.getJSON('/button1',
            function (data) {
            });
        yoloActive = !yoloActive;

        if(yoloActive)
            document.getElementById("button1").style.color = "red";
        else
            document.getElementById("button1").style.color = "black";
        return false;
    });
});

// Callback SSD Button
$(function () {
    $('#button4').bind('click', function () {
        $.getJSON('/button4',
            function (data) {
                console.log(data);
            });
        ssdActive = !ssdActive;

        if(ssdActive)
            document.getElementById("button4").style.color = "red";
        else
            document.getElementById("button4").style.color = "black";
        return false;
    });
});

// Callback FasterRCNN Button
$(function () {
    $('#button3').bind('click', function () {
        $.getJSON('/button3',
            function (data) {
                console.log(data);
            });
        rcnnActive = !rcnnActive;

        if(rcnnActive)
            document.getElementById("button3").style.color = "red";
        else
            document.getElementById("button3").style.color = "black";
        return false;
    });
});

// Callback TinyYolo Button
$(function () {
    $('#button2').bind('click', function () {
        $.getJSON('/button2',
            function (data) {
                console.log(data);
            });
        tinyYoloActive = !tinyYoloActive;

        if(tinyYoloActive)
            document.getElementById("button2").style.color = "red";
        else
            document.getElementById("button2").style.color = "black";
        return false;
    });
});

// Callback Load Net Button
//$(function () {
//    $('#button5').bind('click', function () {
//        $.getJSON('/button5',
//            function (data) {
//                console.log(data);
//            });
//        return false;
//    });
//});
//Callback Reset Button
$(function () {
    $('#button5').bind('click', function () {
        $.getJSON('/button5',
            function (data) {
                console.log(data);
            });

            detection = false;
            clearInterval(mainLoopId);

            fpsChart = new CreateChart(
                "fpsChart",
                "FPS",
                "#ff0000",
                "single",
                1,
                120,
                40
            );
            secChart = new CreateChart(
                "msChart",
                "Sekunden",
                "#00FF00",
                "single",
                0,
                10,
                2
            );

            fpsChart.lineChart.update();
            secChart.lineChart.update();
            timeElapsed = 0;
            document.getElementById('hazNumber').innerHTML = 0;
            document.getElementById('walNumber').innerHTML = 0;
            document.getElementById('peaNumber').innerHTML = 0;


        return false;
    });
});

// Callback Fetch Data Button
$(function () {
    $('#button6').bind('click', function () {
        $.getJSON('/button6',
            function (data) {
                console.log(data);
            });
        if (!detection) {
            detection = true;
            console.log("Detection running")
            fetchData(2000);
        }
        else {
            detection = false;
            clearInterval(mainLoopId);
        }
        return false;
    });
});

// Callback Start Motor Button
$(function () {
    $('#button7').bind('click', function () {
        $.getJSON('/button7',
            function (data) {
                console.log(data);
            });
        return false;
    });
});

// Callback Stop Motor Button
$(function () {
    $('#button8').bind('click', function () {
        $.getJSON('/button8',
            function (data) {
                console.log(data);
            });
        return false;
    });
});

