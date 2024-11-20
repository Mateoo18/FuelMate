function locateUser() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(sendLocation);
    } else {
        alert("Geolokalizacja nie jest wspierana przez twoją przeglądarkę.");
    }
}

function sendLocation(position) {
    fetch("{% url 'nearest_stations' %}", {
        method: "POST",
        headers: {
            "X-CSRFToken": "{{ csrf_token }}",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
        })
    })
    .then(response => response.json())
    .then(data => showStations(data.stations));
}
