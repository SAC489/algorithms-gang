import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

TELEGRAM_BOT_TOKEN = '8009608932:AAGfQj9SL29HZx8aRCFL6of2-wnCXgOBO3c'
CHANNEL_ID = '@algorithmsgang'

def get_all_messages():
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    all_messages = []
    offset = 0
    
    while True:
        params = {'offset': offset, 'limit': 100}
        response = requests.get(url, params=params).json()
        
        if not response.get('result'):
            break
            
        for update in response['result']:
            if 'channel_post' in update and str(update['channel_post']['chat']['id']) == CHANNEL_ID.replace('-100', ''):
                all_messages.append({
                    'id': update['update_id'],
                    'date': update['channel_post']['date'],
                    'text': update['channel_post'].get('text', ''),
                    'photos': [p['file_id'] for p in update['channel_post'].get('photo', [])]
                })
                offset = update['update_id'] + 1
    
    # Sort by date (oldest first)
    all_messages.sort(key=lambda x: x['date'])
    return all_messages

if __name__ == "__main__":
    messages = get_all_messages()
    with open('posts.json', 'w') as f:
        json.dump(messages, f, indent=2)
