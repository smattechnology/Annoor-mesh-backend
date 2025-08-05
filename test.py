from time import sleep

import requests

DEV_URL = "http://localhost:1024"
PRO_URL = "https://api.nuraloom.xyz"

BASE_URL = DEV_URL

PRO_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxNDc5MDg5Ny1kYTk5LTQ2NGQtOTljMy0wNmYyMWUxOTBjNzkiLCJleHAiOjE3NTQzOTQ5MzZ9.NyJUmjiO8ATe5llAswc7wPKl7-waacpPYJHPY6N4j1E"
DEV_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyNGY4NGE0YS0wZWE4LTQxY2ItOTRhYi0yZGIzNGRhNDE1YzQiLCJleHAiOjE3NTQzOTc5ODV9.p9QNJyKgQQIHRotUai3tVUHTZJFlEDjbVWt6P4Fh6uo"
ACCESS_TOKEN = DEV_ACCESS_TOKEN

# UNITS = [
#     {
#         "id": "030c22ab-82e9-463f-9c93-0d4a6c17dfe5",
#         "label": "ডজন (Dozen)",
#         "icon": "📦",
#         "created_at": "2025-08-05T11:09:36",
#         "updated_at": "2025-08-05T11:09:36"
#     },
#     {
#         "id": "11eec59e-99ac-421e-a213-0a963c124d97",
#         "label": "বান্ডিল (Bundle)",
#         "icon": "🎋",
#         "created_at": "2025-08-05T11:09:36",
#         "updated_at": "2025-08-05T11:09:36"
#     },
#     {
#         "id": "5788e52f-937d-49f9-8391-4fa2b525f81b",
#         "label": "মিলিলিটার (ml)",
#         "icon": "🥛",
#         "created_at": "2025-08-05T11:09:35",
#         "updated_at": "2025-08-05T11:09:35"
#     },
#     {
#         "id": "6c54343b-89a1-4052-91d5-f83aa9cbbef9",
#         "label": "লিটার (L)",
#         "icon": "🥛",
#         "created_at": "2025-08-05T11:09:35",
#         "updated_at": "2025-08-05T11:09:35"
#     },
#     {
#         "id": "8f122d5d-2d26-4386-980e-ad383b97607a",
#         "label": "কেজি (Kg)",
#         "icon": "⚖️",
#         "created_at": "2025-08-04T08:19:59",
#         "updated_at": "2025-08-04T08:19:59"
#     },
#     {
#         "id": "a122b8a8-485b-4c8b-882d-2f24bc88ecf3",
#         "label": "প্যাকেট (Packet)",
#         "icon": "📦",
#         "created_at": "2025-08-05T11:09:36",
#         "updated_at": "2025-08-05T11:09:36"
#     },
#     {
#         "id": "e6493d17-df61-4b46-bcd8-c46ec51d4a6f",
#         "label": "পিস (Pcs)",
#         "icon": "📦",
#         "created_at": "2025-08-05T11:09:35",
#         "updated_at": "2025-08-05T11:09:35"
#     },
#     {
#         "id": "f9fb1bd6-751c-45d2-a2a4-b344339e530c",
#         "label": "গ্রাম (g)",
#         "icon": "⚖️",
#         "created_at": "2025-08-05T11:09:35",
#         "updated_at": "2025-08-05T11:09:35"
#     }
# ]

