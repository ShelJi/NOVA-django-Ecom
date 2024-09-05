function toggletheme() {
    const body = document.body;
    const theme = body.getAttribute("data-bs-theme");
    const newTheme = theme === "light" ? "dark" : "light";

    body.setAttribute("data-bs-theme", newTheme);
    localStorage.setItem('theme', newTheme);
}
function applySavedTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.body.setAttribute("data-bs-theme", savedTheme);

    const toggleButton = document.getElementById('toggleThemeButton');
    toggleButton.checked = savedTheme === 'light';
}
document.addEventListener('DOMContentLoaded', () => {
    applySavedTheme();
});
