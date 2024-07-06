import requests

def fetch_news_data(query, api_key):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
    response = requests.get(url)
    return response.json()

import requests

def generate_gmini_story(prompt, user_id, gmini_api_key):
    url = "https://api.gemini.example.com/v1/generate_story"
    headers = {"Authorization": f"Bearer {gmini_api_key}"}
    payload = {"prompt": prompt, "user_id": user_id}
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

