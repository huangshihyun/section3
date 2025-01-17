import requests
import logging

def fetch_news_data(query, api_key):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
    response = requests.get(url)
    return response.json()

import requests
import logging

logger = logging.getLogger(__file__)

def generate_gmini_story(prompt, user_id, gmini_api_key):
    url = "https://api.gemini.example.com/v1/generate_story"  # 确保这是正确的URL
    headers = {"Authorization": f"Bearer {gmini_api_key}"}
    payload = {"prompt": prompt, "user_id": user_id}

    logger.info(f"Sending request to Gemini API with prompt: {prompt}")
    try:
        response = requests.post(url, headers=headers, json=payload)
        logger.info(f"Gemini API response status: {response.status_code}")
        logger.info(f"Gemini API response body: {response.text}")
        if response.status_code == 200:
            logger.info(f"Gemini API response: {response.json()}")
            return response.json()
        else:
            logger.error(f"Error from Gemini API: {response.text}")
            return None
    except Exception as e:
        logger.error(f"Exception when calling Gemini API: {str(e)}")
        return None


