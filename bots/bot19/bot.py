import tweepy
from datetime import datetime
import os

# ======================= #
# TWITTER AUTHENTICATION  #
# ======================= #
bearer_token = "AAAAAAAAAAAAAAAAAAAAAPztzwEAAAAAvBGCjApPNyqj9c%2BG7740SkkTShs%3DTCpOQ0DMncSMhaW0OA4UTPZrPRx3BHjIxFPzRyeoyMs2KHk6hM"
api_key = "uKyGoDr5LQbLvu9i7pgFrAnBr"
api_secret = "KGBVtj1BUmAEsyoTmZhz67953ItQ8TIDcChSpodXV8uGMPXsoH"
access_token = "1901441558596988929-WMdEPOtNDj7QTJgLHVylxnylI9ObgD"
access_token_secret = "9sf83R8A0MBdijPdns6nWaG7HF47htcWo6oONPmMS7o98"


# Create both Client and API (for media uploads)
client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# ======================= #
#        CONFIG           #
# ======================= #

POLL_OPTIONS = [
    "Tyrese Haliburton",
    "Shai Gilgeous-Alexander",
    "Pascal Siakam",
    "Other (comment below)"
]

IMAGE_PATHS = [
    "img/tyrese.png",
    "img/shai.png",
    "img/pascal.png"
]

# ======================= #
#        BOT LOGIC        #
# ======================= #

def run_bot():
    print("🤖 Running Finals MVP Poll Bot...")

    today = datetime.now().strftime("%B %d, %Y")

    # Step 1: Post the poll first
    poll_text = (
        f"🏆 After Game 1 – Who's your NBA Finals MVP so far? \n\n"
        "Vote below ⬇️"
    )

    try:
        poll_tweet = client.create_tweet(
            text=poll_text,
            poll_options=POLL_OPTIONS,
            poll_duration_minutes=1440
        )
        poll_tweet_id = poll_tweet.data["id"]
        print(f"✅ Poll tweet posted (ID: {poll_tweet_id})")
    except Exception as e:
        print(f"❌ Failed to post poll tweet: {e}")
        return

    # Step 2: Upload images and reply with them
    media_ids = []
    for path in IMAGE_PATHS:
        try:
            media = api.media_upload(filename=path)
            media_ids.append(media.media_id_string)
            print(f"✅ Uploaded {path}")
        except Exception as e:
            print(f"❌ Failed to upload {path}: {e}")

    if not media_ids:
        print("⚠️ No media uploaded. Skipping image reply.")
        return

    try:
        reply_text = "📸 MVP Candidates:"
        client.create_tweet(
            text=reply_text,
            media_ids=media_ids,
            in_reply_to_tweet_id=poll_tweet_id
        )
        print("✅ Image reply posted successfully.")
    except Exception as e:
        print(f"❌ Failed to post image reply: {e}")


if __name__ == "__main__":
    run_bot()
