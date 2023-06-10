import json
from database.models import Authors, Quotes
from database.connect import get_database
from mongoengine import MultipleObjectsReturned


def load_data_from_json(json_file):
    with open(json_file, "r") as fh:
        data = json.load(fh)
    return data


def save_authors_to_database(authors):
    get_database()

    # Deleting the Authors collection before adding
    Authors.objects().delete()

    for author in authors:
        Authors(
            fullname=author["fullname"],
            born_date=author["born_date"],
            born_location=author["born_location"],
            description=author["description"],
        ).save()


def save_quotes_to_database(quotes):
    get_database()

    # Deleting the Quotes collection before adding
    Quotes.objects().delete()

    for quote in quotes:
        try:
            author = Authors.objects.get(fullname=quote["author"])
        except MultipleObjectsReturned:
            continue

        Quotes(tags=quote["tags"], author=author, quote=quote["quote"]).save()


if __name__ == "__main__":
    authors_json_file = "authors.json"
    quotes_json_file = "quotes.json"

    authors_data = load_data_from_json(authors_json_file)
    quotes_data = load_data_from_json(quotes_json_file)

    save_authors_to_database(authors_data)
    save_quotes_to_database(quotes_data)
