import { handleNavBar, calcFileSize, isValidExt, isValidSize } from "./utills.js";

handleNavBar();

const expiredAt = 1;

const fileInput = document.getElementById('file-input');
const fileList = document.getElementById('file-list');

fileInput.addEventListener('change', handleFiles);

// Info display div
const infoDiv = document.createElement("div");
infoDiv.setAttribute("id", "info-div");
infoDiv.className = "container mx-auto max-w-2xl p-4 z-20";
infoDiv.innerHTML = `
    <div class="bg-dark-secondary shadow-lg rounded-lg p-6 mb-2">
        <div class="flex items-center">
            <div class="flex-shrink-0 mr-3">
                <svg class="h-5 w-5 text-yellow-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
            </div>
            <div>
                <p class="text-sm text-gray-300">
                    Please download your files immediately. Files are deleted after
                    <span class="font-bold">${expiredAt} hour(s)</span>.
                </p>
            </div>
        </div>
    </div>
`;

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

    // Append infoDiv
    fileList.appendChild(infoDiv)

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

    let preloader = ""
    if (validExt && validSize) {
        preloader = generatePreloader()
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