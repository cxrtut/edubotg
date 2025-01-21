// Function to toggle dropdown visibility
function toggleDropdown() {
    const dropdownMenu = document.getElementById('dropdownMenu');
    dropdownMenu.classList.toggle('show');
    
    // Change user icon color when clicked
    const userIcon = document.querySelector('.user-icon');
    userIcon.classList.toggle('clicked');
}

// JavaScript to open/close the profile modal
function openProfileModal() {
    const modal = document.getElementById("profileModal");
    modal.style.display = "block"; // Show the modal when clicked
}

function closeProfileModal() {
    const modal = document.getElementById("profileModal");
    modal.style.display = "none"; // Close the modal
}

// Close the modal when clicking outside of it
window.onclick = function(event) {
    const modal = document.getElementById("profileModal");
    if (event.target === modal) {
        modal.style.display = "none"; // Close if clicked outside of the modal
    }
}
