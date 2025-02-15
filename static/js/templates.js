function formatTime(dateString) {
    var date = new Date(dateString);

    // Formatowanie godziny i minut
    var hours = date.getHours().toString().padStart(2, '0');
    var minutes = date.getMinutes().toString().padStart(2, '0');

    return hours + ":" + minutes;  // Zwraca godzinę w formacie HH:mm
}
