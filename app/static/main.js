let socket = undefined;

function connect_test() {
    fetch("http://192.168.4.1:80/connect-test")
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
}


function connect_socket() {
    // Close any existing sockets
    disconnect_socket();

    socket = new WebSocket("ws://192.168.4.1:80/connect-websocket");

    // Connection opened
    socket.addEventListener("open", (event) => {
        document.getElementById("status").textContent = "Status: Connected";
    });

    socket.addEventListener("close", (event) => {
        socket = undefined;
        document.getElementById("status").textContent = "Status: Disconnected";
    });

    socket.addEventListener("message", (event) => {
        console.log(event.data)
    });

    socket.addEventListener("error", (event) => {
        socket = undefined;
        document.getElementById("status").textContent = "Status: Disconnected";
    });
}

function disconnect_socket() {
    if(socket != undefined) {
        socket.close();
    }
}

function sendCommand(command) {
    if(socket != undefined) {
        socket.send(command)
        if (command === 'noodstop') {
            console.log("Emergency stop initiated!");
            // You can add visual feedback here if needed
            document.getElementById("status").textContent = "Status: EMERGENCY STOP";
        }
    } else {
        alert("Not connected to the PICO")
    }
}

// Event Source setup
const eventSource = new EventSource("/stream");
const dataDiv = document.getElementById("pico-data");

eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    dataDiv.textContent = "Received data: " + data.value;
};

eventSource.onerror = function(error) {
    console.error("EventSource failed:", error);
    eventSource.close();
};

// Timer functionality
function startTimer() {
    let seconds = 0;
    
    setInterval(function() {
        seconds++;
        let hours = Math.floor(seconds / 3600);
        let minutes = Math.floor((seconds % 3600) / 60);
        let secs = seconds % 60;
        
        // Add leading zeros
        hours = hours.toString().padStart(2, '0');
        minutes = minutes.toString().padStart(2, '0');
        secs = secs.toString().padStart(2, '0');
        
        document.getElementById('timer').textContent = 
            `${hours}:${minutes}:${secs}`;
    }, 1000);
}

// Start the timer when the page loads
window.onload = startTimer; 