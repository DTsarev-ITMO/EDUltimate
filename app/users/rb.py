class RBUser:
    def __init__(self, id: int | None = None,
                 name: str | None = None,
                 email: str | None = None,
                 password: str | None = None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    def to_dict(self) -> dict:
        data = {'id': self.id, 'name': self.name, 'email': self.email,
                'password': self.password}
        # Создаем копию словаря, чтобы избежать изменения словаря во время итерации
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data