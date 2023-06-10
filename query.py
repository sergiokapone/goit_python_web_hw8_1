from prettytable import PrettyTable
from database.models import Authors, Quotes
from database.connect import get_database
import redis
from redis_lru import RedisLRU
from functools import wraps
import time


client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


def time_it(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Function {func.__name__} started")
        start = time.time()
        results = func(*args, **kwargs)
        finish = time.time()
        print(f"Function {func.__name__} executed in {finish - start:.4f} seconds.")
        return results

    return wrapper


@time_it
@cache
def search_quotes_by_author(author_name):
    get_database()

    try:
        author = Authors.objects.get(fullname__istartswith=author_name)
        quotes = Quotes.objects(author=author)
        return quotes
    except Authors.DoesNotExist:
        return []


@time_it
@cache
def search_quotes_by_tag(tag):
    get_database()

    quotes = Quotes.objects(tags__istartswith=tag)
    return quotes


def search_quotes_by_tags(tags):
    get_database()

    quotes = Quotes.objects(tags__istartswith=tags)
    return quotes


def get_author_names():
    get_database()

    authors = Authors.objects()
    author_names = [author.fullname for author in authors]
    return author_names


def get_all_tags():
    get_database()

    tags = Quotes.objects.distinct("tags")
    return tags


if __name__ == "__main__":
    get_database()

    while True:
        command = input(">>> ")

        if command == "name list":
            author_names = get_author_names()
            print("Список імен авторів:")
            for i, name in enumerate(author_names):
                print(f"{i+1}. {name}")

        elif command == "tags":
            tags = get_all_tags()
            print("Список всіх тегів:")
            for i, tag in enumerate(tags):
                print(f"{i+1}. {tag}")

        elif command.startswith("name:"):
            author_name = command.split("name:")[1].strip()
            quotes = search_quotes_by_author(author_name)
            table = PrettyTable(["Author", "Quote", "Tags"])
            if quotes:
                for quote in quotes:
                    table.add_row(
                        [quote.author.fullname, quote.quote, ", ".join(quote.tags)]
                    )
                print(table)
            else:
                print("Цитати для заданого імені автора не знайдено.")

        elif command.startswith("tag:"):
            tag = command.split("tag:")[1].strip()
            quotes = search_quotes_by_tag(tag)
            table = PrettyTable(["Author", "Quote", "Tags"])
            if quotes:
                for quote in quotes:
                    table.add_row(
                        [quote.author.fullname, quote.quote, ", ".join(quote.tags)]
                    )
                print(table)
            else:
                print("Цитати для заданого тегу не знайдено.")

        elif command.startswith("tags:"):
            tags = command.split("tags:")[1].strip().split(",")
            quotes = search_quotes_by_tags(tags)
            table = PrettyTable(["Author", "Quote", "Tags"])
            if quotes:
                for quote in quotes:
                    table.add_row(
                        [quote.author.fullname, quote.quote, ", ".join(quote.tags)]
                    )
                print(table)
            else:
                print("Цитати для заданих тегів не знайдено.")

        elif command == "exit":
            break

        else:
            print("Невідома команда. Спробуйте ще раз.")
