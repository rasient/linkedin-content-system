import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "database.csv")

FIELDNAMES = [
    "post_id",
    "title",
    "post_text",
    "image_file",
    "linkedin_url",
    "topic",
    "status",
    "date",
    "analytics_file",
    "notes",
    "generated_post",
    "views",
    "likes",
    "comments"
]


def validate_database():
    if not os.path.exists(DB_PATH):
        return False, "database.csv not found"

    with open(DB_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        if reader.fieldnames is None:
            return False, "database.csv has no header"

        if "" in reader.fieldnames:
            return False, "database.csv has empty column name"

        missing = [field for field in FIELDNAMES if field not in reader.fieldnames]
        if missing:
            return False, f"Missing columns: {missing}"

    return True, "database valid"


def load_posts():
    posts = []

    valid, message = validate_database()
    if not valid:
        print("CSV ERROR:", message)
        return posts

    with open(DB_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            clean = {}
            for field in FIELDNAMES:
                clean[field] = row.get(field, "")
            posts.append(clean)

    return posts