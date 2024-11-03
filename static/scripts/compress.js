import { handleNavBar, calcFileSize } from "./utills.js";

handleNavBar();

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
    const fileSize = calcFileSize(file.size)

    const fileItem = document.createElement('div');
    fileItem.className = 'bg-gray-800 p-4 rounded-lg shadow';
    fileItem.innerHTML = `
        <p class="text-sm font-medium text-gray-300">${file.name}</p>
        <p class="mt-1 text-sm font-medium text-gray-300"
        >File type: ${file.type}</p>
        <p class="mt-1 mb-1 text-sm font-medium text-gray-300"
        >Original size: ${fileSize}</p>
    `;

    const compressElement = generateCompressElement()

    fileItem.appendChild(compressElement);
    fileList.appendChild(fileItem);

    const formData = new FormData();
    formData.append(`${file.name}`, file);

    // console.log(file);

    const response = await sendFile(formData)
    if (response) {
        fileItem.removeChild(compressElement)

        fileItem.innerHTML += `
        <p class="mt-1 me-2 text-sm text-gray-300 font-semibold"
        >Compression size: ${1.45}MB</p>
        `;

        fileItem.innerHTML += `
        <p class="mt-1 mb-2 text-sm text-green-400 font-semibold">Complete!!!</p>
        `;

        const btn = generateBtn()
        fileItem.appendChild(btn)
    } else {
        fileItem.removeChild(compressElement)

        fileItem.innerHTML += `
        <p class="mt-2 me-2 text-sm text-red-400 font-semibold">Failed</p>
        `;

        fileItem.innerHTML += `
        <p class="mt-2 me-2 text-sm text-blue-400 font-semibold"
        >Please try uploading the file again</p>
        `;

        // Failure error message
        // fileItem.innerHTML += `
        // <p class="mt-2 me-2 text-sm text-blue-400 font-semibold"
        // >Please try the uploading the file again</p>
        // `;

        fileInput.value = "";
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
        // console.log(response)
        // return true
        return false

    } catch (error) {
        console.error(error)
        return false
    }
}

function generateCompressElement() {
    const p = document.createElement("p");
    p.className = "mt-1 mb-2 text-sm text-blue-400 font-semibold"
    p.textContent = 'Compressing...'

    return p
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