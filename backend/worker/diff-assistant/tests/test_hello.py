from use_case_3 import hello


def test_hello(hello_message):
    assert hello() == hello_message
