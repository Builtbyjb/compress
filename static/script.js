document.addEventListener('DOMContentLoaded', function () {
    const navToggle = document.getElementById('nav-toggle');
    const mobileMenu = document.getElementById('mobile-menu');

    navToggle.addEventListener('click', function () {
        mobileMenu.classList.toggle('hidden');
    });
});
const fileInput = document.getElementById('file-input');
const fileList = document.getElementById('file-list');

// const btn = document.createElement("button");
// btn.setAttribute("id", "compress-btn");
// btn.className = "text-gray-300 bg-blue-700 hover:bg-white hover:bg-opacity-10 hover:text-white px-3 py-2 rounded-md text-sm font-medium";
// btn.textContent = "Compress";

fileInput.addEventListener('change', handleFiles);

function handleFiles() {
    const files = this.files;
    for (let i = 0; i < files.length; i++) {
        uploadFile(files[i]);
    }

}

async function uploadFile(file) {
    const fileItem = document.createElement('div');
    fileItem.className = 'bg-gray-800 p-4 rounded-lg shadow';
    fileItem.innerHTML = `
        <div class="flex items-center justify-between">
            <span class="text-sm font-medium text-gray-300">${file.name}</span>
            <span class="text-xs text-gray-400 progress-text">0%</span>
        </div>
        <div class="mt-2 h-2 relative max-w-xl rounded-full overflow-hidden">
            <div class="w-full h-full bg-gray-700 absolute"></div>
            <div class="h-full bg-blue-600 absolute transition-all duration-300 ease-in-out progress-bar" style="width: 0%"></div>
        </div>
    `;
    fileList.appendChild(fileItem);

    const progressBar = fileItem.querySelector('.progress-bar');
    const progressText = fileItem.querySelector('.progress-text');

    const formData = new FormData();
    formData.append(`${file.name}`, file);

    // console.log(file);
    // const data = await fetch("/compress", {
    //     method: "POST",
    //     headers: {
    //         "Content-Type": "multipart/form-data"
    //     },
    //     body: formData
    // })

    // const response = await data;
    // console.log(response)


    // Simulating file upload with setTimeout
    let progress = 0;
    const simulateUpload = setInterval(() => {
        if (progress >= 100) {
            clearInterval(simulateUpload);
            fileItem.innerHTML += `
            <div class="mt-2 text-sm text-green-400 font-semibold">
                Upload complete!
            </div>
            `;
            // fileList.appendChild(btn)
        } else {
            progress += 5;
            progressBar.style.width = progress + '%';
            progressText.textContent = progress + '%';
        }
    }, 200);
}

// Download compress files
document.addEventListener("click", (event) => {
    const element = event.target;

    if (element.id === "compress-btn") {
        console.log(fileInput);
    }
})