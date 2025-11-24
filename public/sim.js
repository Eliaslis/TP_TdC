const ws = new WebSocket("ws://localhost:3000");

let chart;
const logBox = document.getElementById("logBox");

function log(msg) {
    logBox.textContent += msg + "\n";
    logBox.scrollTop = logBox.scrollHeight;
}

// Gráfico
window.onload = () => {
    const ctx = document.getElementById("chart");

    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: [],
            datasets: [
                { label: "Salida (y)", data: [], borderWidth: 2 },
                { label: "Control (u)", data: [], borderWidth: 2 },
                { label: "Error (e)", data: [], borderWidth: 2 }
            ]
        }
    });

    log("Cliente iniciado");
};

ws.onmessage = (msg) => {
    const data = JSON.parse(msg.data);

    chart.data.labels.push("");
    chart.data.datasets[0].data.push(data.y);
    chart.data.datasets[1].data.push(data.u);
    chart.data.datasets[2].data.push(data.e);

    chart.update();

    log(`y=${data.y.toFixed(3)} | u=${data.u.toFixed(3)} | err=${data.e.toFixed(3)}`);
};

function startSim() {
    ws.send(JSON.stringify({ cmd: "start" }));
    updateParams();
}

function stopSim() {
    ws.send(JSON.stringify({ cmd: "stop" }));
}

function resetSim() {
    ws.send(JSON.stringify({ cmd: "reset" }));
    chart.data.labels = [];
    chart.data.datasets.forEach(x => x.data = []);
    chart.update();
}

function updateParams() {
    ws.send(JSON.stringify({
        cmd: "update",
        Kp: parseFloat(kp.value),
        Ki: parseFloat(ki.value),
        Kd: parseFloat(kd.value),
        setpoint: parseFloat(sp.value),
        disturbance: parseFloat(dist.value)
    }));
}

function applyScenario() {
    ws.send(JSON.stringify({
        cmd: "set_scenario",
        scenario: scenario.value
    }));
    log("Escenario cambiado a: " + scenario.value);
}

