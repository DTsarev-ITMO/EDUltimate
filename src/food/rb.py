class RBFood:
    def __init__(self, food_id: int | None = None,
                 name: str | None = None,
                 protein: float | None = None,
                 fats: float | None = None,
                 carbs: float | None = None,
                 calories: float | None = None):
        self.id = food_id
        self.name = name
        self.protein = protein
        self.fats = fats
        self.carbs = carbs
        self.calories = calories

    def to_dict(self) -> dict:
        data = {'id': self.id, 'name': self.name, 'protein': self.protein,
                'fats': self.fats, 'carbs': self.carbs, 'calories': self.calories}
        # Создаем копию словаря, чтобы избежать изменения словаря во время итерации
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data