import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = '8009608932:AAHhv1IlCnl13ADRn7W7lJTtFiGwk27a93I'
CHANNEL_ID = "@algorithmsgang"

def get_all_messages():
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    all_messages = []
    offset = 0
    
    print(f"Starting fetch for channel: {CHANNEL_ID}")
    
    while True:
        params = {'offset': offset, 'limit': 100, 'timeout': 30}
        try:
            response = requests.get(url, params=params).json()
            print(f"Batch response: {response}")
            
            if not response.get('result'):
                print("No more results")
                break
                
            for update in response['result']:
                if 'channel_post' in update:
                    chat_id = str(update['channel_post']['chat']['id'])
                    # Handle both numeric IDs and usernames
                    if (CHANNEL_ID.startswith('@') and (update['channel_post']['chat']['username'] == CHANNEL_ID[1:]) or \
                       (CHANNEL_ID.startswith('-100') and (chat_id == CHANNEL_ID.replace('-100', ''))):
                        all_messages.append({
                            'date': update['channel_post']['date'],
                            'text': update['channel_post'].get('text', ''),
                            'photos': [p['file_id'] for p in update['channel_post'].get('photo', [])]
                        })
                        offset = update['update_id'] + 1
        except Exception as e:
            print(f"Error: {str(e)}")
            break
    
    print(f"Found {len(all_messages)} messages")
    return sorted(all_messages, key=lambda x: x['date'])

if __name__ == "__main__":
    messages = get_all_messages()
    with open('posts.json', 'w') as f:
        json.dump(messages, f, indent=2)
    print("posts.json updated successfully")
