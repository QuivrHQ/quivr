import os
from typing import List, Tuple

import pytest
from quivr_api.modules.brain.entity.brain_entity import Brain, BrainType
from quivr_api.modules.dependencies import get_embedding_client
from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB
from quivr_api.vector.entity.vector import Vector
from quivr_api.vector.repository.vectors_repository import VectorRepository
from sqlalchemy import create_engine
from sqlmodel import Session, select

pg_database_base_url = "postgresql://postgres:postgres@localhost:54322/postgres"

TestData = Tuple[List[Vector], KnowledgeDB, Brain]


@pytest.fixture(scope="session")
def engine():
    return create_engine(
        pg_database_base_url,
        echo=True if os.getenv("ORM_DEBUG") else False,
    )


@pytest.fixture(scope="function")
def session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def test_data(session: Session) -> TestData:
    embedding = get_embedding_client()
    vectors = embedding.embed_documents(
        ["I love paste a la vongole", "I rather play chess than watch football"]
    )

    nested = session.begin_nested()  # Start a savepoint

    brain_1 = Brain(
        name="test_brain",
        description="this is a test brain",
        brain_type=BrainType.integration,
    )
    knowledge_1 = KnowledgeDB(
        file_name="test_file_1",
        mime_type="txt",
        status="UPLOADED",
        source="test_source",
        source_link="test_source_link",
        file_size=100,
        file_sha1="test_sha1",
        brains=[brain_1],
    )
    session.add(knowledge_1)
    session.flush()  # This will assign an ID to knowledge_1
    assert knowledge_1.id, "Knowledge ID not generated"

    vector_1 = Vector(
        content="vector_1",
        metadata_={"chunk_size": 16},
        embedding=vectors[0],  # type: ignore
        knowledge_id=knowledge_1.id,
    )

    vector_2 = Vector(
        content="vector_2",
        metadata_={"chunk_size": 16},
        embedding=vectors[1],  # type: ignore
        knowledge_id=knowledge_1.id,
    )

    session.add(vector_1)
    session.add(vector_2)

    session.flush()

    yield ([vector_1, vector_2], knowledge_1, brain_1)
    # @Amine do not get the typing() error

    nested.rollback()  # Roll back the savepoint after the test


def test_get_vectors_by_knowledge_id(session: Session, test_data: TestData):
    vectors, knowledge, _ = test_data
    assert knowledge.id

    query = select(Vector).where(Vector.knowledge_id == knowledge.id)
    results = session.execute(query).all()

    assert len(results) == 2, f"Expected 2 vectors, got {len(results)}"
    assert (
        results[0][0].content == vectors[0].content
    ), f"Expected {vectors[0].content}, got {results[0][0].content}"
    assert (
        results[1][0].content == vectors[1].content
    ), f"Expected {vectors[1].content}, got {results[1][0].content}"


def test_similarity_search(session: Session, test_data: TestData):
    vectors, knowledge, brain = test_data
    assert knowledge.id
    assert brain.brain_id

    repo = VectorRepository(session)

    k = 2
    results = repo.similarity_search(vectors[0].embedding, brain.brain_id, k=k)  # type: ignore
    assert len(results) == k
    assert results[0].content == vectors[0].content

    results = repo.similarity_search(vectors[1].embedding, brain.brain_id, k=k)  # type: ignore

    assert results[0].content == vectors[1].content
