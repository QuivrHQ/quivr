import asyncio
import os
import select
from typing import List, Tuple

import pytest
import pytest_asyncio
import sqlalchemy
from pgvector.sqlalchemy import Vector as PGVector
from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB
from quivr_api.vector.entity.vector import Vector
from sqlmodel import Session, select

pg_database_base_url = "postgres:postgres@localhost:54322/postgres"

TestData = Tuple[List[Vector], KnowledgeDB]


@pytest.fixture(scope="session")
def event_loop(request: pytest.FixtureRequest):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
def async_engine():
    engine = sqlalchemy.create_engine(
        "postgresql://" + pg_database_base_url,
        echo=True if os.getenv("ORM_DEBUG") else False,
        future=True,
        # NOTE: pessimistic bound on
        pool_pre_ping=True,
        pool_size=10,  # NOTE: no bouncer for now, if 6 process workers => 6
        pool_recycle=1800,
    )
    yield engine


@pytest.fixture()
def session(engine):
    with engine.connect() as conn:
        conn.begin()
        conn.begin_nested()
        session = Session(conn, expire_on_commit=False)

        @sqlalchemy.event.listens_for(session, "after_transaction_end")
        def end_savepoint(session, transaction):
            if conn.closed:
                return
            if not conn.in_nested_transaction():
                conn.sync_connection.begin_nested()

        yield session


@pytest.fixture()
def test_data(
    session: Session,
) -> TestData:
    knowledge_1 = KnowledgeDB(
        file_name="test_file_1",
        mime_type="txt",
        status="UPLOADED",
        source="test_source",
        source_link="test_source_link",
        file_size=100,
        file_sha1="test_sha1",
        brains=[],
    )
    assert knowledge_1.id, "Knowledge ID not generated"

    vector_1 = Vector(
        content="vector_1",
        metadata_={"metadata": "metadata_1"},
        embedding=PGVector([1, 2, 3]),
        knowledge_id=knowledge_1.id,
    )

    vector_2 = Vector(
        content="vector_2",
        metadata_={"metadata": "metadata_2"},
        embedding=PGVector([4, 5, 6]),
        knowledge_id=knowledge_1.id,
    )

    session.add(knowledge_1)
    session.add(vector_1)
    session.add(vector_2)

    session.commit()
    return [vector_1, vector_2], knowledge_1


def test_get_vectors_by_knowledge_id(session: Session, test_data: TestData):
    vectors, knowledge = test_data
    assert knowledge.id

    query = select(Vector).where(Vector.knowledge_id == knowledge.id)
    results = session.exec(query).all()

    assert len(results) == 2
    assert results[0].content == vectors[0].content
    assert results[1].content == vectors[1].content
