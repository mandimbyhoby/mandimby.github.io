function showInfo(day) {
    document.querySelectorAll('.info > div').forEach(function(element) {
        element.style.display = 'none';
    });
    const selectedInfo = document.getElementById(day);
    if (selectedInfo) {
        selectedInfo.style.display = 'block';
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const firstDay = '{{ grouped_schedules.keys|first }}';  // Cela ne fonctionnera pas ici, à déplacer dans le template
    if (firstDay) {
        showInfo(firstDay);
    }
});
