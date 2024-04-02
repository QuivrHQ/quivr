
from modules.analytics.repository.analytics import Analytics
from modules.analytics.repository.analytics_interface import AnalyticsInterface

class AnalyticsService:
    repository: AnalyticsInterface

    def __init__(self):
        self.repository = Analytics()

    def get_brains_usages(self, user_id):
        return self.repository.get_brains_usages(user_id)