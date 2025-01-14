document.addEventListener("DOMContentLoaded", () => {
    const emailForm = document.getElementById("email-form");
    const emailInput = document.getElementById("email");
    const user_input = document.getElementById("user_email")
    const emailError = document.getElementById("email-error");
    const passwordSection = document.getElementById("password-section");
    const passwordForm = document.getElementById("password-form");
    const passwordInput = document.getElementById("password");
    const passwordError = document.getElementById("password-error");

    emailForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        emailError.textContent = "";

        const email = emailInput.value.trim();

        try {
            const response = await fetch("/validate_email", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email }),
            });

            const result = await response.json();
            if (!response.ok) {
                emailError.textContent = result.message;
                return;
            }
            user_input.setAttribute("value", emailInput.value.trim())
            // Show password section if email is valid
            passwordSection.style.display = "block";
            emailForm.style.display = "none";
        } catch (error) {
            emailError.textContent = "An error occurred. Please try again.";
        }
    });

    passwordForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        passwordError.textContent = "";
    
        const password = passwordInput.value.trim();
    
        if (password.length < 8) {
            passwordError.textContent = "Password must be at least 8 characters.";
            return;
        }
    
        try {
            const response = await fetch("/validate_password", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email: emailInput.value.trim(), password }),
            });
    
            const result = await response.json();
            if (!response.ok) {
                passwordError.textContent = result.message;
                return;
            }
    
            window.location.href = "/";
        } catch (error) {
            passwordError.textContent = "An error occurred. Please try again.";
        }
    });

});
