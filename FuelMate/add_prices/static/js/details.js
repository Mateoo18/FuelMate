document.addEventListener('DOMContentLoaded', function() {
    // Jeśli są jakieś komunikaty, wyświetl je
    if (window.messages && window.messages.length > 0) {
        window.messages.forEach(function(message) {
            // Wywołanie funkcji do pokazania komunikatu
            showMessage(message.text, message.type);
        });
    }

    // Funkcja do wyświetlania komunikatu na ekranie
    function showMessage(message, type) {
        const messageBox = document.createElement('div');
        messageBox.classList.add('message-box', type);
        messageBox.textContent = message;

        document.body.appendChild(messageBox);

        // Pokaż komunikat
        messageBox.style.display = 'block';

        // Ukryj komunikat po 5 sekundach
        setTimeout(() => {
            messageBox.style.display = 'none';
            messageBox.remove();
        }, 5000);
    }
});
