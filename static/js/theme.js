/*<!---
#comp 3450 <Ashima,ripan>--> */
document.addEventListener("DOMContentLoaded", function() {
    let mode = localStorage.getItem("mode");
    if (mode) document.body.classList.add(mode);
});

// Toggle Dark Mode
function toggleMode() {
    document.body.classList.toggle("dark-mode");
    localStorage.setItem("mode", document.body.classList.contains("dark-mode") ? "dark-mode" : "light-mode");
}

// Toggle High Contrast Mode
function toggleContrast() {
    document.body.classList.toggle("high-contrast");
    localStorage.setItem("mode", document.body.classList.contains("high-contrast") ? "high-contrast" : "light-mode");
}
