import re
import csv
import json

from pathlib import Path

from global_config import settings


class ParserUtils:
    @staticmethod
    def validate_email(email: str) -> bool: 
        email_regex = re.compile(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        )
        
        return re.match(email_regex, email) is not None
    
    @staticmethod
    def read_csv(file_name: str) -> list[dict]:
        data = []
        file_path = Path(__file__).parent.parent.parent / file_name
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data

    @staticmethod
    def write_result_to_json(result_data: dict):
        file_path = Path(__file__).parent.parent.parent / settings.RESULT_FILE_NAME
        if file_path.exists():
            with open(file_path, mode='r', encoding='utf-8') as file:
                try:
                    existing_data = json.load(file)
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []

        existing_data.append(result_data)

        with open(file_path, mode='w', encoding='utf-8') as file:
            json.dump(existing_data, file, indent=4, ensure_ascii=False)
