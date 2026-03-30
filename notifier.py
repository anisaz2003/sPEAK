from plyer import notification

APP_NAME = "WisprFlow"


def notify(title: str, message: str, timeout: int = 3):
    try:
        notification.notify(
            title=title,
            message=message,
            app_name=APP_NAME,
            timeout=timeout,
        )
    except Exception as e:
        # Never crash the main flow if notifications fail
        print(f"[notifier] {e}")
