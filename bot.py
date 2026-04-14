import requests
import os

PAGE_ID = os.environ.get("FB_PAGE_ID")
ACCESS_TOKEN = os.environ.get("FB_PAGE_ACCESS_TOKEN")

# Step 1: Get recent posts
url = f"https://graph.facebook.com/{PAGE_ID}/posts?access_token={ACCESS_TOKEN}"
response = requests.get(url).json()

if "data" not in response:
    print("No posts found or error:", response)
    exit()

posts = response["data"]

for post in posts[:3]:  # check last 3 posts
    post_id = post["id"]

    # Step 2: Get comments
    comment_url = f"https://graph.facebook.com/{post_id}/comments?access_token={ACCESS_TOKEN}"
    comments = requests.get(comment_url).json()

    if "data" not in comments:
        continue

    for comment in comments["data"]:
        comment_id = comment["id"]
        message = comment.get("message", "")

        # Simple filter
        if len(message) < 5:
            continue

        # Step 3: Reply
        reply = "Interesting point. This is exactly what Economy on Steroids explores—why things feel more expensive even when nothing seems to change."

        reply_url = f"https://graph.facebook.com/{comment_id}/comments"
        requests.post(reply_url, data={
            "message": reply,
            "access_token": ACCESS_TOKEN
        })

        print(f"Replied to comment: {message}")
