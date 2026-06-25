/* static/js/ui.js */

document.addEventListener('DOMContentLoaded', () => {
    // --- Theme Toggler ---
    const themeToggler = document.getElementById('theme-toggler');
    const htmlElement = document.documentElement;

    // Set initial theme based on localStorage or system preference
    const savedTheme = localStorage.getItem('theme') || 'light';
    htmlElement.setAttribute('data-theme', savedTheme);
    if (themeToggler) {
        themeToggler.checked = savedTheme === 'dark';
    }


    themeToggler?.addEventListener('change', () => {
        const newTheme = themeToggler.checked ? 'dark' : 'light';
        htmlElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });

    // --- Sidebar Toggler ---
    const sidebarToggler = document.getElementById('sidebar-toggler');
    const sidebar = document.querySelector('.sidebar');

    sidebarToggler?.addEventListener('click', () => {
        sidebar?.classList.toggle('is-open');
    });

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (e) => {
        if (window.innerWidth < 768 && sidebar?.classList.contains('is-open')) {
            if (!sidebar.contains(e.target) && !sidebarToggler.contains(e.target)) {
                sidebar.classList.remove('is-open');
            }
        }
    });
});
