from backend.models.databases.database import Database
from models.settings import CommonsDep, common_dependencies


class SupabaseDB(Database):
    @property
    def commons(self) -> CommonsDep:
        return common_dependencies()

    def select(self, table, columns, conditions):
        # Implement select operation using Supabase API
        pass

    def insert(self, table, data):
        # Implement insert operation using Supabase API
        self.db.table(table).insert(data).execute()

    def update(self, table, data, conditions):
        # Implement update operation using Supabase API
        pass

    def delete(self, table, conditions):
        # Implement delete operation using Supabase API
        pass
