document.getElementById("contactForm").addEventListener("submit", function(event) {
    event.preventDefault();

    let name = document.getElementById("name").value.trim();
    let email = document.getElementById("email").value.trim();
    let phone = document.getElementById("phone").value.trim();
    let message = document.getElementById("message").value.trim();
    let formMessage = document.getElementById("formMessage"); 

    let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    let phonePattern = /^[0-9]{10}$/;

    if (name === "" || email === "" || phone === "" || message === "") {
        formMessage.textContent = "Please fill in all fields.";
        formMessage.style.color = "red";
        return;
    }

    if (!emailPattern.test(email)) {
        formMessage.textContent = "Please enter a valid email address.";
        formMessage.style.color = "red";
        return;
    }

    if (!phonePattern.test(phone)) {
        formMessage.textContent = "Phone number must be 10 digits.";
        formMessage.style.color = "red";
        return;
    }

    formMessage.textContent = "Your message has been sent successfully!";
    formMessage.style.color = "green";

    document.getElementById("contactForm").reset();
});
