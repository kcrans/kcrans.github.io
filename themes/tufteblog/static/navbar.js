document.addEventListener("DOMContentLoaded", function() {
    const navLinks = document.querySelectorAll(".nav-link");
    const currentUrl = window.location.pathname;
    navLinks.forEach(function(link) {
        console.log(link.getAttribute("href"), currentUrl);
        if (link.getAttribute("href") === currentUrl) {
            link.classList.add("current-page");
        }
        else if (link.getAttribute("href") === "/posts" && currentUrl.includes("/posts/")) {
            link.classList.add("current-page");
        }
    });
});
