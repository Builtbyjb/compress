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
    const bytes = 1024

    // Calculate Kilo bytes
    let newSize = fileSize / bytes

    if (newSize > 1024) {
        // Calulate Mega bytes
        newSize = newSize / bytes

        if (newSize > 1024) {
            // Calulate Giga bytes
            newSize = newSize / bytes

            return `${newSize.toFixed(2)}GB`
        } else {
            return `${newSize.toFixed(2)}MB`
        }
    } else {
        return `${newSize.toFixed(0)}KB`
    }
}

const ALLOWED_EXT = ["jpg", "jpeg", "png", "mkv", "mov", "mp4", "heic", "heif"]

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

// Validate file size
export function isValidSize(fileSize) {
    const gBytes = 1_073_741_824
    if (fileSize > gBytes) {
        return false
    } else {
        return true
    }
}