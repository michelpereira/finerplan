from finerplan import db

from config import fundamental_accounts


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    path = db.Column(db.String(500), index=True)
    group = db.Column(db.String(64))
    # TODO: Transform properties into hybrid properties so SQLAlchemy can query them

    def __repr__(self):
        return f'<Account {self.id} {self.name}>'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def create(cls, name, user, parent=None) -> 'Account':
        """
        Public method to create an account linked to an user.

        Parameters
        ----------
        name: str
            Name of the new account.
        user: models.User
            User object to which the new account will be linked to.
        parent: models.Account
            If passed, the new account will become a subaccount of
            parent Account and will have the same type.
        """
        if cls.check_unique_fullname(name=name, user=user, parent=parent):
            new_account = cls(name=name, user_id=user.id)
            db.session.add(new_account)
            db.session.commit()

        else:
            raise NameError("Each account's fullname must be unique.")

        new_account._generate_path(parent=parent)
        db.session.commit()

        new_account._define_group(parent=parent)
        db.session.commit()

        return new_account

    @classmethod
    def check_unique_fullname(cls, name, user, parent):
        if parent is not None:
            base_fullname = parent.fullname + ' - '
        else:
            base_fullname = ''

        account = cls.query.filter(
            cls.name == name,
            cls.user_id == user.id).all()

        if not account:
            return True

        for _account in account:
            if _account.fullname == base_fullname + name:
                return False

        return True

    def _generate_path(self, parent=None) -> None:
        if parent is not None:
            path = parent.path + '.'
        else:
            path = ''
        self.path = path + str(self.id)

    def _define_group(self, parent=None) -> None:
        if parent is not None:
            group = parent.group
        else:
            group = self.name.lower()
        self.group = group

    @property
    def fullname(self):
        """
        Returns the name of all the account's parents accounts in a single string.
        """
        path_nodes = self.path.split('.')
        path_names = [Account.query.get(int(node)).name for node in path_nodes]

        return ' - '.join(path_names)

    @property
    def depth(self):
        """
        Returns how deep a certain account is in the hierarchy
        """
        return len(self.path.split('.'))

    def descendents(self):
        """
        Returns the descendents from self.
        """
        children_path = self.path + '.%'
        children = self.query.filter(Account.path.like(children_path))

        return children.all()

    @property
    def is_leaf(self):
        """
        Returns a boolean indicating whether the queried account
        is a leaf (ie, has no descendents).
        """
        return len(self.descendents()) == 0


def init_fundamental_accounts(user):
    # Initialize user accounts here
    for account_name in fundamental_accounts:
        try:
            Account.create(name=account_name, user=user)
        except NameError:
            pass  # Account is already created
