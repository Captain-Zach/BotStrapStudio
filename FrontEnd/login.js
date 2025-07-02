document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const response = await fetch('https://botstrap-backend-7973138883.us-west1.run.app/login', {
    // const response = await fetch('http://localhost:8080/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    const result = await response.json();
    const msgDiv = document.getElementById('loginMessage');
    if (result.success) {
        // Redirect to game-select.html on successful login
        window.location.href = 'game-select.html';
    } else {
        msgDiv.textContent = result.message || 'Login failed.';
        msgDiv.style.color = 'red';
    }
});
