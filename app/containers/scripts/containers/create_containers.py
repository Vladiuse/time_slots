from containers.book_readers.unloading_reader import UploadBookReader
from containers.models import Container
from containers.services.sync import SyncResult, sync_from_text


def test_reader() -> None:
    with open("_data/BD_1.txt", "r", encoding="utf-8") as file:
        text = file.read()
        reader = UploadBookReader()
        containers = reader.read(text=text)
        print(len(containers))


def print_sync_result(file: str, result: SyncResult) -> None:
    print(f"\n=== {file} ===")
    print(f"  new clients:         {len(result.new_client_ids)}")
    print(f"  new client accounts: {len(result.new_client_account_ids)}")
    print(f"  containers created:  {len(result.containers.created_ids)}")
    print(f"  containers picked up: {len(result.containers.picked_up_numbers)}")
    print(f"  skipped (no client): {len(result.containers.skipped_no_client_numbers)}")


def load_3_db() -> None:
    Container.objects.all().delete()
    files = ["_data/BD_1.txt", "_data/BD_2.txt", "_data/BD_3.txt"]
    for file in files:
        print("Reading file:", file)
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()
        result = sync_from_text(text=text)
        print_sync_result(file, result)


def run() -> None:
    load_3_db()
