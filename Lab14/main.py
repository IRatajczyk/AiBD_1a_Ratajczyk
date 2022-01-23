import textblob
from typing import List


def hello(name: str) -> str:
    return "Hello " + name


def extract_sentiment(text: str):
    text = textblob.TextBlob(text)
    return text.sentiment.polarity


def text_contain_word(pattern: str, text: str) -> bool:
    return pattern in text.split()


def bubblesort(input_list: List[int], ascending=True):
    working_list = input_list[:]
    lgh = len(working_list)
    change = True
    while lgh and change:
        change = False
        for i in range(lgh - 1):
            if working_list[i] > working_list[i + 1]:
                change = True
                working_list[i], working_list[i + 1] = working_list[i + 1], working_list[i]
        lgh -= 1
    return working_list if ascending else working_list[::-1]
