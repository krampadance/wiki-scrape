import re


def remove_special_characters(text: str) -> str:
    return re.sub(r"[^\x00-\x7F]+", " ", text)


def remove_number_brackets(text: str) -> str:
    # Regular expression pattern to match [number] where number can be any digit
    pattern = r"\[\d+\]"
    # Replace matched patterns with an empty string
    return re.sub(pattern, "", text)


def clean_text(text: str) -> str:
    text = remove_special_characters(text)
    return remove_number_brackets(text)
