import re

def remove_unnecessary_white_space(text: str) -> str:
    return " ".join(text.split())

def remove_not_korean(text: str) -> str:
    korean = re.compile(r"[^ ㄱ-ㅣ가-힣+]")
    return korean.sub(" ", text)

def remove_reporter_name(text: str) -> str:
    return re.sub(r"[ㄱ-ㅣ가-힣]+ 기자", "", text)