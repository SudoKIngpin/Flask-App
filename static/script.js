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
