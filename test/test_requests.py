import requests

BASE_URL = "http://localhost:5000"

def register_user(username, email, password):
    res = requests.post(f"{BASE_URL}/auth/register", json={
        "username": username,
        "email": email,
        "password": password
    })
    print("Register:", res.status_code, res.json())

def login_user(email, password):
    res = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": password
    })
    print("Login:", res.status_code, res.json())
    return res.json().get("access_token")

def create_post(token, content):
    res = requests.post(f"{BASE_URL}/posts/", json={"content": content},
                        headers={"Authorization": f"Bearer {token}"})
    print("Create Post:", res.status_code, res.json())

def get_posts():
    res = requests.get(f"{BASE_URL}/posts/")
    print("Get Posts:", res.status_code, res.json())
    return res.json()

def follow_user(token, user_id):
    res = requests.post(f"{BASE_URL}/users/follow/{user_id}",
                        headers={"Authorization": f"Bearer {token}"})
    print("Follow:", res.status_code, res.json())

def add_comment(token, content, post_id):
    res = requests.post(f"{BASE_URL}/comments/", json={"content": content, "post_id": post_id},
                        headers={"Authorization": f"Bearer {token}"})
    print("Add Comment:", res.status_code, res.json())

def get_comments(post_id):
    res = requests.get(f"{BASE_URL}/comments/{post_id}")
    print("Get Comments:", res.status_code, res.json())

def update_bio(token, bio):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"bio": bio}
    response = requests.patch(f"{BASE_URL}/users/me", headers=headers, json=data)
    print("Update Bio:", response.status_code, response.json())

def test_all():
    register_user("test1", "test1@example.com", "123456")
    register_user("test2", "test2@example.com", "123456")

    token1 = login_user("test1@example.com", "123456")
    token2 = login_user("test2@example.com", "123456")

    create_post(token1, "Hello from test1!")
    create_post(token2, "Hello from test2!")

    posts_data = get_posts()
    posts = posts_data.get("posts", [])
    if posts:
        first_post_id = posts[0]['id']
        add_comment(token2, "Nice post, test1!", first_post_id)
        get_comments(first_post_id)

    follow_user(token2, 1)

    update_bio(token2, "I'm a backend developer from Türkiye!")


if __name__ == "__main__":
    test_all()