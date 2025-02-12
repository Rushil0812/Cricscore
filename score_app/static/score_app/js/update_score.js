const socket = new WebSocket('ws://localhost:8000/ws/live_scores/');
console.log(socket)
socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log("Message received:", data);

    // Check if the data is valid
    if (data.team1 && data.team2) {
        // Update the live scores
        document.getElementById('live-scores').innerHTML = `
            <h2>${data.team1} vs ${data.team2}</h2>
            <p>Runs: ${data.team1_runs} - ${data.team2_runs}</p>
            <p>Wickets: ${data.team1_wickets} - ${data.team2_wickets}</p>
            <p>Overs: ${data.overs}</p>
        `;

        // Update the form fields
        const form = document.getElementById('update-score-form');
        if (form) {
            form.querySelector('input[name="team1_runs"]').value = data.team1_runs;
            form.querySelector('input[name="team2_runs"]').value = data.team2_runs;
            form.querySelector('input[name="team1_wickets"]').value = data.team1_wickets;
            form.querySelector('input[name="team2_wickets"]').value = data.team2_wickets;
            form.querySelector('input[name="overs"]').value = data.overs;
        }
    } 
    else {
        console.error("Invalid data received:", data);
    }
};    

socket.onerror = function(error) {
    console.error("WebSocket error:", error);
};