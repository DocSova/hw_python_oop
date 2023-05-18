"""Домашняя работа Яндекс Практикума."""


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        """Инициализация."""
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def show_training_info(self) -> None:
        """Возвращает форматированную строку."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.2f} ч.; '
                f'Дистанция: {self.distance:.2f} км; '
                f'Ср. скорость: {self.speed:.2f} км/ч; '
                f'Потрачено ккал: {self.calories:.2f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        """Инициализация."""
        self.action = action
        self.duration = duration
        self.weight = weight

    def __str__(self):
        """Описание."""
        return 'Тренировка'

    def get_distance(self, action: int) -> float:
        """Получить дистанцию в км."""
        return action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self, distance: float, time: float) -> float:
        """Получить среднюю скорость движения."""
        return distance / time

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        distance = self.get_distance(self.action)
        mean_speed = self.get_mean_speed(distance, self.duration)
        calories = self.get_spent_calories()
        return InfoMessage(self,
                           self.duration,
                           distance,
                           mean_speed,
                           calories).show_training_info()


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self, action: int, duration: float, weight: float):
        """Инициализация."""
        super().__init__(action, duration, weight)

    def __str__(self):
        """Описание."""
        return 'Бег'

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        distance = self.get_distance(self.action)
        mean_speed = self.get_mean_speed(distance, self.duration)
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * mean_speed
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.duration)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_MEAN_WEIGHT_MULTIPLIER = 0.035
    CALORIES_MEAN_WEIGHT_SHIFT = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int):
        """Инициализация."""
        super().__init__(action, duration, weight)
        self.height = height

    def __str__(self):
        """Описание."""
        return 'Спортивная ходьба'

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        distance = self.get_distance(self.action)
        mean_speed = self.get_mean_speed(distance, self.duration)
        return ((self.CALORIES_MEAN_WEIGHT_MULTIPLIER * self.weight
                + (mean_speed**2 / self.height)
                * self.CALORIES_MEAN_WEIGHT_SHIFT * self.weight)
                * self.duration)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER = 1.1
    CALORIES_MEAN__SHIFT = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 lenght_pool: int,
                 count_pool: int):
        """Инициализация."""
        super().__init__(action, duration, weight)
        self.lenght_pool = lenght_pool
        self.count_pool = count_pool

    def __str__(self):
        """Описание."""
        return 'Плавание'

    def get_mean_speed(self, *args) -> float:
        """Получить среднюю скорость движения."""
        return (self.lenght_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        distance = self.get_distance(self.action)
        mean_speed = self.get_mean_speed(distance, self.duration)
        return ((mean_speed + self.CALORIES_MEAN_SPEED_MULTIPLIER)
                * self.CALORIES_MEAN__SHIFT * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    types_of_packages = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return types_of_packages[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
