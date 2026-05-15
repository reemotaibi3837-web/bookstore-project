document.getElementById("contactForm").addEventListener("submit", function(event) {

    let name = document.getElementById("name").value.trim();
    let email = document.getElementById("email").value.trim();
    let phone = document.getElementById("phone").value.trim();
    let message = document.getElementById("message").value.trim();
    let formMessage = document.getElementById("formMessage");

    let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    let phonePattern = /^[0-9]{10}$/;

    if (name === "" || email === "" || phone === "" || message === "") {

        event.preventDefault();

        formMessage.textContent = "Please fill in all fields.";
        formMessage.style.color = "red";

        return;
    }

    if (!emailPattern.test(email)) {

        event.preventDefault();

        formMessage.textContent = "Please enter a valid email address.";
        formMessage.style.color = "red";

        return;
    }

    if (!phonePattern.test(phone)) {

        event.preventDefault();

        formMessage.textContent = "Phone number must be 10 digits.";
        formMessage.style.color = "red";

        return;
    }

});
