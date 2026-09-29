//const API_URL = "http://127.0.0.1:8000/api/auth/register/";
//
//document.getElementById("register-form").addEventListener("submit", async (e) => {
//    e.preventDefault();
//
//    const errorEl = document.getElementById("error-msg");
//    errorEl.textContent = "";
//
//    const payload = {
//        username: document.getElementById("username").value,
//        email: document.getElementById("email").value,
//        role: document.getElementById("role").value,
//        password: document.getElementById("password").value,
//        password2: document.getElementById("password2").value,
//    };
//
//    try {
//        const res = await fetch(API_URL, {
//            method: "POST",
//            headers: { "Content-Type": "application/json" },
//            body: JSON.stringify(payload),
//        });
//
//        const data = await res.json();
//
//        if (!res.ok) {
//            // Flatten DRF error object into a readable string
//            const messages = Object.values(data).flat().join(" ");
//            errorEl.textContent = messages || "Registration failed.";
//            return;
//        }
//
//        // Save tokens and redirect
//        localStorage.setItem("access_token", data.access);
//        localStorage.setItem("refresh_token", data.refresh);
//        window.location.href = "/dashboard.html";
//
//    } catch (err) {
//        errorEl.textContent = "Network error. Please try again.";
//    }
//}); const API_URL = "http://127.0.0.1:8000/api/auth/register/";
//
//document.getElementById("register-form").addEventListener("submit", async (e) => {
//    e.preventDefault();
//
//    const errorEl = document.getElementById("error-msg");
//    errorEl.textContent = "";
//
//    const payload = {
//        username: document.getElementById("username").value,
//        email: document.getElementById("email").value,
//        role: document.getElementById("role").value,
//        password: document.getElementById("password").value,
//        password2: document.getElementById("password2").value,
//    };
//
//    try {
//        const res = await fetch(API_URL, {
//            method: "POST",
//            headers: { "Content-Type": "application/json" },
//            body: JSON.stringify(payload),
//        });
//
//        const data = await res.json();
//
//        if (!res.ok) {
//            // Flatten DRF error object into a readable string
//            const messages = Object.values(data).flat().join(" ");
//            errorEl.textContent = messages || "Registration failed.";
//            return;
//        }
//
//        // Save tokens and redirect
//        localStorage.setItem("access_token", data.access);
//        localStorage.setItem("refresh_token", data.refresh);
//        window.location.href = "/dashboard.html";
//
//    } catch (err) {
//        errorEl.textContent = "Network error. Please try again.";
//    }
//});
//document.getElementById("tc-accept").addEventListener("click", async () => {
//    try {
// Tell the backend the user accepted (recommended — see step 3)
//        const res = await fetch("/accounts/terms/accept/", {
//            method: "POST",
//            headers: {
//                "Content-Type": "application/json",
//                "X-CSRFToken": getCookie("csrftoken"),
//            },
//            credentials: "same-origin",
//            body: JSON.stringify({ accepted: true }),
//        });
//
//        if (!res.ok) throw new Error("Failed to record acceptance");
//
//        // Mark locally too — belt and suspenders
//        sessionStorage.setItem("terms_accepted", "true");
//
//        // 🚀 Send them BACK to the register page
//        window.location.href = "/accounts/register/";
//    } catch (err) {
//        console.error(err);
//        alert("Something went wrong. Please try again.");
//    }
//});
//
//document.getElementById("tc-decline").addEventListener("click", () => {
//    // Clear any prior acceptance
//    sessionStorage.removeItem("terms_accepted");
//    window.location.href = "/accounts/register/";
//});
//
//// Helper (if you don't already have one)
//function getCookie(name) {
//    const value = `; ${document.cookie}`;
//    const parts = value.split(`; ${name}=`);
//    if (parts.length === 2) return parts.pop().split(";").shift();
//}