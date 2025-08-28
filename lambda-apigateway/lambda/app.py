def handler(event, context):
    text = event["text"]

    is_anagram = text == text[::-1]
    message = f"{text} is an anagram" if is_anagram else f"{text} is not an anagram"

    return {
        "status": "success",
        "message": message,
    }
