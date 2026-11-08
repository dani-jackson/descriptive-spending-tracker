import json
from model.user_profile import UserProfile

class FileStorage:
    def save(self, profile, filename):
        with open(filename, "w") as f:
            json.dump(profile.to_dict(), f, indent=4)

    def load(self, filename):
        with open(filename, "r") as f:
            data = json.load(f)

        return UserProfile.from_dict(data)
