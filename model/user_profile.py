# model/user_profile.py

class UserProfile:
    def __init__(self, accounts=None):
        self.accounts = accounts if accounts else []

    def add_account(self, account):
        self.accounts.append(account)

    def to_dict(self):
        return {
            "accounts": [acct.to_dict() for acct in self.accounts]
        }

    @staticmethod
    def from_dict(data):
        """
        Load a UserProfile from saved JSON.
        Uses Account.from_dict() so budgets, APY, APR, and IDs are preserved.
        """
        from model.account import Account

        accounts = []

        # Backward compatibility: old single-account format
        if "acct_type" in data:
            acct = Account.from_dict(data)
            return UserProfile([acct])

        # New multi-account format
        for a in data.get("accounts", []):
            acct = Account.from_dict(a)
            accounts.append(acct)

        return UserProfile(accounts)
