import requests

def fetch_news_data(query, api_key):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
    response = requests.get(url)
    return response.json()


import requests
import logging
def generate_gmini_story(prompt, user_id, gmini_api_key):
    url = "https://api.gemini.example.com/v1/generate_story"
    headers = {"Authorization": f"Bearer {gmini_api_key}"}
    payload = {"prompt": prompt, "user_id": user_id}

    try:
        response = requests.post(url, headers=headers, json=payload)
        logger.info(f"Gemini API response status: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Error from Gemini API: {response.text}")
            return None
    except Exception as e:
        logger.error(f"Exception when calling Gemini API: {str(e)}")
        return None

