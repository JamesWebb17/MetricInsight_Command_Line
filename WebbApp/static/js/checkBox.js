// Ajoutez un gestionnaire d'événements pour basculer la checkbox lorsqu'elle est cliquée
document.querySelector('.toggle-checkbox input').addEventListener('change', function () {
    var slider = document.querySelector('.toggle-checkbox .slider');
    slider.style.left = this.checked ? '30px' : '0';
});
