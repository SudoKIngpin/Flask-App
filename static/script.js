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
window.onload = function() {
    setTimeout(function() {
        document.getElementById("exam-popup").style.display = "block";
        document.getElementById("popup-overlay").style.display = "block";
    }, 2500); // Popup appears 1 second after page load
};

// Close the popup when the close button is clicked
function closePopup() {
    document.getElementById("exam-popup").style.display = "none";
    document.getElementById("popup-overlay").style.display = "none";
}

