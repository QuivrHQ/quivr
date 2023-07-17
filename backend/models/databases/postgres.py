from models.databases.database import Database
import models.sqlalchemy_repository as repo
from sqlalchemy.orm import class_mapper


from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

TABLE_CLASS_MAPPING = {
    "users": repo.User,
    "brains": repo.Brain,
    "brains_users": repo.BrainUser,
    "brains_vectors": repo.BrainVector,
    "brain_subscription_invitations": repo.BrainSubscriptionInvitation,
    "api_keys": repo.ApiKey,
}


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in class_mapper(obj.__class__).columns}


class Response:
    def __init__(self, data):
        self.data = data


class PostgresDB(Database):
    def __init__(self, session):
        self.session = session

    def select(self, table, columns, conditions):
        # Implement select operation using psycopg2 or SQLAlchemy
        pass

    def insert(self, table, data):
        table_class: Base = TABLE_CLASS_MAPPING[table]
        new_entry = table_class(**data)
        self.session.add(new_entry)
        self.session.commit()
        self.session.refresh(new_entry)
        return Response([object_as_dict(new_entry)])

    def update(self, table, data, conditions):
        # Implement update operation using psycopg2 or SQLAlchemy
        pass

    def delete(self, table, conditions):
        # Implement delete operation using psycopg2 or SQLAlchemy
        pass
