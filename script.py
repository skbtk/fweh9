# script.py
async def upload_links_to_channel(app, channel_id, links: list[str]):
    for link in links:
        try:
            await app.send_message(chat_id=channel_id, text=link)
        except Exception as e:
            print(f"Error sending link: {e}")
