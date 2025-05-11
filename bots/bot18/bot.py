# === bot.py ===

import tweepy
from nba_api.stats.endpoints import leaguedashplayerstats
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

# Tweepy v2 client for posting
client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

# Tweepy v1.1 API for media upload
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api_v1 = tweepy.API(auth)

# ======================= #
#    MAIN BOT LOGIC       #
# ======================= #

def get_top_playoff_scorers():
    try:
        player_stats = leaguedashplayerstats.LeagueDashPlayerStats(
            season_type_all_star='Playoffs',
            date_from_nullable='06/06/2025',
            date_to_nullable='06/23/2025'
        ).get_normalized_dict()

        players = player_stats.get('LeagueDashPlayerStats', [])
        players_sorted = sorted(players, key=lambda x: x['PTS'], reverse=True)
        return players_sorted[:4]  # Top 4 for tweet
    except Exception as e:
        print("Error fetching playoff scoring leaders:", e)
        return []

def compose_tweet(top4):
    today = datetime.now().strftime("%B %d, %Y")
    tweet = f"👑🔥 NBA Finals Scoring Leaders ({today})\n\n"
    medals = ["🥇", "🥈", "🥉"]

    for idx, player in enumerate(top4, 1):
        name = player['PLAYER_NAME']
        points = int(player['PTS'])

        if idx <= 3:
            medal = medals[idx-1]
            tweet += f"{medal} {name} – {points} PTS\n"
        else:
            tweet += f"{idx}. {name} – {points} PTS\n"

    tweet += "\n#NBAFinals #CourtKingsHQ"
    return tweet

def get_top3_media_ids(top3):
    media_ids = []
    base_dir = os.path.dirname(os.path.abspath(__file__))
    img_dir = os.path.join(base_dir, "img")

    for player in top3:
        first_name = player['PLAYER_NAME'].split()[0].lower()
        image_path = os.path.join(img_dir, f"{first_name}.png")

        print(f"🔍 Looking for image at: {image_path}")

        if os.path.exists(image_path):
            try:
                media = api_v1.media_upload(filename=image_path)
                media_ids.append(media.media_id_string)
                print(f"✅ Uploaded image: {image_path}")
            except Exception as e:
                print(f"❌ Failed to upload {image_path}: {e}")
        else:
            print(f"⚠️ Image not found: {image_path}")
    return media_ids

# ======================= #
#        MAIN RUN         #
# ======================= #

def run_bot():
    print("🤖 Running NBA Finals Scoring Leaders Bot...")

    top4 = get_top_playoff_scorers()
    if not top4:
        print("🔝 No data found. Try again later.")
        return

    tweet = compose_tweet(top4)
    media_ids = get_top3_media_ids(top4[:3])  # Only top 3 get headshots

    # Print preview
    print("\n=== TWEET PREVIEW ===\n")
    print(tweet)
    print("\n=== IMAGE IDS ===")
    print(media_ids)
    print("\n=== END ===\n")

    # Post to Twitter
    if media_ids:
        client.create_tweet(text=tweet, media_ids=media_ids)
    else:
        client.create_tweet(text=tweet)

if __name__ == "__main__":
    run_bot()
