// Fetch "Hello World" from backend
//fetch("/")
//    .then(response => response.json())
//    .then(data => {
//        document.getElementById("homepageTitle").textContent = data.message;
//    })
//    .catch(err => console.error("Error fetching message:", err));

document.addEventListener('DOMContentLoaded', () => {
  // Récupération des variables de la fenetre de connection

  const loggerModal = document.getElementById("loggerModal");
  const usernameInput = document.getElementById("usernameInput");
  const submitButton = document.getElementById("submitUsername");

  const savedUser = localStorage.getItem('username');
  if (savedUser) {
    // Hide modal if user exists
    loggerModal.style.display = 'none';
    alert("Welcome back, " + savedUser);
  } else {
    // Show modal and wait for submit
    loggerModal.style.display = 'flex';
  }


  submitButton.addEventListener('click', () => {
    const username = usernameInput.value.trim();
    if (username){
      localStorage.setItem('username', username);
      loggerModal.style.display = 'none';
      console.log("Hello" + username);

      //envoye l'adresse IP dans un database et le stoque avec le nom.
      fetch("/register-user", {
        method: "POST",
        headers: {"content-type": "application/json"},
        body: JSON.stringify({username})
      })
      .then(res => res.json())
      .then(data => console.log("Background response:", data))
      .catch(err => console.error("Error registering user:", err));

    } else {
      alert("You need to insert a username");
    }
  });
});


document.addEventListener("DOMContentLoaded", () => {
  const createGameBtn = document.getElementById("createGameBtn")
  createGameBtn.addEventListener('click', () => {
    window.location.href = "/waitingroom";
  });
});
