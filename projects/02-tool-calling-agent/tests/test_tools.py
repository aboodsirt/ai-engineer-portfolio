from app.tools import calculate, search_knowledge


def test_calculator_supports_arithmetic():
    assert calculate({"expression": "3 * 19.99"}) == "59.97"


def test_calculator_rejects_code():
    assert "Only arithmetic" in calculate({"expression": "__import__('os')"})


def test_knowledge_search_returns_policy():
    assert "fourteen days" in search_knowledge({"topic": "refund policy"})

