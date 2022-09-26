import requests


class Bot:
    def __init__(self, token):
        self.token = token

        self.url = f"https://api.telegram.org/bot{self.token}"

    def get_me(self):
        return requests.get(f"{self.url}/getMe")

    def get_updates(self):
        return requests.get(f"{self.url}/getUpdates")

    def send_message(self, chat_id, text, parse_mode):
        params = dict(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
            disable_web_page_preview=True,
        )

        return requests.get(f"{self.url}/sendMessage", data=params)
