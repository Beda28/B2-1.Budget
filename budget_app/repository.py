import json

from dataclasses import asdict
from pathlib     import Path


class JsonlRepository:
    def __init__(self, file_path:str | Path):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, data) -> None:
        with self.file_path.open("a", encoding='utf-8') as file:
            file.write(json.dumps(asdict(data), ensure_ascii=False) + '\n')

    def stream(self):
        if not self.file_path.exists(): return

        with self.file_path.open("r", encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    yield json.loads(line)

    def update(self, id: int, changed_data: dict) -> bool:
        data_list = list(self.stream())
        updated   = False

        for data in data_list:
            if data['id'] == id:
                data.update(changed_data)
                updated = True
                break

        if not updated: return False

        with self.file_path.open("w", encoding='utf-8') as file:
            for data in data_list:
                file.write(json.dumps(data, ensure_ascii=False) + "\n")

    def next_id(self):
        transaction = list(self.stream())

        if not transaction: return 1
        return max(transactions["id"] for transactions in transaction) + 1