// JavaScript for enhancing user experience

document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");

    // Form validation
    form.addEventListener("submit", function(event) {
        let valid = true;
        const name = document.getElementById("name").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const bio = document.getElementById("bio").value;
        const skills = document.getElementById("skills").value;
        const employment = document.getElementById("employment").value;

        // Check if name is filled
        if (!name) {
            valid = false;
            alert("Please enter your name.");
        }

        // Check if email is valid
        const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
        if (!email || !email.match(emailPattern)) {
            valid = false;
            alert("Please enter a valid email address.");
        }

        // Check if password is filled
        if (!password) {
            valid = false;
            alert("Please enter your password.");
        }

        // Check if bio is filled
        if (!bio) {
            valid = false;
            alert("Please provide a bio.");
        }

        // Check if skills are filled
        if (!skills) {
            valid = false;
            alert("Please list your skills.");
        }

        // Check if employment is filled
        if (!employment) {
            valid = false;
            alert("Please enter your current employment status.");
        }

        // Prevent form submission if any field is invalid
        if (!valid) {
            event.preventDefault();
        }
    });

    // Optionally, you can add more functions or event listeners for interactivity
});
