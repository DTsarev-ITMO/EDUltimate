class RBUser:
    def __init__(self, user_id: int | None = None,
                 username: str | None = None,
                 email: str | None = None,
                 weight: float | None = None,
                 LBS: float | None = None,
                 fat_percentage: float | None = None):
        self.id = user_id
        self.name = username
        self.email = email
        self.weight = weight
        self.LBS = LBS
        self.fat_percentage = fat_percentage

    def to_dict(self) -> dict:
        data = {'id': self.id, 'Имя': self.name, 'e-mail': self.email,
                'Масса': self.weight, 'Сухая масса': self.LBS, 'Процет жира': self.fat_percentage}
        # Создаем копию словаря, чтобы избежать изменения словаря во время итерации
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data