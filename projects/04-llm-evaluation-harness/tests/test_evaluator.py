from app.evaluator import CaseScore, summarize


def test_summary_averages_quality_dimensions():
    scores = [CaseScore("a", 5, 4, 3, "good"), CaseScore("b", 3, 4, 5, "good")]
    result = summarize(scores)
    assert result == {"cases": 2, "relevance": 4.0, "groundedness": 4.0, "context_coverage": 4.0, "overall": 4.0}


def test_empty_summary_is_safe():
    assert summarize([])["overall"] == 0.0
