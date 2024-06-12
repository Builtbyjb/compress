// Controls which section is being displayed
function displaySection(section) {
    document.querySelector("#defaultDiv").style.display = 'none';
    document.querySelectorAll(".sectionDisplay").forEach((section) => {
        section.style.display = "none";
    });
    document.querySelector(`#${section}`).style.display = "block";
}

/* for each button with the "section_button" class,
*  it calls the display_section function
*/
document.querySelectorAll(".sectionButton").forEach((button) => {
    button.onclick = () => {
        displaySection(button.dataset.section);
    }
});

// Video Conversion
document.querySelector("#vidConvertForm").onsubmit = () => {
    document.querySelector("#vidConvertMsgLog").innerHTML = "Submitted successfully";
    const formData = new formData();
    const fileField = document.querySelector("#vidConvertFile");
    console.log(fileField);
    return false;
}


// Sends data to the server
async function upload(formData, path, msgLogID) {
    try {
        const response = await fetch(`https://127.0.0.1:8000/${path}`, {
            method: "POST",
            body: formData,
        })
        console.log(response);
    } catch (error) {
        console.log("Upload error: ", error);
    }

}