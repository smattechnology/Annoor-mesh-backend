import requests


def get_all_user():
    url = 'https://dummyjson.com/users?limit=100'
    post_url = "http://localhost:1024/auth/register"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch users: {response.status_code}")
        return

    data = response.json()

    for d in data["users"]:
        name = f"{d['firstName']} {d['maidenName']} {d['lastName']}"
        email = d["email"]
        username = d["username"]
        password = d["password"]
        role = d.get("role", "user")

        payload = {
            "email": email,
            "username": username,
            "name": name,
            "password": password,
            "role": role if role in ("admin", "user") else "user"
        }

        try:
            post_response = requests.post(post_url, json=payload)
            if post_response.status_code != 200:
                print(f"Failed to register: {post_response.status_code}")
                print(post_response.text)
                break
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            break


if __name__ == '__main__':
    get_all_user()
