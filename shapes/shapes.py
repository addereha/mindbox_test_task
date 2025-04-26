from abc import ABC, abstractmethod
from enum import Enum
import math

class ShapeType(Enum):
    """
    Enum для названий фигур
    """
    CIRCLE = "circle"
    TRIANGLE = "triangle"

class Shape(ABC):
    """
    Абстрактный базовый класс для всех фигур с регистрацией подклассов по ShapeType.
    """
    registry: dict[ShapeType, type['Shape']] = {}

    def __init_subclass__(cls, /, shape_type: ShapeType = None, **kwargs):
        super().__init_subclass__(**kwargs)
        if shape_type:
            Shape.registry[shape_type] = cls

    @abstractmethod
    def area(self) -> float:
        """
        Найти площадь фигуры.
        """
        pass

    @classmethod
    def create(cls, shape_type: ShapeType | str, *args, **kwargs) -> 'Shape':
        """
        Фабричный метод: создать экземпляр фигуры по типу из ShapeType или строке.
        """
        # Поддержка передачи строкового значения
        if isinstance(shape_type, str):
            try:
                shape_type = ShapeType(shape_type)
            except ValueError:
                raise ValueError(f"Неизвестный тип фигуры: {shape_type}")
        if shape_type not in cls.registry:
            raise ValueError(f"Тип фигуры не зарегистрирован: {shape_type}")
        return cls.registry[shape_type](*args, **kwargs)


def compute_area(shape: Shape) -> float:
    """
    Вычислить площадь любого объекта, наследующего Shape.
    """
    return shape.area()

class Circle(Shape, shape_type=ShapeType.CIRCLE):
    """
    Круг, задаётся радиусом.
    """
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        """
        Площадь круга: π·r²
        """
        return math.pi * self.radius ** 2

class Triangle(Shape, shape_type=ShapeType.TRIANGLE):
    """
    Треугольник по трём сторонам с формулой Герона
    и проверкой на прямой угол.
    """
    def __init__(self, a: float, b: float, c: float):
        # Проверяет треугольник
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("Неправильные длины сторон треугольника")
        self.a = a
        self.b = b
        self.c = c

    def area(self) -> float:
        """
        Считает площадь по формуле Герона.
        """
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def is_right(self) -> bool:
        """
        Проверяет, является ли треугольник прямоугольным.
        """
        sides = sorted([self.a, self.b, self.c])
        return math.isclose(sides[0]**2 + sides[1]**2, sides[2]**2, rel_tol=1e-9)
    