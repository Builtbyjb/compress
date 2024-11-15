import { handleNavBar, calcFileSize, isValidExt, isValidSize } from "./utills.js";

handleNavBar();

const fileInput = document.getElementById('file-input');
const fileList = document.getElementById('file-list');

fileInput.addEventListener('change', handleFiles);

function handleFiles() {
    const files = this.files;

    const d = new Date()
    const secs = d.getSeconds()

    if (files.length > 0) {
        for (let i = 0; i < files.length; i++) {
            const idx = i + secs // Generate unique id
            uploadFile(files[i], idx);
        }
    }
}

async function uploadFile(file, idx) {

    const fileSize = calcFileSize(file.size)

    const fileItem = document.createElement('div');
    fileItem.className = 'bg-gray-800 p-4 rounded-lg shadow';
    fileItem.innerHTML = `
        <p id="file-${idx}-msg-display" class="text-sm font-medium text-red-400"></p>
        <p id="file-display-name-${idx}" class="text-sm font-medium text-gray-300">${file.name}</p>
        <p class="mt-1 mb-1 text-sm font-medium text-gray-300">size: ${fileSize}</p>
    `;

    const validExt = isValidExt(file.name)
    const validSize = isValidSize(file.size)

    if (validExt && validSize) {
        const preloader = generatePreloader()
        fileItem.appendChild(preloader);
    }

    fileList.appendChild(fileItem);

    if (!validExt) {
        fileMsgUpdate(idx, "Invalid extention")
    }

    if (!validSize) {
        fileMsgUpdate(idx, "File size cannot be larger 1GB")
    }

    // console.log(file);

    if (validExt && validSize) {
        const formData = new FormData();
        formData.append("file", file);

        const r = await sendFile(formData)

        if (r.message === "Success") {
            fileItem.removeChild(preloader)

            // Calculate new file size
            const newFileSize = calcFileSize(r.compressedFileSize)

            fileItem.innerHTML += `
            <p class="mt-1 me-2 text-sm text-gray-300 font-semibold"
            >Compressed size: ${newFileSize}</p>
            `;

            fileItem.innerHTML += `
            <p class="mt-1 mb-2 text-sm text-green-400 font-semibold">Complete!!!</p>
            `;

            changeDisplayFileName(r.fileDisplayName, idx)

            const btn = generateBtn(r.fileDownloadName, r.fileDisplayName)
            fileItem.appendChild(btn)
        } else {
            fileItem.removeChild(preloader)

            fileItem.innerHTML += `
            <p class="mt-2 me-2 text-sm text-red-400 font-semibold">Failed</p>
            `;

            fileItem.innerHTML += `
            <p class="mt-2 me-2 text-sm text-red-400 font-semibold">${r.detail}</p>
            `;

            fileItem.innerHTML += `
            <p class="mt-2 me-2 text-sm text-blue-400 font-semibold"
            >Please try again</p>
            `;

            fileInput.value = "";
        }
    }

}

// Upload image/video files
async function sendFile(formData) {
    try {
        const file = await fetch('/compress', {
            method: "POST",
            body: formData

        })
        const r = await file.json()
        // console.log(r)
        return r

    } catch (error) {
        console.error(error)
    }
}

function generatePreloader() {
    const div = document.createElement("div");
    div.className = "preloader"
    div.innerHTML = `
        <div class="mt-2 text-blue-400 text-sm font-semibold">Compressing...</div>
        <div class="mt-2 relative w-100 h-1 bg-gray-200 rounded-full overflow-hidden">
            <div class="absolute top-0 left-0 h-full w-1/3 bg-blue-500 rounded-full animate-slide"></div>
        </div>
    `;

    return div
}

function generateBtn(fileDownloadName, fileName) {
    const btn = document.createElement("button");
    btn.setAttribute("id", "compress-btn");
    btn.setAttribute("data-filedownloadname", `${fileDownloadName}`);
    btn.setAttribute("data-filename", `${fileName}`);
    btn.className = "text-gray-300 bg-blue-700 hover:bg-white hover:bg-opacity-10 hover:text-white px-3 py-2 rounded-md text-sm font-medium";
    btn.textContent = "Download";

    return btn
}

// Download compressed files
document.addEventListener("click", (event) => {
    const element = event.target;

    if (element.id === "compress-btn") {
        const a = document.createElement("a");
        a.setAttribute("download", `${element.dataset.filename}`);
        a.setAttribute("href", `/downloads/${element.dataset.filedownloadname}`);
        a.style.display = "none";
        document.body.append(a);
        a.click();
        a.remove();
    }
})

function changeDisplayFileName(fileName, idx) {
    document.querySelector(`#file-display-name-${idx}`).textContent = fileName;
}

// Update file mesage
function fileMsgUpdate(idx, message) {
    document.querySelector(`#file-${idx}-msg-display`).textContent = message
}