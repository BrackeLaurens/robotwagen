const SERVER_CONFIG = {
    baseUrl: "http://192.168.4.1:80",
    wsUrl: "ws://192.168.4.1:80"
};

let socket = undefined;
let timerInterval = null;
let totaalSeconden = 5 * 60; // 5 minuten

function connect_socket() {
    console.log("SOCKET - connect");
    disconnect_socket(); // sluit bestaande socket indien aanwezig

    socket = new WebSocket(`${SERVER_CONFIG.wsUrl}/connect-websocket`);

    socket.addEventListener("open", () => {
        document.getElementById("status").textContent = "Status: Connected";
    });

    socket.addEventListener("close", () => {
        socket = undefined;
        document.getElementById("status").textContent = "Status: Disconnected";
    });

    socket.addEventListener("message", (event) => {
        console.log("Message from Pico:", event.data);
        if (event.data === "start") {
            startTimer(); // Timer starten via bericht van Pico
        }
    });

    socket.addEventListener("error", () => {
        socket = undefined;
        document.getElementById("status").textContent = "Status: Disconnected";
    });
}

function disconnect_socket() {
    if (socket != undefined) {
        socket.close();
    }
}

function sendCommand(command) {
    if (socket != undefined && socket.readyState === WebSocket.OPEN) {
        socket.send(command);

        if (command === 'noodstop') {
            document.getElementById("status").textContent = "Status: EMERGENCY STOP";
            console.log("Emergency stop initiated!");
            stopTimer(); // timer pauzeren/stoppen
        }

        if (command === 'start') {
            startTimer();
        }

    } else {
        alert("Not connected to the PICO");
    }
}

function startTimer() {
    stopTimer(); // Reset als hij al loopt
    totaalSeconden = 5 * 60;

    updateTimerDisplay(); // Toon meteen de starttijd

    timerInterval = setInterval(() => {
        if (totaalSeconden > 0) {
            totaalSeconden--;
            updateTimerDisplay();
        } else {
            clearInterval(timerInterval);
            timerInterval = null;
            document.getElementById("timer").textContent = "00:00:00";
            console.log("Timer afgelopen.");
        }
    }, 1000);
}

function stopTimer() {
    if (timerInterval !== null) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
}

function updateTimerDisplay() {
    const uren = Math.floor(totaalSeconden / 3600);
    const minuten = Math.floor((totaalSeconden % 3600) / 60);
    const seconden = totaalSeconden % 60;

    document.getElementById("timer").textContent =
        `${String(uren).padStart(2, '0')}:${String(minuten).padStart(2, '0')}:${String(seconden).padStart(2, '0')}`;
}

// Socket automatisch verbinden bij laden
window.addEventListener('load', function () {
    connect_socket();
});
