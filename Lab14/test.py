from main import *
import pytest

def test_hello():
    got = hello("Aleksandra")
    want = "Hello Aleksandra"
    assert got == want



testdata = ["I think today will be a great day","I do not think this will turn out well"]

@pytest.mark.parametrize('sample', testdata)
def test_extract_sentiment(sample):
    sentiment = extract_sentiment(sample)
    assert sentiment >= 0

testdata = [
    ('There is a duck in this text', 'duck', True),
    ('There is nothing here', 'duck', False)
]

@pytest.mark.parametrize('sample, word, expected_output', testdata)
def test_text_contain_word(sample, word, expected_output):
    assert text_contain_word(word, sample) == expected_output

prepared_data = [
    ([1,2,3,4,5,6], True, [1,2,3,4,5,6]),
    ([2,3,6,4,1,5], True, [1,2,3,4,5,6]),
    ([1,2,3,4,5,6], False, [6,5,4,3,2,1]),
    ([2,3,6,4,1,5], False, [6,5,4,3,2,1]),
]
@pytest.mark.parametrize('sample_list, ascending, expected_output', prepared_data)
def test_bubblesort(sample_list, ascending, expected_output):
    assert bubblesort(sample_list, ascending) == expected_output

