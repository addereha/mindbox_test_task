import pytest
import math
from shapes import Circle, Triangle, Shape, compute_area, ShapeType



def test_circle_area():
    # Площадь круга с радиусом 2 должна быть 4π
    c = Circle(2)
    assert math.isclose(c.area(), math.pi * 4)


def test_triangle_area():
    # Прямоугольный треугольник 3-4-5 имеет площадь 6
    t = Triangle(3, 4, 5)
    assert math.isclose(t.area(), 6)


def test_triangle_invalid():
    # Нельзя создать треугольник с такими сторонами
    with pytest.raises(ValueError):
        Triangle(1, 2, 3)


def test_triangle_right():
    # Проверка прямоугольности
    t = Triangle(5, 12, 13)
    assert t.is_right()
    t2 = Triangle(2, 3, 4)
    assert not t2.is_right()


def test_factory_enum():
    # Создание через ShapeType
    c = Shape.create(ShapeType.CIRCLE, 3)
    assert isinstance(c, Circle)
    assert math.isclose(compute_area(c), math.pi * 9)


def test_factory_str():
    # Создание по строке для обратной совместимости
    t = Shape.create("triangle", 3, 4, 5)
    assert isinstance(t, Triangle)
    assert math.isclose(compute_area(t), 6)


def test_unknown_shape():
    # При попытке создать неизвестную фигуру должна быть ошибка
    with pytest.raises(ValueError):
        Shape.create("hexagon", 1)
