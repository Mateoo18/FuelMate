document.addEventListener("DOMContentLoaded", function () {
    // Inicjalizacja mapy
    const apiKey = 'IEG0jzxyaLifhaBjY8o7ofwsPiiXK4xD';
    const map = tt.map({
        key: apiKey,
        container: 'map',
        center: [stationLongitude, stationLatitude], // Współrzędne stacji paliw
        zoom: 14
    });

    map.addControl(new tt.NavigationControl());

    // Dodanie markera dla bieżącej stacji
    const marker = new tt.Marker()
        .setLngLat([stationLongitude, stationLatitude])
        .addTo(map);

    const popup = new tt.Popup({ offset: 35 })
        .setHTML(`<strong>${stationName}</strong><br>
                  ${stationAddress}<br>
                  Miasto: ${stationCity}<br>
                  Kod pocztowy: ${stationPostalCode}<br>
                  Telefon: ${stationPhone}`);
    marker.setPopup(popup);
    marker.togglePopup();
});

document.addEventListener("DOMContentLoaded", function () {
    const notifications = document.getElementById('notifications');
    if (typeof djangoMessages !== "undefined") {
        djangoMessages.forEach((msg) => {
            const div = document.createElement("div");
            div.className = `notification ${msg.tags}`;
            div.textContent = msg.message;

            notifications.appendChild(div);

            // Usuń powiadomienie po 5 sekundach
            setTimeout(() => div.remove(), 5000);
        });
    }
});