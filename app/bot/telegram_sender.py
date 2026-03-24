from urllib import parse, request


class TelegramSendError(RuntimeError):
    pass


def send_text(token: str, chat_id: str, text: str) -> None:
    data = parse.urlencode({"chat_id": chat_id, "text": text}).encode("utf-8")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    req = request.Request(url, data=data, method="POST")

    try:
        with request.urlopen(req, timeout=10) as response:
            if response.status != 200:
                raise TelegramSendError(f"Telegram API returned {response.status}")
    except Exception as exc:  # noqa: BLE001
        raise TelegramSendError(str(exc)) from exc
