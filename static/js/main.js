/*
 * main.js - Global JavaScript for the LMS project.
 *
 * HOW JS WORKS IN DJANGO:
 *   1. JS files live in the static/ folder (or app-specific static/ folders)
 *   2. Templates include them: <script src="{% static 'js/main.js' %}"></script>
 *   3. This file is loaded on EVERY page (included in base.html)
 *   4. Page-specific JS goes in {% block extra_js %} in individual templates
 *
 * DOMContentLoaded:
 *   This event fires when the HTML is fully loaded and parsed.
 *   We wrap our code in this listener to make sure all HTML elements exist
 *   before we try to interact with them.
 *   Without it, JavaScript might try to find elements that haven't been created yet.
 */
document.addEventListener("DOMContentLoaded", function () {

    // --- Auto-dismiss alert messages after 5 seconds ---
    // querySelectorAll finds ALL elements matching the CSS selector ".alert"
    // It returns a NodeList (like an array of HTML elements)
    var alerts = document.querySelectorAll(".alert");

    // forEach loops through each alert element
    alerts.forEach(function (alert) {

        // setTimeout runs a function after a delay (in milliseconds)
        // 5000ms = 5 seconds
        setTimeout(function () {
            // First: fade out the alert by making it transparent
            alert.style.opacity = "0";

            // Then: after the fade animation (300ms), remove the element from the page entirely
            setTimeout(function () {
                alert.remove();  // Removes the HTML element from the DOM
            }, 300);
        }, 5000);  // Wait 5 seconds before starting the fade
    });
});
