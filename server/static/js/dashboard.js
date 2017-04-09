var default_dataset = {
    label:"label", 
    pointRadius: 1,
    pointHoverRadius: 5,
    fill: false,
    data: []
};

function AppendToOrCreateDataset(name, timestamp, value){
    var updated = false;
    for (var i=0; i<window.temperature_data.datasets.length; i++){
        if (window.temperature_data.datasets[i].label != name)
            continue;
        window.temperature_data.datasets[i].data.push({
            x: timestamp,
            y: value
        });
        updated = true;
    }

    if (updated) 
        return;
    
    console.log(window.default_dataset);
    new_dataset = JSON.parse(JSON.stringify(window.default_dataset));
    new_dataset.label = name;

    var r = Math.floor(Math.random() * 255);
    var g = Math.floor(Math.random() * 255);
    var b = Math.floor(Math.random() * 255);
    new_dataset.borderColor =  "rgb(" + r + "," + g + "," + b + ")";
    new_dataset.data.push({
        x: timestamp,
        y: value
    });
    window.temperature_data.datasets.push(new_dataset);
}

function UpdateChart(data){
    
    for (var i=0; i<data.measurements.length; i++){
        if(window.selected_node != -1 && data.node_id != window.selected_node)
            continue;

        AppendToOrCreateDataset(
            data.node.name + ' ' + data.measurements[i].label,
            data.timestamp,
            data.measurements[i].value,
        );
    }
    console.log(window.temperature_data);
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
        console.log(received_msg);
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
                    time: {
                        unit: 'minute',
                        unitStepSize: 5
                    }
                }],
                yAxes:[{
                    ticks:{
                        suggestedMin: 0,
                        suggestedMax: 100
                    }
                }]
            }
        }
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
