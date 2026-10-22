
const menuToggle = document.getElementById("menuToggle");
const navBar = document.getElementById("navBar");

if (menuToggle && navBar) {
    menuToggle.addEventListener("click", () => {
        const isOpen = navBar.classList.toggle("open");

        menuToggle.setAttribute("aria-expanded", isOpen);
        menuToggle.setAttribute(
            "aria-label",
            isOpen ? "Close navigation menu" : "Open navigation menu"
        );

        menuToggle.textContent = isOpen ? "✕" : "☰";
    });

    // Close the menu after selecting a link on mobile
    navBar.querySelectorAll(".nav-link").forEach(link => {
        link.addEventListener("click", () => {
            navBar.classList.remove("open");
            menuToggle.setAttribute("aria-expanded", "false");
            menuToggle.setAttribute("aria-label", "Open navigation menu");
            menuToggle.textContent = "☰";
        });
    });
}
