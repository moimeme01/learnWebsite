// Fetch "Hello World" from backend
fetch("/")
    .then(response => response.json())
    .then(data => {
        document.getElementById("greeting").textContent = data.message;
    })
    .catch(err => console.error("Error fetching message:", err));

fetch('/user')
  .then(res => res.json())
  .then(data => {
    if(data.user_id) {
      console.log("User ID from cookie:", data.user_id);
    } else {
      console.log("No user ID found");
    }
  });

document.addEventListener('DOMContentLoaded', () => {
  const loggerModal = document.getElementById('loggerModal');
  const usernameInput = document.getElementById('usernameInput');
  const submitBtn = document.getElementById('submitUsername');

  // Check if username already saved
  const savedUser = localStorage.getItem('username');
  if (savedUser) {
    // Hide modal if user exists
    loggerModal.style.display = 'none';
    console.log("Welcome back, " + savedUser);
  } else {
    // Show modal and wait for submit
    loggerModal.style.display = 'flex';
  }

  submitBtn.addEventListener('click', () => {
    const username = usernameInput.value.trim();
    if (username) {
      localStorage.setItem('username', username);
      loggerModal.style.display = 'none';
      console.log("Hello, " + username);
      // Optionally: send username to backend here via fetch
    } else {
      alert("Please enter a username!");
    }
  });
});