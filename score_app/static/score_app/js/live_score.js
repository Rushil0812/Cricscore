const socket = new WebSocket('ws://localhost:8000/ws/live_scores/');
console.log("WebSocket connection established:", socket);

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log("Message received:", data);

    const matchCard = document.getElementById(`match-${data.match_id}`);
    if (!matchCard) {
        console.error(`Match card with id 'match-${data.match_id}' not found.`);
        return;
    }

    document.getElementById(`team1-score-${data.match_id}`).innerText = `${data.team1_runs}/${data.team1_wickets}`;
    document.getElementById(`team2-score-${data.match_id}`).innerText = `${data.team2_runs}/${data.team2_wickets}`;
    document.getElementById(`overs-${data.match_id}`).innerText = `${data.overs}`;

    const commentaryElement = document.getElementById(`commentary-${data.match_id}`);
    if (commentaryElement) {
        commentaryElement.innerText = data.commentary;
    } else {
        console.error(`Commentary element for match ${data.match_id} not found.`);
    }
};

socket.onerror = function(error) {
    console.error("WebSocket error:", error);
};

socket.onclose = function() {
    console.warn("WebSocket connection closed.");
};