import os
from typing import List
from uuid import UUID

import numpy as np
from pydantic import BaseModel
from quivr_api.logger import get_logger
from quivr_api.models.settings import settings
from quivr_api.modules.brain.entity.brain_entity import Brain, BrainType
from quivr_api.modules.brain.entity.brain_user import BrainUserDB
from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB
from quivr_api.modules.user.entity.user_identity import User
from quivr_api.modules.vector.entity.vector import Vector
from sqlmodel import Session, create_engine, select

N_BRAINS = 100
N_USERS = 1
KNOWLEDGE_PER_BRAIN_MAX = 50
KNOWLEDGE_PER_BRAIN_MIN = 20
MEAN_VECTORS_PER_KNOWLEDGE = 500
STD_VECTORS_PER_KNOWLEDGE = 200
SAVE_PATH = "benchmarks/data.json"


logger = get_logger("load_testing")
pg_database_base_url = "postgresql://postgres:postgres@localhost:54322/postgres"


class Data(BaseModel):
    brains_ids: List[UUID]
    knowledges_ids: List[UUID]
    vectors_ids: List[UUID]


def setup_brains(session: Session, user_id: UUID):
    brains = []
    brains_users = []

    for idx in range(N_BRAINS):
        brain = Brain(
            name=f"brain_{idx}",
            description="this is a test brain",
            brain_type=BrainType.integration,
            status="private",
        )
        brains.append(brain)

    session.add_all(brains)
    session.commit()
    [session.refresh(b) for b in brains]

    for brain in brains:
        brain_user = BrainUserDB(
            brain_id=brain.brain_id,
            user_id=user_id,
            default_brain=True,
            rights="Owner",
        )
        brains_users.append(brain_user)
    session.add_all(brains_users)
    session.commit()

    return brains


def setup_knowledge_brain(session: Session, brain: Brain, n_km: int, user_id: UUID):
    kms = []

    for idx in range(n_km):
        knowledge = KnowledgeDB(
            file_name=f"test_file_{idx}_brain_{idx}",
            extension="txt",
            status="UPLOADED",
            source="test_source",
            source_link="test_source_link",
            file_size=100,
            file_sha1=f"{os.urandom(128)}",
            brains=[brain],
            user_id=user_id,
        )
        kms.append(knowledge)

    return kms


def setup_vectors_knowledge(session: Session, knowledge: KnowledgeDB, n_vecs: int):
    vecs = []
    assert knowledge.id
    for idx in range(n_vecs):
        vector = Vector(
            content=f"vector_{idx}",
            metadata_={"file_name": f"{knowledge.file_name}", "chunk_size": 96},
            embedding=np.random.randn(settings.embedding_dim),  # type: ignore
            knowledge_id=knowledge.id,
        )

        vecs.append(vector)

    return vecs


def setup_all(session: Session):
    user = (session.exec(select(User).where(User.email == "admin@quivr.app"))).one()
    assert user.id
    brains = setup_brains(session, user.id)
    logger.info(f"Inserted all {len(brains)} brains")
    # all_km = []
    # all_vecs = []
    # for brain in brains:
    #     assert brain
    #     n_knowledges = random.randint(KNOWLEDGE_PER_BRAIN_MIN, KNOWLEDGE_PER_BRAIN_MAX)
    #     knowledges = setup_knowledge_brain(
    #         session, brain=brain, n_km=n_knowledges, user_id=user.id
    #     )
    #     logger.info(f"Inserted all {len(knowledges)} kms for {brain.name}")
    #     all_km.extend(knowledges)

    # session.add_all(all_km)
    # session.commit()
    # [session.refresh(b) for b in all_km]

    # n_vecs = np.random.normal(
    #     MEAN_VECTORS_PER_KNOWLEDGE, STD_VECTORS_PER_KNOWLEDGE, len(all_km)
    # ).tolist()
    # for n_vecs_km, knowledge in zip(n_vecs, all_km, strict=False):
    #     vecs = setup_vectors_knowledge(session, knowledge, int(n_vecs_km))
    #     all_vecs.extend(vecs)

    # logger.info(f"Inserting all {len(all_vecs)} vecs for knowledge {knowledge.id}")
    # session.add_all(all_vecs)
    # session.commit()
    # [session.refresh(b) for b in all_km]
    # [session.refresh(b) for b in all_vecs]

    return Data(
        brains_ids=[b.brain_id for b in brains],
        knowledges_ids=[],  # [k.id for k in all_km],
        vectors_ids=[],  # [v.id for v in all_vecs],
    )


def setup_data():
    logger.info(f"""Starting load data script
    N_BRAINS = {N_BRAINS},
    N_USERS = {N_USERS},
    KNOWLEDGE_PER_BRAIN_MIN = {KNOWLEDGE_PER_BRAIN_MIN},
    KNOWLEDGE_PER_BRAIN_MAX = {KNOWLEDGE_PER_BRAIN_MAX },
    MEAN_VECTORS_PER_KNOWLEDGE = {MEAN_VECTORS_PER_KNOWLEDGE}
    STD_VECTORS_PER_KNOWLEDGE ={STD_VECTORS_PER_KNOWLEDGE}
                 """)
    sync_engine = create_engine(
        pg_database_base_url,
        echo=True if os.getenv("ORM_DEBUG") else False,
        future=True,
        # NOTE: pessimistic bound on
        pool_pre_ping=True,
        pool_size=10,  # NOTE: no bouncer for now, if 6 process workers => 6
        pool_recycle=1800,
    )

    with Session(sync_engine, expire_on_commit=False, autoflush=False) as session:
        data = setup_all(session)

    logger.info(
        f"Insert {len(data.brains_ids)} brains, {len(data.knowledges_ids)} knowledges, {len(data.vectors_ids)} vectors"
    )

    with open(SAVE_PATH, "w") as f:
        f.write(data.model_dump_json())


if __name__ == "__main__":
    setup_data()
