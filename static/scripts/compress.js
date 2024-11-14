import { handleNavBar, calcFileSize, isValidExt } from "./utills.js";

handleNavBar();

const fileInput = document.getElementById('file-input');
const fileList = document.getElementById('file-list');

fileInput.addEventListener('change', handleFiles);

function handleFiles() {
    const files = this.files;

    if (files.length > 0) {
        for (let i = 0; i < files.length; i++) {
            uploadFile(files[i], i);
        }
    } else {
        console.log("At least one file most be submitted");
    }
}

async function uploadFile(file, idx) {

    // Validate file extentions
    const isValid = isValidExt(file.name)
    if (!isValid) {
        console.log(`The file with the name ${file.name} has an invalid extention`)
        return
    }

    const fileSize = calcFileSize(file.size)

    const fileItem = document.createElement('div');
    fileItem.className = 'bg-gray-800 p-4 rounded-lg shadow';
    fileItem.innerHTML = `
        <p id="file-display-name-${idx}" class="text-sm font-medium text-gray-300">${file.name}</p>
        <p class="mt-1 mb-1 text-sm font-medium text-gray-300"
        >Original size: ${fileSize}</p>
    `;

    const compressElement = generateCompressElement()

    fileItem.appendChild(compressElement);
    fileList.appendChild(fileItem);

    const formData = new FormData();
    formData.append("file", file);

    // console.log(file);

    const r = await sendFile(formData)
    if (r.message != undefined) {
        fileItem.removeChild(compressElement)

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
        fileItem.removeChild(compressElement)

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

function generateCompressElement() {
    const p = document.createElement("p");
    p.className = "mt-1 mb-2 text-sm text-blue-400 font-semibold"
    p.textContent = 'Compressing...'

    return p
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

// Download compress files
document.addEventListener("click", (event) => {
    const element = event.target;

    if (element.id === "compress-btn") {
        const a = document.createElement("a");
        a.setAttribute("download", `${element.dataset.filename}`);
        a.setAttribute("href", `/downloads/${element.dataset.filedownloadname}`);
        a.style.display = "none";
        document.body.append(a)
        a.click()
        a.remove()
    }
})

function changeDisplayFileName(fileName, idx) {
    document.querySelector(`#file-display-name-${idx}`).textContent = fileName;
}