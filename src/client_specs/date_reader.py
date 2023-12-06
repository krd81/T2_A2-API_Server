from collections.abc import Callable
from models.booking_date import Date
import json
from typing import Any

class DateDecoder(json.JSONDecoder):
    def __init__(self, *, object_hook: Callable[[dict[str, Any]], Any] | None = None, parse_float: Callable[[str], Any] | None = None, parse_int: Callable[[str], Any] | None = None, parse_constant: Callable[[str], Any] | None = None, strict: bool = True, object_pairs_hook: Callable[[list[tuple[str, Any]]], Any] | None = None) -> None:
        super().__init__(object_hook=object_hook, parse_float=parse_float, parse_int=parse_int, parse_constant=parse_constant, strict=strict, object_pairs_hook=object_pairs_hook)

    

    
    json_data = [
            
        {"id": "2024_1",
        "mon": "2024-01-01",
        "tue": "2024-01-02",
        "wed": "2024-01-03",
        "thu": "2024-01-04",
        "fri": "2024-01-05"
        },
        {
        "id": "2024_2",
        "mon": "2024-01-08",
        "tue": "2024-01-09",
        "wed": "2024-01-10",
        "thu": "2024-01-11",
        "fri": "2024-01-12"
        },
        {
        "id": "2024_3",
        "mon": "2024-01-15",
        "tue": "2024-01-16",
        "wed": "2024-01-17",
        "thu": "2024-01-18",
        "fri": "2024-01-19"
        }]


    def object_hook(self, json_data):
    
        if Date in json_data:
            date = Date(json_data["Date"]["id"], json_data["Date"]["mon"], json_data["Date"]["tue"], json_data["Date"]["wed"], json_data["Date"]["thu"], json_data["Date"]["fri"])
        return date