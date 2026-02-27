<?php
session_start();

// Hardcoded credentials (intentionally vulnerable)
define('ADMIN_USERNAME', 'admin');
define('ADMIN_PASSWORD', 's3cur3P@ssw0rd!');

// Secret key for HMAC demo
define('SECRET_KEY', 'super_secret_hmac_key_12345');
