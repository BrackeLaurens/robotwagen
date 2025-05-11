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

  if (event.data.startsWith("score:")) {
    const score = event.data.split(":")[1];
    document.getElementById("live-score").textContent = score;
    return;
  }

  // Andere commando's
  switch (event.data) {
    case "start":
      startTimer();
      break;
    case "noodstop":
      stopTimer();
      break;
    default:
      console.warn("⚠️ Onbekend commando ontvangen:", event.data);
      break;
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
        if (command === 'kalibreer') {
            document.getElementById("status").textContent = "Status: kalibreren...";
            console.log("kalibreren begonnen!");
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





// WebSocket management
let ws;
let isConnected = false;
const maxReconnectAttempts = 5;
let reconnectAttempts = 0;

function connectWebSocket() {
    ws = new WebSocket('ws://192.168.4.1/connect-websocket');

    // Verbinding geslaagd
    ws.onopen = () => {
        isConnected = true;
        reconnectAttempts = 0;
        updateStatus("Verbonden");
        console.log("WebSocket verbonden");
    };

    // Verbinding verbroken
    ws.onclose = () => {
        isConnected = false;
        updateStatus("Verbinding verbroken - opnieuw verbinden...");
        console.log("WebSocket verbinding gesloten");

        if (reconnectAttempts < maxReconnectAttempts) {
            reconnectAttempts++;
            setTimeout(connectWebSocket, 1000); // Reconnect na 1 seconde
        } else {
            updateStatus("Fout: Kan niet verbinden");
        }
    };

    // Berichten ontvangen
    ws.onmessage = (e) => {
        console.log("Ontvangen:", e.data);

        if (e.data.startsWith("score:")) {
            updateScore(e.data.split(":")[1]);
        } else if (e.data === "started") {
            updateStatus("Actief - verbonden");
        } else if (e.data === "stopped") {
            updateStatus("Gepauzeerd - verbonden");
        }
    };

    ws.onerror = (error) => {
        console.error("WebSocket fout:", error);
        updateStatus("Fout in verbinding");
    };
}

// Helper functies
function updateStatus(message) {
    const statusElement = document.getElementById("status");
    if (statusElement) {
        statusElement.textContent = `Status: ${message}`;
        // Kleuraanpassingen gebaseerd op status
        if (message.includes("Verbonden")) statusElement.style.color = "green";
        else if (message.includes("Fout")) statusElement.style.color = "red";
        else statusElement.style.color = "orange";
    }
}

function updateScore(newScore) {
    const scoreElement = document.getElementById("live-score");
    if (scoreElement) {
        scoreElement.textContent = newScore;
        // Visuele feedback bij score-update
        scoreElement.classList.add("score-update");
        setTimeout(() => scoreElement.classList.remove("score-update"), 300);
    }
}

// Knop handlers
function setupButtonListeners() {
    document.querySelector(".buttonBlue")?.addEventListener("click", () => {
        if (ws && isConnected) {
            ws.send("start");
            updateStatus("Startcommando verzonden...");
        }
    });

    document.querySelector(".buttonRed")?.addEventListener("click", () => {
        if (ws && isConnected) {
            ws.send("noodstop");
            updateStatus("Noodstop geactiveerd!");
        }
    });
    document.querySelector(".buttonYellow")?.addEventListener("click", () => {
        if (ws && isConnected) {
            ws.send("kalibreer");
            updateStatus("kalibreren begonnen");
        }
    });
}

// Timer functie (indien nodig)
function updateTimer() {
    const timerElement = document.getElementById("timer");
    if (timerElement) {
        // Implementeer je timer logica hier
        // Bijvoorbeeld: timerElement.textContent = new Date().toLocaleTimeString();
    }
}

// Initialisatie
function init() {
    connectWebSocket();
    setupButtonListeners();
    setInterval(updateTimer, 1000); // Update timer elke seconde
}

// Start wanneer de pagina geladen is
document.addEventListener("DOMContentLoaded", init);