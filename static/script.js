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

function uploadFile(file) {
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

    // Simulating file upload with setTimeout
    let progress = 0;
    const simulateUpload = setInterval(() => {
        if (progress >= 100) {
            clearInterval(simulateUpload);
            fileItem.innerHTML += '<div class="mt-2 text-sm text-green-400 font-semibold">Upload complete!</div>';
        } else {
            progress += 5;
            progressBar.style.width = progress + '%';
            progressText.textContent = progress + '%';
        }
    }, 200);

    // In a real application, you would use XMLHttpRequest or Fetch API here
    // const xhr = new XMLHttpRequest();
    // xhr.open('POST', 'your-upload-url');
    // xhr.upload.addEventListener('progress', (e) => {
    //     if (e.lengthComputable) {
    //         const percentComplete = (e.loaded / e.total) * 100;
    //         progressBar.style.width = percentComplete + '%';
    //         progressText.textContent = Math.round(percentComplete) + '%';
    //     }
    // });
    // xhr.addEventListener('load', () => {
    //     if (xhr.status === 200) {
    //         fileItem.innerHTML += '<div class="mt-2 text-sm text-green-400 font-semibold">Upload complete!</div>';
    //     } else {
    //         fileItem.innerHTML += '<div class="mt-2 text-sm text-red-400 font-semibold">Upload failed!</div>';
    //     }
    // });
    // xhr.send(file);
}