from rich import print

# A random, decently sized dictionary with different types of values
data = {
    "name": "John Doe",
    "age": 30,
    "is_student": False,
    "marks": [80, 90, 85],
    "address": {
        "city": "New York",
        "state": "NY",
        "country": "USA",
    },
    "friends": [
        {"name": "Jane Doe", "age": 29},
        {"name": "Jim Doe", "age": 31},
    ],
    "is_employed": True,
    "salary": 100000,
    "languages": ("English", "Spanish"),
    "skills": {"Python", "JavaScript", "SQL"},
    "is_married": True,
    "spouse": {
        "name": "Jill Doe",
        "age": 28,
    },
    "children": [
        {"name": "Jack Doe", "age": 5},
        {"name": "Jill Doe Jr.", "age": 3},
    ],
    "is_retired": False,
    "retirement_age": 65,
    "retirement_savings": 1000000,
    "is_vaccinated": True,
    "vaccines": ["Moderna", "Pfizer"],
    "is_senior_citizen": False,
    "is_disabled": False,
}

print(data)
