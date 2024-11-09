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
    // TODO: make it more robust for KB and GB
    const bytes = 1_048_576
    const newSize = (fileSize / bytes).toFixed(2)

    return `${newSize}MB`
}

const ALLOWED_EXT = ["jpg", "jpeg", "png", "mkv", "mov", "mp4", "heic"]

// Validate file extention
export function isValidExt(fileName) {
    let isValid = false;
    const str = fileName.split(".");
    const idx = str.length - 1;
    ALLOWED_EXT.map(i => {
        if (i === str[idx].toLowerCase()) {
            isValid = true;
        }
    })

    return isValid
}