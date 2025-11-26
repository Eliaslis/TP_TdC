let scenario = "none";

const express = require("express");
const http = require("http");
const WebSocket = require("ws");

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

app.use(express.static("public"));

console.log("Servidor iniciado...");

// Parámetros
let running = false;
let Kp = 1.2, Ki = 0.4, Kd = 0.2;
let setpoint = 1.0;
let disturbance = 0;

// Estado
let y = 0, u = 0;
let e = setpoint - y;
let integral = 0, prevError = 0;

// Simulación
setInterval(() => {
    if (!running) return;

    const dt = 0.05;

    // --- Error ---
    e = setpoint - y;

    // PID
    integral += e * dt;
    const derivative = (e - prevError) / dt;
    u = Kp * e + Ki * integral + Kd * derivative;

    // Aplicar escenario automático
    let autoDist = computeScenarioDisturbance(scenario);

    // Perturbación total
    y += disturbance + autoDist;

    // Planta
    y += dt * (-y + u);

    prevError = e;

    const payload = {
        y, u, e, Kp, Ki, Kd, setpoint, disturbance
    };

    wss.clients.forEach(c => {
        if (c.readyState === WebSocket.OPEN) {
            c.send(JSON.stringify(payload));
        }
    });

}, 50);

// WebSocket
wss.on("connection", ws => {
    console.log("Cliente conectado");

    ws.on("message", msg => {
        const data = JSON.parse(msg);

        if (data.cmd === "start") running = true;
        if (data.cmd === "stop") running = false;
        if (data.cmd === "reset") {
            y = 0;
            u = 0;
            e = setpoint;
            integral = 0;
            prevError = 0;
        }

        if (data.cmd === "update") {
            Kp = data.Kp;
            Ki = data.Ki;
            Kd = data.Kd;
            setpoint = data.setpoint;
            disturbance = data.disturbance;
        }

        if (data.cmd === "set_scenario") {
            scenario = data.scenario;
            console.log("Escenario cambiado a:", scenario);
        }
    });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log("Servidor escuchando en puerto " + PORT);
});

function computeScenarioDisturbance(s) {
    switch (s) {

        case "deploy_fail":
            // Fallo instantáneo fuerte
            return -2;

        case "critical_bug":
            // Falla progresiva que se hace más grave
            return -(Math.random() * 0.2 + 0.3);

        case "overload":
            // Carga pesada constante
            return 0.5;

        case "perfect":
            return 0;

        default:
            return 0;
    }
}

