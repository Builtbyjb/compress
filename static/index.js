// Controls which div is being displayed
function display_section(section) {
    document.getElementById("default_div").style.display = 'none';
    document.querySelectorAll(".section_display").forEach((section) => {
        section.style.display = "none";
    });
    document.querySelector(`#${section}`).style.display = "block";
}

/* for each button with the "section_button" class,
*  it calls the display_section function
*/
document.querySelectorAll(".section_button").forEach((button) => {
    button.onclick = () => {
        display_section(button.dataset.section);
    }
});

// Video Conversion
document.querySelector("#vid_convert_form").onsubmit = () => {
    console.log("submiting form");
    return false;
}