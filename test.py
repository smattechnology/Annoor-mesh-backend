from time import sleep

import requests

access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyNGY4NGE0YS0wZWE4LTQxY2ItOTRhYi0yZGIzNGRhNDE1YzQiLCJleHAiOjE3NTQzMDczNzJ9.gmPtsMwch1IU6JxhKaMUKaRU67oCm_QLijVhngRJYOQ"


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


def upload_category():
    post_url = "http://localhost:1024/product/add/category"
    access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyNGY4NGE0YS0wZWE4LTQxY2ItOTRhYi0yZGIzNGRhNDE1YzQiLCJleHAiOjE3NTQyMzY4OTh9.U3BPBnw-0ymSDLww4WLKxkQrsDUcO1tORDPnc3tGQ_8"
    cookies = {
        "access_token": access_token
    }
    categories = [
        {"value": "vegetables", "label": "সবজি (Vegetables)", "icon": "🥬"},
        {"value": "fruits", "label": "ফল (Fruits)", "icon": "🍎"},
        {"value": "grains", "label": "চাল ও ডাল (Grains & Pulses)", "icon": "🌾"},
        {"value": "dairy", "label": "দুগ্ধজাত (Dairy)", "icon": "🥛"},
        {"value": "meat", "label": "মাংস ও মাছ (Meat & Fish)", "icon": "🐟"},
        {"value": "spices", "label": "মসলা (Spices)", "icon": "🌶️"},
        {"value": "snacks", "label": "নাস্তা (Snacks)", "icon": "🍪"},
        {"value": "beverages", "label": "পানীয় (Beverages)", "icon": "🧃"},
    ]

    success_count = 0
    fail_count = 0

    with requests.Session() as session:
        for i, category in enumerate(categories, 1):
            try:
                response = session.post(post_url, json=category, cookies=cookies)
                if response.status_code == 201:
                    print(f"[{i}/{len(categories)}] ✅ Uploaded: {category['label']}")
                    success_count += 1
                elif response.status_code == 400 and "already exists" in response.text:
                    print(f"[{i}/{len(categories)}] ⚠️ Already exists: {category['label']}")
                else:
                    print(f"[{i}/{len(categories)}] ❌ Failed: {category['label']}, Status: {response.status_code}")
                    print(f"   → Error: {response.text}")
                    fail_count += 1
                sleep(0.2)  # Optional delay to avoid flooding server
            except requests.exceptions.RequestException as e:
                print(f"[{i}/{len(categories)}] ❗ Exception for {category['label']}: {e}")
                fail_count += 1

    print("\nUpload Summary:")
    print(f"✅ Success: {success_count}")
    print(f"❌ Failed: {fail_count}")


def upload_unite():
    post_url = "http://localhost:1024/product/add/unite"

    cookies = {
        "access_token": access_token
    }

    units = [
        {"value": "kilogram", "label": "কেজি (Kg)", "icon": "⚖️"},
        {"value": "gram", "label": "গ্রাম (g)", "icon": "⚖️"},
        {"value": "liter", "label": "লিটার (L)", "icon": "🥛"},
        {"value": "milliliter", "label": "মিলিলিটার (ml)", "icon": "🥛"},
        {"value": "piece", "label": "পিস (Pcs)", "icon": "📦"},
        {"value": "dozen", "label": "ডজন (Dozen)", "icon": "📦"},
        {"value": "bundle", "label": "বান্ডিল (Bundle)", "icon": "🎋"},
        {"value": "packet", "label": "প্যাকেট (Packet)", "icon": "📦"},
    ]

    success_count = 0
    fail_count = 0

    with requests.Session() as session:
        for i, unit in enumerate(units, 1):
            try:
                response = session.post(post_url, json=unit, cookies=cookies)
                if response.status_code == 201:
                    print(f"[{i}/{len(units)}] ✅ Uploaded: {unit['label']}")
                    success_count += 1
                elif response.status_code == 400 and "already exists" in response.text:
                    print(f"[{i}/{len(units)}] ⚠️ Already exists: {unit['label']}")
                else:
                    print(f"[{i}/{len(units)}] ❌ Failed: {unit['label']}, Status: {response.status_code}")
                    print(f"   → Error: {response.text}")
                    fail_count += 1
                sleep(0.2)
            except requests.exceptions.RequestException as e:
                print(f"[{i}/{len(units)}] ❗ Exception for {unit['label']}: {e}")
                fail_count += 1

    print("\nUpload Summary:")
    print(f"✅ Success: {success_count}")
    print(f"❌ Failed: {fail_count}")


