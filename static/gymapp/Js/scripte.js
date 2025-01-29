function showInfo(id) {
    document.querySelectorAll('.info').forEach(function(element) {
        element.style.display = 'none';
    });
    document.getElementById(id).style.display = 'block';
}
document.addEventListener("DOMContentLoaded", function() {
    showInfo('monday');
});