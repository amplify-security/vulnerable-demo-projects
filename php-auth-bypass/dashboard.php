<?php
require_once 'config.php';

if (empty($_SESSION['logged_in'])) {
    header('Location: index.php');
    exit;
}

if (isset($_GET['logout'])) {
    session_destroy();
    header('Location: index.php');
    exit;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard — SecureCorp Portal</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f0f2f5; padding: 2rem; }
        .dashboard { max-width: 800px; margin: 0 auto; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }
        h1 { color: #333; }
        .logout { color: #dc3545; text-decoration: none; font-size: 0.9rem; }
        .card { background: #fff; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 1rem; }
        .card h2 { margin-bottom: 0.75rem; color: #333; font-size: 1.1rem; }
        table { width: 100%; border-collapse: collapse; }
        th, td { text-align: left; padding: 0.5rem; border-bottom: 1px solid #eee; }
        th { color: #666; font-size: 0.85rem; text-transform: uppercase; }
        .badge { display: inline-block; padding: 0.15rem 0.5rem; border-radius: 3px; font-size: 0.8rem; color: #fff; background: #28a745; }
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>Welcome, <?= htmlspecialchars($_SESSION['username']) ?></h1>
            <a href="?logout=1" class="logout">Log out</a>
        </div>

        <div class="card">
            <h2>User Accounts</h2>
            <table>
                <tr><th>Username</th><th>Role</th><th>Status</th></tr>
                <tr><td>admin</td><td>Administrator</td><td><span class="badge">Active</span></td></tr>
                <tr><td>jdoe</td><td>Editor</td><td><span class="badge">Active</span></td></tr>
                <tr><td>alice</td><td>Viewer</td><td><span class="badge">Active</span></td></tr>
            </table>
        </div>

        <div class="card">
            <h2>API Keys</h2>
            <table>
                <tr><th>Key</th><th>Created</th></tr>
                <tr><td><code>sk-live-4f3c2a1b...</code></td><td>2025-12-01</td></tr>
                <tr><td><code>sk-live-9e8d7c6f...</code></td><td>2026-01-15</td></tr>
            </table>
        </div>

        <div class="card">
            <h2>Internal Notes</h2>
            <p>Database migration scheduled for next Monday. Backup credentials stored in <code>/etc/secrets/db.conf</code>.</p>
        </div>
    </div>
</body>
</html>
