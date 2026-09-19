from app.workflow import clean_html, valid_public_url


def test_clean_html_removes_scripts():
    assert clean_html("<h1>Title</h1><script>ignore()</script><p>Body</p>") == "Title Body"


def test_public_url_validation():
    assert valid_public_url("https://example.com/article")
    assert not valid_public_url("http://localhost:8000/secret")

