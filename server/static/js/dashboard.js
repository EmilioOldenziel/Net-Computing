var default_dataset = {
    label:"label", 
    pointRadius: 1,
    pointHoverRadius: 5,
    fill: false,
    data: []
};

// display max 5 minutes
var MAX_DATA_AGE = 5*60*1000;

function AppendToOrCreateDataset(name, timestamp, value){
    var dataset = null;

    if (((new Date) - timestamp) > MAX_DATA_AGE)
        return;

    for (var i=0; i<window.temperature_data.datasets.length; i++) {
        if (window.temperature_data.datasets[i].label == name) {
            dataset = window.temperature_data.datasets[i];
            break;
        }

    }

    if (!dataset) {
        dataset = JSON.parse(JSON.stringify(window.default_dataset));
        dataset.label = name;

        var h = Math.floor(Math.random() * 12) * 30;
        // var s = Math.floor(Math.random() * 3) * 25 + 50;
        var s = 100;
        var l = Math.floor(Math.random() * 3) * 25 + 25;
        dataset.borderColor =  "hsl(" + h + ", " + s + "%, " + l + "% )";

        window.temperature_data.datasets.push(dataset);   
    }
    
    dataset.data.push({
        x: timestamp,
        y: value
    });

    for (var i=0; i<dataset.data.length; i++) 
        if (((new Date) - new Date(dataset.data[i].x)) > MAX_DATA_AGE)
            dataset.data.splice(i,1);
}

function UpdateChart(data){
    for (var i=0; i<data.measurements.length; i++){
        if (window.selected_node != -1 && data.node_id != window.selected_node)
            continue;

        AppendToOrCreateDataset(
            data.node.name + ' ' + data.measurements[i].label,
            data.timestamp,
            data.measurements[i].value
        );
    }
    window.temperature_chart.data = window.temperature_data;
    window.temperature_chart.update();
}

function MeasurementsSocket() {
    if (! ("WebSocket" in window)) {
        // The browser doesn't support WebSocket
        alert("WebSocket NOT supported by your Browser!");
        return;
    }
    this.ws = new WebSocket("ws://" + window.location.host + "/measurements");

    this.ws.onopen = function() {

    };

    this.ws.onmessage = function (evt) { 
        var received_msg = JSON.parse(evt.data);
        // console.log(received_msg);
        if (received_msg.msg_type === 'update_clients'){
            UpdateChart(received_msg.data);
        }
    };

    this.ws.onclose = function() {
        setTimeout(initMeasuretmentSocket, 1000);
    };

    this.callRemoteMethod = function(node_id, method){
        this.ws.send(JSON.stringify({
            msg_type: 'method_call',
            data: {
                'node_id': node_id,
                'method': method
            }
        }));
    }
}


var selected_node = -1;

document.getElementById("node-select").addEventListener("change", function(){
    window.selected_node = this.options[this.selectedIndex].value;
    window.temperature_chart.destroy();
    initChart();
});

fetch('/api/nodelist/')
.then(function(response) {
    return response.json();
})
.then(function(data) {
    data = data.json_list;
    var select_element = document.getElementById("node-select");

    for (var idx = 0; idx < data.length; idx++) {
        var option_element = document.createElement('option');
        option_element.value = data[idx].id;
        option_element.innerHTML = data[idx].name;
        select_element.appendChild(option_element);
    }
});

function initChart(){
    window.temperature_chart_element = document.getElementById("temperature-chart");
    window.temperature_data = {datasets:[]};
    window.temperature_chart = new Chart(temperature_chart_element, {
        type: 'line',
        data: temperature_data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            gridLines: {
                drawBorder: true
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    position: 'bottom',
                    scaleLabel: {
                        display: true,
                        labelString: 'Time in seconds',
                    },
                    time: {
                        displayFormats:  {
                            minute: 'HH:mm:ss',
                            second: 'HH:mm:ss'
                        },
                        round: 'second'
                    }
                }],
                yAxes:[{
                    scaleLabel: {
                        display: true,
                        labelString: 'Temperature in degrees Celcius',
                    },
                    ticks:{
                        suggestedMin: 0,
                        suggestedMax: 100
                    }
                }]
            }
        }
    });

    var url = '/api/measurementslist/';
    if (window.selected_node != -1)
        url += window.selected_node;

    fetch(url)
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        data = data.json_list;
        for (var idx = 0; idx < data.length; idx++) {
            AppendToOrCreateDataset(
                data[idx].node.name + ' ' + data[idx].label,
                data[idx].timestamp,
                data[idx].value,
            );
        }
        window.temperature_chart.data = window.temperature_data;
        window.temperature_chart.update();
    });
}

function initMeasuretmentSocket(){
    window.measurement_socket = new MeasurementsSocket();    
}

initMeasuretmentSocket();
initChart();

document.getElementById("noise-button").addEventListener("click", function(){
    console.log(window.selected_node);
    window.measurement_socket.callRemoteMethod(window.selected_node, 'noise');
});
