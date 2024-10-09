"""
Small experiment debugging json serializer for KMS.
Compare three serialization libs: pydantic, msgspec, orjson
"""

import statistics
import timeit
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

import msgspec
import orjson
from pydantic import BaseModel
from quivr_api.modules.knowledge.dto.outputs import KnowledgeDTO
from quivr_core.models import KnowledgeStatus
from rich.console import Console
from rich.table import Table

n_dto = 1000
num_runs = 100


class ListKM(BaseModel):
    kms: List[KnowledgeDTO]


def serialize_orjson(kms: list[KnowledgeDTO]):
    return orjson.dumps([k.model_dump() for k in kms])


def serialize_orjson_single(kms: ListKM):
    return orjson.dumps(kms.model_dump())


def serialize_pydantic(kms: list[KnowledgeDTO]):
    return [km.model_dump_json() for km in kms]


def serialize_pydantic_obj(kms: ListKM):
    return kms.model_dump_json()


def evaluate(name, func):
    times = timeit.repeat(
        lambda: func(), globals=globals(), repeat=num_runs, number=1
    )  # Change repeat=5 for desired runs
    average_time = sum(times) / len(times)
    std_dev = statistics.stdev(times)
    return name, average_time * 1000, std_dev * 1000


class KnowledgeMsg(msgspec.Struct):
    updated_at: datetime
    created_at: datetime
    user_id: UUID
    brains: List[Dict[str, Any]]
    id: Optional[UUID] = None
    status: Optional[KnowledgeStatus] = None
    file_size: int = 0
    file_name: Optional[str] = None
    url: Optional[str] = None
    extension: str = ".txt"
    is_folder: bool = False
    source: Optional[str] = None
    source_link: Optional[str] = None
    file_sha1: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
    parent: Optional["KnowledgeDTO"] = None
    children: List["KnowledgeDTO"] = []
    sync_id: Optional[int] = None
    sync_file_id: Optional[str] = None


def print_table(results):
    console = Console()
    table = Table(title=f"Serialization Performance, n_obj={n_dto}", show_lines=True)

    # Define table columns
    table.add_column("Function Name", justify="left", style="cyan")
    table.add_column("Average Time (ms)", justify="right", style="magenta")
    table.add_column("Standard Deviation (ms)", justify="right", style="green")

    # Add rows with evaluation results
    for name, avg_time, std_dev in results:
        table.add_row(name, f"{avg_time:.6f}", f"{std_dev:.6f}")

    # Print the table to the console
    console.print(table)


def main():
    data = {
        "id": "24185498-9025-44ea-ae70-b5a1a342f97c",
        "file_size": 57210,
        "status": "UPLOADED",
        "file_name": "0000993.pdf",
        "url": None,
        "extension": ".pdf",
        "is_folder": False,
        "updated_at": "2024-09-26T19:01:23.881842Z",
        "created_at": "2024-09-26T19:00:57.110967Z",
        "source": "local",
        "source_link": None,
        "file_sha1": "1488859a8d85a309b2bff4c669177e688997bfe9",
        "metadata": None,
        "user_id": "155b9ab3-e649-4f8a-b5cf-8150728a9202",
        "brains": [
            {
                "name": "all_kms",
                "description": "kms",
                "temperature": 0,
                "brain_type": "doc",
                "brain_id": "a035b4e5-a385-468a-8f41-2d8344cc6a8f",
                "status": "private",
                "model": None,
                "max_tokens": 2000,
                "last_update": "2024-09-26T19:31:16.352708",
                "prompt_id": None,
            }
        ],
        "sync_id": None,
        "sync_file_id": None,
        "parent": None,
        "children": [],
    }

    km = KnowledgeDTO.model_validate(data)
    # print(isinstance([km]*N,BaseModel))
    list_dto = [km] * n_dto
    single_obj = ListKM(kms=list_dto)
    km_msgspec = msgspec.json.decode(msgspec.json.encode(data), type=KnowledgeMsg)
    list_msgspec = [km_msgspec] * n_dto

    # Evaluation
    results = []
    results.append(evaluate("serialize_pydantic", lambda: serialize_pydantic(list_dto)))
    results.append(
        evaluate(
            "serialize_pydantic_single_obj", lambda: serialize_pydantic_obj(single_obj)
        )
    )
    results.append(evaluate("serialize_orjson", lambda: serialize_orjson(list_dto)))
    results.append(
        evaluate("serialize_orjson_single", lambda: serialize_orjson_single(single_obj))
    )
    results.append(
        evaluate(
            "serialize_msgspec",
            lambda: [msgspec.json.encode(msg) for msg in list_msgspec],
        )
    )

    print_table(results)


if __name__ == "__main__":
    main()
