// Example of basic interactivity - for future enhancements
document.addEventListener('DOMContentLoaded', () => {
    const logoutButton = document.querySelector('a[href$="logout"]');
    
    // Confirmation before logging out
    if (logoutButton) {
        logoutButton.addEventListener('click', (e) => {
            const confirmLogout = confirm("Are you sure you want to log out?");
            if (!confirmLogout) {
                e.preventDefault();
            }
        });
    }
});