# CATEGORIES = [
#     {
#         "id": "15b4941f-5acb-460d-aead-fdc33e059367",
#         "label": "শাক (Leafy Greens)",
#         "icon": "🥬",
#         "created_at": "2025-08-05T11:38:55",
#         "updated_at": "2025-08-05T11:38:55"
#     },
#     {
#         "id": "304618f2-d571-47bf-b376-d729717cc250",
#         "label": "তেল/মশলা (Oil/Spices)",
#         "icon": "🫒",
#         "created_at": "2025-08-05T11:38:55",
#         "updated_at": "2025-08-05T11:38:55"
#     },
#     {
#         "id": "39319d5f-8fd0-4750-a573-7a35488b4b18",
#         "label": "মাছ (Fish)",
#         "icon": "🐟",
#         "created_at": "2025-08-05T11:38:56",
#         "updated_at": "2025-08-05T11:38:56"
#     },
#     {
#         "id": "39f5aaa9-e4ba-487a-8350-9ad2d7c7f5d7",
#         "label": "নিত্যপ্রয়োজনীয় খাদ্যপণ্য (Staples)",
#         "icon": "🛒",
#         "created_at": "2025-08-05T11:38:56",
#         "updated_at": "2025-08-05T11:38:56"
#     },
#     {
#         "id": "ec0cd58d-fff3-4770-91c6-9ece18e13aeb",
#         "label": "মাংস (Meat)",
#         "icon": "🍗",
#         "created_at": "2025-08-05T11:38:56",
#         "updated_at": "2025-08-05T11:38:56"
#     },
#     {
#         "id": "fb52d6d9-1a07-4e95-9e1c-df075cc20db3",
#         "label": "সবজি (Vegetables)",
#         "icon": "🥕",
#         "created_at": "2025-08-05T11:38:56",
#         "updated_at": "2025-08-05T11:38:56"
#     }
# ]

