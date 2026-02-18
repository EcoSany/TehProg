from datetime import datetime

class Logger:
    @staticmethod
    def log(message, level="ERROR"):
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] [{level}] {message}\n")