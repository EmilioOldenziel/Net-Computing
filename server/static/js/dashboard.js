var default_dataset = {
    label:"label", 
    pointRadius: 1,
    pointHoverRadius: 5,
    data: [{x:Date.now(), y:null}]
};

function UpdateChart(data){
    console.log(data);
    temperature_data.datasets[0].data.push({
        x: Date.now(), 
        y: data[0].value
    });
    if (temperature_data.datasets[0].data.length > 60*15)
        temperature_data.datasets[0].data.splice(0, 1);
    window.temperature_chart.data = data;
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

var temperature_chart_element = document.getElementById("temperature-chart");
var temperature_data = {datasets:[default_dataset]};
var temperature_chart = new Chart(temperature_chart_element, {
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

function initMeasuretmentSocket(){
    window.measurement_socket = new MeasurementsSocket();    
}

initMeasuretmentSocket();

document.getElementById("noise-button").addEventListener("click", function(){
    window.measurement_socket.callRemoteMethod(21, 'noise');
});
