import requests
import time
from random import choice

API_URL = 'https://api.telegram.org/bot'
API_CAT_URL = 'https://api.thecatapi.com/v1/images/search'
API_DOG_URL = 'https://random.dog/woof.json'
API_FOX_URL = ' https://randomfox.ca/floof/'
API_GIF_URL = 'https://yesno.wtf/api?force=yes'
BOT_TOKEN = '6460540408:AAHkYNEg2skgqOBKKhHjfAacLjMq-V4tdc0'
ERROR_TEXT = 'Здесь должны были быть котики'
MAX_COUNTER = 100
api_url = [API_DOG_URL, API_FOX_URL, API_CAT_URL,API_GIF_URL]

offset = -2
counter = 0
response = requests.Response
link = str

while counter < MAX_COUNTER:
    print('attempt=', counter)
    random_url = choice(api_url)

    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            response = requests.get(random_url)
            if response.status_code == 200 and random_url == API_CAT_URL:
                link = response.json()[0]['url']
                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={link}')
            elif response.status_code == 200 and random_url == API_FOX_URL:
                link = response.json()['image']
                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={link}')
            elif response.status_code == 200 and random_url == API_DOG_URL:
                link = response.json()['url']
                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={link}')
            elif response.status_code == 200 and random_url == API_GIF_URL:
                link = response.json()['image']
                requests.get(f'{API_URL}{BOT_TOKEN}/sendAnimation?chat_id={chat_id}&animation={link}')
            else:
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')

    time.sleep(1)
    counter += 1
