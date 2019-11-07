def func(x):
    return x + 1


def test_answer(test_client):
    assert func(3) == 5
