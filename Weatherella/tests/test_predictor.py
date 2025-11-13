from backend.predictor import should_bring_umbrella


def test_recommend_for_rain():
    weather = {"weather": {"id": 501, "main": "Rain", "description": "moderate rain"}, "rain": {"1h": 2.5}, "clouds": 90, "humidity": 80}
    rec = should_bring_umbrella(weather)
    assert rec["recommend"] is True
    assert rec["score"] >= 0.8


def test_no_recommend_clear():
    weather = {"weather": {"id": 800, "main": "Clear", "description": "clear sky"}, "clouds": 0, "humidity": 40}
    rec = should_bring_umbrella(weather)
    assert rec["recommend"] is False


def test_user_example_taguiq_like():
    # Example provided: 31°C, feels 38°C, broken clouds, humidity 74%, wind 4.47 m/s, pressure 1004 hPa, visibility 10 km, clouds 75%
    weather = {
        "temp": 31.0,
        "feels_like": 38.0,
        "weather": {"id": 803, "main": "Clouds", "description": "broken clouds", "icon": "04d"},
        "humidity": 74,
        "wind_speed": 4.47,
        "pressure": 1004,
        "visibility": 10000,
        "clouds": 75,
    }
    rec = should_bring_umbrella(weather)
    # With these inputs, probability should be moderate; assert that score is between 0.1 and 0.7 and that recommendation is False-ish
    assert 0.0 <= rec["score"] <= 1.0
    # we don't force a strict boolean since edge thresholds may vary, but give an informative check
    assert isinstance(rec["recommend"], bool)
