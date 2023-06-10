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


def build_table(quotes):
    table = PrettyTable(["Author", "Quote", "Tags"])
    table._max_width = {"Quote": 40}
    table.align["Quote"] = "l"

    for quote in quotes:
        table.add_row([quote.author.fullname, quote.quote, ", ".join(quote.tags)])
    return table


if __name__ == "__main__":
    get_database()

    while True:
        command = input(">>> ")

        match command:
            case "":
                continue

            case "name list":
                author_names = get_author_names()
                print("Список імен авторів:")
                for i, name in enumerate(author_names):
                    print(f"{i+1}. {name}")

            case "tags":
                tags = get_all_tags()
                print("Список всіх тегів:")
                for i, tag in enumerate(tags):
                    print(f"{i+1}. {tag}")

            case cmd if cmd.startswith("name:"):
                author_name = command.split("name:")[1].strip()
                quotes = search_quotes_by_author(author_name)
                if quotes:
                    table = build_table(quotes)
                    print(table)
                else:
                    print("Цитати для заданого імені автора не знайдено.")

            case cmd if cmd.startswith("tag:"):
                tag = command.split("tag:")[1].strip()
                quotes = search_quotes_by_tag(tag)
                if quotes:
                    table = build_table(quotes)
                    print(table)
                else:
                    print("Цитати для заданого тегу не знайдено.")

            case cmd if cmd.startswith("tags:"):
                tags = command.split("tags:")[1].strip().split(",")
                quotes = search_quotes_by_tags(tags)
                if quotes:
                    table = build_table(quotes)
                    print(table)
                else:
                    print("Цитати для заданих тегів не знайдено.")

            case "exit":
                break

            case _:
                print("Невідома команда. Спробуйте ще раз.")