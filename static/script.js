const textElement = document.getElementById("text");
const message = "Welcome  SIETIANS !";
let index = 0;
let isDeleting = false;

function typeEffect() {
    if (isDeleting) {
        textElement.textContent = message.substring(0, index--);
    } else {
        textElement.textContent = message.substring(0, index++);
    }

    if (!isDeleting && index === message.length) {
        setTimeout(() => isDeleting = true, 1000); // Pause before deleting
    } else if (isDeleting && index === 0) {
        isDeleting = false;
    }

    setTimeout(typeEffect, isDeleting ? 160: 185); // Adjust typing and deleting speed
}

// Start the typing effect
typeEffect();




// Show the popup after the page loads
// window.onload = function() {
//     setTimeout(function() {
//         document.getElementById("exam-popup").style.display = "block";
//         document.getElementById("popup-overlay").style.display = "block";
//     }, 2500); // Popup appears 1 second after page load
// };

// Close the popup when the close button is clicked
// function closePopup() {
//     document.getElementById("exam-popup").style.display = "none";
//     document.getElementById("popup-overlay").style.display = "none";
// }




// Get the toggle button and its icons
const toggleBtn = document.getElementById('toggle-btn');
const brightIcon = document.getElementById('bright');
const darkIcon = document.getElementById('dark');
const root = document.documentElement;


function toggleMode() {
    // Check if we are currently in bright mode
    if (brightIcon.style.display !== 'none') {
        // Switch to dark mode
        brightIcon.style.display = 'none';
        darkIcon.style.display = 'block';
        document.body.style.filter = "invert(1)";
        document.querySelectorAll('img').forEach(img => img.style.filter = 'invert(1)');


    } else {
        // Switch to bright mode
        brightIcon.style.display = 'block';
        darkIcon.style.display = 'none';
        document.body.style.filter = "invert(0)";
        document.querySelectorAll('img').forEach(img => img.style.filter = 'invert(0)');

    }
}

// Add event listener to the toggle button
toggleBtn.addEventListener('click', toggleMode);

