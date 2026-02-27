<?php
require_once 'config.php';

// Redirect to dashboard if already logged in
if (!empty($_SESSION['logged_in'])) {
    header('Location: dashboard.php');
    exit;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login — SecureCorp Portal</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .login-container { background: #fff; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 100%; max-width: 400px; }
        h1 { text-align: center; margin-bottom: 1.5rem; color: #333; }
        .form-group { margin-bottom: 1rem; }
        label { display: block; margin-bottom: 0.25rem; color: #555; font-size: 0.9rem; }
        input[type="text"], input[type="password"] { width: 100%; padding: 0.6rem; border: 1px solid #ccc; border-radius: 4px; font-size: 1rem; }
        button { width: 100%; padding: 0.7rem; background: #007bff; color: #fff; border: none; border-radius: 4px; font-size: 1rem; cursor: pointer; }
        button:hover { background: #0056b3; }
        .error { background: #f8d7da; color: #842029; padding: 0.6rem; border-radius: 4px; margin-bottom: 1rem; text-align: center; display: none; }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>SecureCorp Login</h1>
        <div class="error" id="error"></div>
        <form id="login-form">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit">Log In</button>
        </form>
    </div>
    <script>
        document.getElementById('login-form').addEventListener('submit', function(e) {
            e.preventDefault();

            var username = document.getElementById('username').value;
            var password = document.getElementById('password').value;

            fetch('/api/login.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: username, password: password }),
                credentials: 'same-origin'
            })
            .then(function(res) { return res.json(); })
            .then(function(data) {
                if (data.success) {
                    window.location.href = data.redirect || '/dashboard.php';
                } else {
                    var el = document.getElementById('error');
                    el.textContent = data.message || 'Invalid credentials.';
                    el.style.display = 'block';
                }
            })
            .catch(function() {
                var el = document.getElementById('error');
                el.textContent = 'An error occurred. Please try again.';
                el.style.display = 'block';
            });
        });
    </script>
</body>
</html>
