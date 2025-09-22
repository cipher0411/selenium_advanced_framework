def test_google_title(setup):
    driver = setup
    driver.get("https://www.google.com")
    assert "Google" in driver.title
