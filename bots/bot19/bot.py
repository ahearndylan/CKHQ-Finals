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
    "Jayson Tatum",
    "Jaylen Brown",
    "Luka Dončić",
    "Other (comment below)"
]

IMAGE_PATHS = [
    "img/jayson.jpeg",
    "img/jaylen.jpeg",
    "img/luka.jpeg"
]

# ======================= #
#        BOT LOGIC        #
# ======================= #

def run_bot():
    print("🤖 Running Finals MVP Poll Bot...")

    # Upload headshots and get media IDs
    media_ids = []
    for path in IMAGE_PATHS:
        try:
            media = api.media_upload(filename=path)
            media_ids.append(media.media_id_string)
            print(f"✅ Uploaded {path}")
        except Exception as e:
            print(f"❌ Failed to upload {path}: {e}")

    # Format tweet text
    today = datetime.now().strftime("%B %d, %Y")
    tweet_text = (
        f"🏆 After Game 1 – Who's your NBA Finals MVP so far? ({today})\n\n"
        "Vote below ⬇️"
    )

    try:
        # Post tweet with poll and media
        client.create_tweet(
            text=tweet_text,
            poll_options=POLL_OPTIONS,
            poll_duration_minutes=1440,
            media_ids=media_ids
        )
        print("✅ Tweet posted successfully.")
    except Exception as e:
        print("❌ Error posting tweet:", e)

if __name__ == "__main__":
    run_bot()