def upload_product():
    post_url = "http://localhost:1024/product/add/"

    cookies = {
        "access_token": access_token
    }

    products = [
        {
            "name": "সয়াবিন তেল",
            "price": 100,
            "unite": None,
            "bld": {
                "breakfast": False,
                "lunch": False,
                "dinner": False,
                "editable": False,
            },
        },
        {
            "name": "সরিষার তেল",
            "price": 80,
            "unite": "লিটার",
            "bld": {
                "breakfast": False,
                "lunch": True,
                "dinner": False,
                "editable": True,
            },
        },
        {
            "name": "পাম তেল",
            "price": 90,
            "unite": "লিটার",
            "bld": {
                "breakfast": True,
                "lunch": True,
                "dinner": False,
                "editable": False,
            },
        },
        {
            "name": "কোকোনাট তেল",
            "price": 120,
            "unite": "লিটার",
            "bld": {
                "breakfast": False,
                "lunch": False,
                "dinner": True,
                "editable": True,
            },
        },
        {
            "name": "ঘি",
            "price": 200,
            "unite": "লিটার",
            "bld": {
                "breakfast": True,
                "lunch": False,
                "dinner": False,
                "editable": True,
            },
        },
        {
            "name": "বাটার",
            "price": 150,
            "unite": "লিটার",
            "bld": {
                "breakfast": False,
                "lunch": True,
                "dinner": True,
                "editable": False,
            },
        },
        {
            "name": "চিনি",
            "price": 50,
            "unite": "কেজি",
            "bld": {
                "breakfast": True,
                "lunch": True,
                "dinner": True,
                "editable": True,
            },
        },
        {
            "name": "লবণ",
            "price": 20,
            "unite": "কেজি",
            "bld": {
                "breakfast": False,
                "lunch": False,
                "dinner": False,
                "editable": False,
            },
        },
    ]

    category_id = "0a5bf0e4-0cb5-459c-88ca-4c9662bdc9fc"
    unite_id = "4bfdca59-59eb-478a-88ff-d36062ea1176"  # replace with real dynamic match if needed

    success_count = 0
    fail_count = 0

    with requests.Session() as session:
        for i, product in enumerate(products, 1):
            payload = {
                "name": product.get("name"),
                "price": str(product.get("price")),
                "unite_id": unite_id,
                "category_id": category_id,
            }

            try:
                response = session.post(post_url, json=payload, cookies=cookies)

                if response.status_code == 201:
                    print(f"[{i}/{len(products)}] ✅ Uploaded: {product['name']}")
                    success_count += 1
                elif response.status_code == 400 and "already exists" in response.text:
                    print(f"[{i}/{len(products)}] ⚠️ Already exists: {product['name']}")
                else:
                    print(f"[{i}/{len(products)}] ❌ Failed: {product['name']}, Status: {response.status_code}")
                    print(f"   → Error: {response.text}")
                    fail_count += 1

                sleep(0.2)

            except requests.exceptions.RequestException as e:
                print(f"[{i}/{len(products)}] ❗ Exception for {product['name']}: {e}")
                fail_count += 1

    print("\nUpload Summary:")
    print(f"✅ Success: {success_count}")
    print(f"❌ Failed: {fail_count}")


if __name__ == '__main__':
    upload_product()
