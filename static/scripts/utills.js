export function handleNavBar() {
    document.addEventListener('DOMContentLoaded', function () {
        const navToggle = document.getElementById('nav-toggle');
        const mobileMenu = document.getElementById('mobile-menu');

        navToggle.addEventListener('click', function () {
            mobileMenu.classList.toggle('hidden');
        });
    });
}

// Converts bytes to megabytes
export function calcFileSize(fileSize) {
    const bytes = 1_048_576
    const newSize = (fileSize / bytes).toFixed(2)

    return `${newSize}MB`
}