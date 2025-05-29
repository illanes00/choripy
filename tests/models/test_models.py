from src.db.models import Crime

def test_crime_model():
    c = Crime(id=1, city="X", year=2020, incidents=5)
    assert c.city == "X"
