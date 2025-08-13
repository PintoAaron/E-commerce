def format_phone_number(phone_number: str) -> str:
    if phone_number.startswith("0"):
        return "+233" + phone_number[1:]
    return phone_number
