from core.manager import Manager


class OnBoard(Manager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "OnBoard App"
        self.version = "0.0.1"
        self.description = "Onboarding new users"
    
    async def get_leave(self, user_id):
        return self.SLACK_CLIENT.users_profile_get(user=user_id)