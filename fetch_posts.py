import requests
import json

TELEGRAM_BOT_TOKEN = 'your_bot_token'
CHANNEL_ID = '@your_channel_name'
OUTPUT_FILE = 'posts.json'

def get_channel_messages():
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    response = requests.get(url)
    messages = response.json().get('result', [])
    
    posts = []
    for msg in messages:
        if 'channel_post' in msg:
            post = {
                'date': msg['channel_post']['date'],
                'text': msg['channel_post'].get('text', ''),
                'photos': [p['file_id'] for p in msg['channel_post'].get('photo', [])]
            }
            posts.append(post)
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(posts[-10:], f)  # Save last 10 posts

if __name__ == "__main__":
    get_channel_messages()