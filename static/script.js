// Handles mobile navbar
document.addEventListener('DOMContentLoaded', function () {
    const navToggle = document.getElementById('nav-toggle');
    const mobileMenu = document.getElementById('mobile-menu');

    navToggle.addEventListener('click', function () {
        mobileMenu.classList.toggle('hidden');
    });
});

const fileInput = document.getElementById('file-input');
const fileList = document.getElementById('file-list');

fileInput.addEventListener('change', handleFiles);

function handleFiles() {
    const files = this.files;
    for (let i = 0; i < files.length; i++) {
        uploadFile(files[i]);
    }
}

async function uploadFile(file) {
    const fileItem = document.createElement('div');
    fileItem.className = 'bg-gray-800 p-4 rounded-lg shadow flex justify-between';
    fileItem.innerHTML = `
        <div class="flex items-center justify-between w-1/2">
            <span class="text-sm font-medium text-gray-300">${file.name}</span>
            <span class="text-sm font-medium text-gray-300">${file.type}</span>
        </div>
    `;

    const subDiv = document.createElement("div");
    subDiv.className = 'w-24 justify-center items-center'

    const spinner = generateSpinner(true, "blue")

    subDiv.append(spinner);
    fileItem.appendChild(subDiv);
    fileList.appendChild(fileItem);

    const formData = new FormData();
    formData.append(`${file.name}`, file);

    console.log(file);

    const response = await sendFile(formData)
    if (response) {
        subDiv.removeChild(spinner)
        fileItem.innerHTML += `
        <div class="mt-2 me-2 text-sm text-green-400 font-semibold">Complete</div>
        `;
        const btn = generateBtn()
        fileItem.appendChild(btn)
    } else {
        subDiv.removeChild(spinner)
        fileItem.innerHTML += `
        <div class="mt-2 me-2 text-sm text-red-400 font-semibold">Failed</div>
        `;
        const errorSpinner = generateSpinner(false, "red")
        fileItem.appendChild(errorSpinner)
    }
}

// Upload image/video files
async function sendFile(formData) {
    try {
        const file = await fetch('/compress', {
            method: "POST",
            headers: {
                "Content-Type": "multipart/form-data"
            },
            body: formData

        })
        const response = await file.json()
        console.log(response)
        return true
        // return false

    } catch (error) {
        console.error(error)
        return false
    }
}

function generateSpinner(play, color) {
    const spinner = document.createElement("div");
    spinner.className = 'relative w-8 h-8';
    spinner.setAttribute('id', 'spinner');

    if (play) {
        animate = "animate-spin-slow"
    } else {
        animate = ""
    }

    spinner.innerHTML = `
        <div class="absolute top-0 left-0 right-0 bottom-0 border-4 border-gray-200 rounded-full"></div>
        <div id="spinner-ring" class="absolute top-0 left-0 right-0 bottom-0 border-4 border-${color}-500 rounded-full border-t-transparent ${animate} "></div>
        <svg class="hidden">
            <defs>
                <linearGradient id="spinner-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" style="stop-color:#3B82F6;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#93C5FD;stop-opacity:1" />
                </linearGradient>
            </defs>
        </svg>
    `;

    return spinner
}

function generateBtn() {
    const btn = document.createElement("button");
    btn.setAttribute("id", "compress-btn");
    btn.className = "text-gray-300 bg-blue-700 hover:bg-white hover:bg-opacity-10 hover:text-white px-3 py-2 rounded-md text-sm font-medium";
    btn.textContent = "Download";

    return btn
}

// Download compress files
document.addEventListener("click", (event) => {
    const element = event.target;

    if (element.id === "compress-btn") {
        console.log("Downloading");
    }
})