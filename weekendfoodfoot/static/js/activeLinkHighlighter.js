document.addEventListener('DOMContentLoaded', function () {
    var urlPath = window.location.pathname;
    var navLinks = document.querySelectorAll('.navbar-nav .nav-link');

    navLinks.forEach(function (link) {
        if (link.getAttribute('href') === urlPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
});