PRODUCTS = [
    {
        "id": 1,
        "title": "তেল/মশলা",
        "items": [
            {
                "id": 1,
                "name": "সয়াবিন তেল",
                "price": 100,
                "unite": "লিটার",
                "bld": {"breakfast": True, "lunch": False, "dinner": True, "editable": False},
                "pp": 10,
            },
            {
                "id": 2,
                "name": "সরিষার তেল",
                "price": 80,
                "unite": "লিটার",
                "bld": {"breakfast": False, "lunch": True, "dinner": False, "editable": True},
            },
            {
                "id": 3,
                "name": "পাম তেল",
                "price": 90,
                "unite": "লিটার",
                "bld": {"breakfast": True, "lunch": True, "dinner": False, "editable": False},
            },
            {
                "id": 4,
                "name": "কোকোনাট তেল",
                "price": 120,
                "unite": "লিটার",
                "bld": {"breakfast": False, "lunch": False, "dinner": True, "editable": True},
            },
            {
                "id": 5,
                "name": "ঘি",
                "price": 200,
                "unite": "লিটার",
                "bld": {"breakfast": True, "lunch": False, "dinner": False, "editable": True},
            },
            {
                "id": 6,
                "name": "বাটার",
                "price": 150,
                "unite": "লিটার",
                "bld": {"breakfast": False, "lunch": True, "dinner": True, "editable": False},
            },
            {
                "id": 7,
                "name": "চিনি",
                "price": 50,
                "unite": "কেজি",
                "bld": {"breakfast": True, "lunch": True, "dinner": True, "editable": True},
            },
            {
                "id": 8,
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
        ],
    },
    {
        "id": 2,
        "title": "শাক",
        "items": [
            {
                "id": 9,
                "name": "পালং শাক",
                "price": 20,
                "unite": "কেজি",
                "bld": {"breakfast": False, "lunch": True, "dinner": True, "editable": True},
            },
            {
                "id": 10,
                "name": "লাল শাক",
                "price": 25,
                "unite": "কেজি",
                "bld": {"breakfast": True, "lunch": False, "dinner": False, "editable": True},
            },
            {
                "id": 11,
                "name": "কলমি শাক",
                "price": 18,
                "unite": "কেজি",
                "bld": {"breakfast": False, "lunch": True, "dinner": False, "editable": True},
            },
            {
                "id": 12,
                "name": "পুঁই শাক",
                "price": 22,
                "unite": "কেজি",
                "bld": {"breakfast": True, "lunch": False, "dinner": True, "editable": True},
            },
            {
                "id": 13,
                "name": "ঝিঙ্গে শাক",
                "price": 28,
                "unite": "কেজি",
                "bld": {"breakfast": True, "lunch": True, "dinner": False, "editable": True},
            },
            {
                "id": 14,
                "name": "নটে শাক",
                "price": 19,
                "unite": "কেজি",
                "bld": {"breakfast": False, "lunch": False, "dinner": True, "editable": True},
            },
            {
                "id": 15,
                "name": "শ্যাম শাক",
                "price": 30,
                "unite": "কেজি",
                "bld": {"breakfast": True, "lunch": True, "dinner": True, "editable": True},
            },
            {
                "id": 16,
                "name": "সরিষা শাক",
                "price": 26,
                "unite": "কেজি",
                "bld": {"breakfast": False, "lunch": True, "dinner": False, "editable": True},
            },
        ],
    },
    {
        "id": 3,
        "title": "সবজি",
        "items": [
            {
                "id": 17,
                "name": "আলু",
                "price": 30,
                "unite": "কেজি",
                "bld": {"breakfast": True, "lunch": True, "dinner": True, "editable": True},
            },
            {
                "id": 18,
                "name": "বেগুন",
                "price": 35,
                "unite": "কেজি",
                "bld": {"breakfast": False, "lunch": True, "dinner": False, "editable": True},
            },
            {
                "id": 19,
                "name": "টমেটো",
                "price": 40,
                "unite": "কেজি",
                "bld": {"breakfast": True, "lunch": True, "dinner": True, "editable": True},
            },
            {
                "id": 20,
                "name": "শসা",
                "price": 25,
                "unite": "কেজি",
                "bld": {"breakfast": True, "lunch": False, "dinner": False, "editable": True},
            },
            {
                "id": 21,
                "name": "করলা",
                "price": 32,
                "unite": "কেজি",
                "bld": {"breakfast": False, "lunch": True, "dinner": True, "editable": True},
            },
            {
                "id": 22,
                "name": "মিষ্টি কুমড়া",
                "price": 27,
                "unite": "কেজি",
                "bld": {"breakfast": False, "lunch": False, "dinner": True, "editable": True},
            },
            {
                "id": 23,
                "name": "পটল",
                "price": 34,
                "unite": "কেজি",
                "bld": {"breakfast": True, "lunch": False, "dinner": False, "editable": True},
            },
            {
                "id": 24,
                "name": "কাঁচা মরিচ",
                "price": 80,
                "unite": "কেজি",
                "bld": {
                    "breakfast": False,
                    "lunch": False,
                    "dinner": False,
                    "editable": False,
                },
            },
        ],
    },
    {
        "id": 4,
        "title": "মাছ",
        "items": [
            {
                "id": 25,
                "name": "রুই মাছ",
                "price": 250,
                "unite": "কেজি",
                "bld": {"breakfast": False, "lunch": True, "dinner": True, "editable": True},
            },
            {
                "id": 26,
                "name": "ইলিশ মাছ",
                "price": 800,
                "unite": "কেজি",
                "bld": {"breakfast": True, "lunch": False, "dinner": False, "editable": False},
            },
            {
                "id": 27,
                "name": "কাতলা",
                "price": 300,
                "unite": "কেজি",
                "bld": {"breakfast": True, "lunch": True, "dinner": False, "editable": True},
            },
            {
                "id": 28,
                "name": "পাবদা",
                "price": 350,
                "unite": "কেজি",
                "bld": {"breakfast": False, "lunch": True, "dinner": True, "editable": True},
            },
            {
                "id": 29,
                "name": "টেংরা",
                "price": 400,
                "unite": "কেজি",
                "bld": {"breakfast": True, "lunch": False, "dinner": False, "editable": True},
            },
            {
                "id": 30,
                "name": "চিংড়ি",
                "price": 600,
                "unite": "কেজি",
                "bld": {"breakfast": False, "lunch": True, "dinner": True, "editable": True},
            },
            {
                "id": 31,
                "name": "মাগুর মাছ",
                "price": 450,
                "unite": "কেজি",
                "bld": {"breakfast": True, "lunch": True, "dinner": False, "editable": True},
            },
            {
                "id": 32,
                "name": "সিলভার কার্প",
                "price": 220,
                "unite": "কেজি",
                "bld": {"breakfast": False, "lunch": False, "dinner": True, "editable": True},
            },
        ],
    },
    {
        "id": 5,
        "title": "মাংস",
        "items": [
            {
                "id": 33,
                "name": "গরুর মাংস",
                "price": 700,
                "unite": "কেজি",
                "bld": {"breakfast": False, "lunch": False, "dinner": True, "editable": True},
            },
            {
                "id": 34,
                "name": "মুরগি",
                "price": 180,
                "unite": "কেজি",
                "bld": {"breakfast": True, "lunch": True, "dinner": True, "editable": True},
            },
            {
                "id": 35,
                "name": "খাসির মাংস",
                "price": 850,
                "unite": "কেজি",
                "bld": {"breakfast": False, "lunch": True, "dinner": False, "editable": True},
            },
            {
                "id": 36,
                "name": "হাঁস",
                "price": 400,
                "unite": "কেজি",
                "bld": {"breakfast": True, "lunch": False, "dinner": True, "editable": True},
            },
            {
                "id": 37,
                "name": "মুরগি লেগ পিস",
                "price": 200,
                "unite": "কেজি",
                "bld": {"breakfast": False, "lunch": True, "dinner": False, "editable": True},
            },
            {
                "id": 38,
                "name": "চিকেন উইংস",
                "price": 210,
                "unite": "কেজি",
                "bld": {"breakfast": False, "lunch": False, "dinner": True, "editable": True},
            },
            {
                "id": 39,
                "name": "মুরগি বুকের মাংস",
                "price": 220,
                "unite": "কেজি",
                "bld": {"breakfast": True, "lunch": True, "dinner": True, "editable": True},
            },
            {
                "id": 40,
                "name": "হাড় ছাড়া মাংস",
                "price": 260,
                "unite": "কেজি",
                "bld": {"breakfast": False, "lunch": True, "dinner": True, "editable": True},
            },
        ],
    },
    {
        "id": 6,
        "title": "নিত্যপ্রয়োজনীয় খাদ্যপণ্য",
        "items": [
            {
                "id": 41,
                "name": "চাল",
                "price": 60,
                "unite": "কেজি",
                "bld": {"breakfast": True, "lunch": True, "dinner": True, "editable": False},
            },
            {
                "id": 42,
                "name": "ডাল",
                "price": 90,
                "unite": "কেজি",
                "bld": {"breakfast": False, "lunch": False, "dinner": True, "editable": True},
            },
            {
                "id": 43,
                "name": "চিনি",
                "price": 55,
                "unite": "কেজি",
                "bld": {"breakfast": True, "lunch": False, "dinner": True, "editable": False},
            },
            {
                "id": 44,
                "name": "আটা",
                "price": 45,
                "unite": "কেজি",
                "bld": {"breakfast": False, "lunch": True, "dinner": True, "editable": True},
            },
            {
                "id": 45,
                "name": "ময়দা",
                "price": 50,
                "unite": "কেজি",
                "bld": {"breakfast": True, "lunch": True, "dinner": False, "editable": True},
            },
            {
                "id": 46,
                "name": "চিড়া",
                "price": 35,
                "unite": "কেজি",
                "bld": {"breakfast": True, "lunch": False, "dinner": False, "editable": True},
            },
            {
                "id": 47,
                "name": "সুজি",
                "price": 40,
                "unite": "কেজি",
                "bld": {"breakfast": False, "lunch": True, "dinner": False, "editable": True},
            },
            {
                "id": 48,
                "name": "মুড়ি",
                "price": 30,
                "unite": "কেজি",
                "bld": {"breakfast": True, "lunch": False, "dinner": False, "editable": True},
            },
        ],
    },
]


def get_all_category():
    get_url = f"{BASE_URL}/product/get/category/all"
    cookies = {
        "access_token": ACCESS_TOKEN
    }
    with requests.Session() as session:
        try:
            response = session.get(get_url, cookies=cookies)
            if response.status_code == 200:
                return response.json()
            else:
                print(response.text)
        except requests.exceptions.RequestException as e:
            print(e)

def get_all_unite():
    get_url = f"{BASE_URL}/product/get/unite/all"
    cookies = {
        "access_token": ACCESS_TOKEN
    }
    with requests.Session() as session:
        try:
            response = session.get(get_url, cookies=cookies)
            if response.status_code == 200:
                return response.json()
            else:
                print(response.text)
        except requests.exceptions.RequestException as e:
            print(e)


def get_all_user():
    url = 'https://dummyjson.com/users?limit=100'
    post_url = f"{BASE_URL}/auth/register"
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
    post_url = f"{BASE_URL}/product/add/category"
    cookies = {
        "access_token": ACCESS_TOKEN
    }
    categories = [
        {
            "value": "oil_spices",
            "label": "তেল/মশলা (Oil/Spices)",
            "icon": "🫒"
        },
        {
            "value": "greens",
            "label": "শাক (Leafy Greens)",
            "icon": "🥬"
        },
        {
            "value": "vegetables",
            "label": "সবজি (Vegetables)",
            "icon": "🥕"
        },
        {
            "value": "fish",
            "label": "মাছ (Fish)",
            "icon": "🐟"
        },
        {
            "value": "meat",
            "label": "মাংস (Meat)",
            "icon": "🍗"
        },
        {
            "value": "staples",
            "label": "নিত্যপ্রয়োজনীয় খাদ্যপণ্য (Staples)",
            "icon": "🛒"
        }
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
    post_url = f"{BASE_URL}/product/add/unite"

    cookies = {
        "access_token": ACCESS_TOKEN
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
    post_url = f"{BASE_URL}/product/add/"

    cookies = {
        "access_token": ACCESS_TOKEN
    }

    success_count = 0
    fail_count = 0

    UNITS  = get_all_unite()
    CATEGORIES = get_all_category()

    with requests.Session() as session:
        for group_index, group in enumerate(PRODUCTS, 1):
            category_label = group["title"]

            # Find matching category_id by label (partial match with CATEGORIES)
            matched_category = next(
                (cat for cat in CATEGORIES if cat["label"].startswith(category_label)), None
            )

            if not matched_category:
                print(f"[{group_index}] ❌ No matching category for: {category_label}")
                continue

            category_id = matched_category["id"]

            for item_index, product in enumerate(group["items"], 1):
                unit_label = product["unite"]
                matched_unit = next(
                    (u for u in UNITS if u["label"].startswith(unit_label)), None
                )

                if not matched_unit:
                    print(f"[{group_index}.{item_index}] ❌ No matching unit for: {unit_label}")
                    continue

                unite_id = matched_unit["id"]

                payload = {
                    "name": product.get("name"),
                    "price": str(product.get("price")),
                    "unite_id": unite_id,
                    "category_id": category_id,
                }

                try:
                    response = session.post(post_url, json=payload, cookies=cookies)

                    if response.status_code == 201:
                        print(f"[{group_index}.{item_index}] ✅ Uploaded: {product['name']}")
                        success_count += 1
                    elif response.status_code == 400 and "already exists" in response.text:
                        print(f"[{group_index}.{item_index}] ⚠️ Already exists: {product['name']}")
                    else:
                        print(
                            f"[{group_index}.{item_index}] ❌ Failed: {product['name']}, Status: {response.status_code}")
                        print(f"   → Error: {response.text}")
                        fail_count += 1

                    sleep(0.2)

                except requests.exceptions.RequestException as e:
                    print(f"[{group_index}.{item_index}] ❗ Exception for {product['name']}: {e}")
                    fail_count += 1

    print("\nUpload Summary:")
    print(f"✅ Success: {success_count}")
    print(f"❌ Failed: {fail_count}")


if __name__ == '__main__':
    upload_product()
