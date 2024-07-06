import os
import sys
import logging
import requests
from fastapi import FastAPI, HTTPException, Request
from linebot.v3.webhook import WebhookParser
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from utils import fetch_news_data, generate_gmini_story

if os.getenv('API_ENV') != 'production':
    from dotenv import load_dotenv
    load_dotenv()

logging.basicConfig(level=os.getenv('LOG', 'INFO'))
logger = logging.getLogger(__file__)

app = FastAPI()

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None or channel_access_token is None:
    logger.error('Specify LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN as environment variables.')
    sys.exit(1)

configuration = Configuration(access_token=channel_access_token)
async_api_client = AsyncApiClient(configuration)
line_bot_api = AsyncMessagingApi(async_api_client)
parser = WebhookParser(channel_secret)

news_api_key = os.getenv('NEWS_API_KEY')
gmini_api_key = os.getenv('GMINI_API_KEY')

@app.get("/health")
async def health():
    return 'ok'

import random

async def process_user_message(message, user_id):
    """
    處理用戶發送的消息並返回相應的回應。
    """
    if "新聞" in message:
        # Extract keyword from the message
        keyword = message.replace("新聞", "").strip()
        if not keyword:
            return "請提供要查詢的新聞關鍵字，例如「性別平等新聞」或「台積電新聞」。"
        
        # Fetch news data based on the keyword
        news_response = fetch_news_data(keyword, news_api_key)
        if news_response and news_response.get("status") == "ok":
            articles = news_response.get("articles", [])
            if articles:
                random_article = random.choice(articles)
                return f"最新新聞：\n\n標題: {random_article['title']}\n\n描述: {random_article['description']}\n\n更多詳情: {random_article['url']}"
        return "目前沒有相關新聞。"
    elif "故事" in message:
        # Extract keyword from the message
        keyword = message.replace("故事", "").strip()
        if not keyword:
            return "請提供要編寫故事的關鍵字，例如「性別平等故事」或「朋友故事」。"

        # Fetch story from Gemini API based on the keyword
        logger.info(f"Fetching story for keyword: {keyword}")
        story_response = generate_gmini_story(keyword, user_id, gmini_api_key)
        if story_response:
            logger.info(f"Story generated: {story_response}")
            return story_response.get("story", "無法生成故事。")
        logger.error("Failed to generate story.")
        return "生成故事時出現錯誤。"
    else:
        return "請問你想了解什麼？可以說「新聞」或「故事」。"

@app.post("/webhooks/line")
async def handle_callback(request: Request):
    """
    處理來自 LINE Bot 的 Webhook 回調請求。
    """
    signature = request.headers['X-Line-Signature']
    body = await request.body()
    body = body.decode()

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        logger.error("Invalid signature")
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        logging.info(f"Received event: {event}")
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessageContent):
            continue
        
        text = event.message.text
        user_id = event.source.user_id

        reply_message = await process_user_message(text, user_id)
        await line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_message)]
            )
        )

    return 'OK'

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get('PORT', default=8080))
    debug = os.environ.get('API_ENV', default='develop') == 'develop'
    logger.info('Application will start...')
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=debug)
