<?php
require_once __DIR__ . '/../config.php';

header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed. Send a POST request with JSON body.']);
    exit;
}

// Read raw JSON input — json_decode preserves native types (bool, int, etc.)
$input = json_decode(file_get_contents('php://input'), true);

if (!$input || !isset($input['username']) || !isset($input['password'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Missing username or password. Send JSON: {"username":"...","password":"..."}']);
    exit;
}

$username = $input['username'];
$password = $input['password'];

// VULNERABLE: loose comparison (==) with json_decoded input
// Exploit 1: {"username":"admin","password":true}   -> true == "s3cur3P@ssw0rd!" is true
// Exploit 2: {"username":"admin","password":0}       -> 0 == "s3cur3P@ssw0rd!" is true (PHP < 8.0)
    if ($username == ADMIN_USERNAME && $password == ADMIN_PASSWORD) {
        $_SESSION['logged_in'] = true;
        $_SESSION['username'] = ADMIN_USERNAME;
    
        echo json_encode([
            'success' => true,
            'message' => 'Login successful.',
            'redirect' => '/dashboard.php',
            'session_id' => session_id()
        ]);
    } else {
        http_response_code(401);
        echo json_encode([
            'success' => false,
            'message' => 'Invalid credentials.'
        ]);
    }
