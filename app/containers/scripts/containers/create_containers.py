from pprint import pprint

from containers.book_readers.unloading_reader import UploadBookReader
from containers.models import Container
from containers.services.sync import sync_from_text


def test_reader() -> None:
    with open("_data/BD_1.txt", "r", encoding="utf-8") as file:
        text = file.read()
        reader = UploadBookReader()
        containers = reader.read(text=text)
        print(len(containers))

def test_load_containers() -> None:
    with open("_data/BD_3.txt", "r", encoding="utf-8") as file:
        text = file.read()
    result = sync_from_text(text=text)
    pprint(result)

def load_3_db() -> None:
    Container.objects.all().delete()
    files = ["_data/BD_1.txt", "_data/BD_2.txt", "_data/BD_3.txt"]
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()
        result = sync_from_text(text=text)
        pprint(result)

def run() -> None:
    load_3_db()

