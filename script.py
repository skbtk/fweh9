from database import get_channels

async def upload_links(app, links):
    channels = get_channels()
    if not channels:
        return
    text = "\n".join(links)
    for cid in channels:
        try:
            await app.send_message(cid, text)
        except Exception as e:
            print(f"Failed to send to {cid}: {e}")
