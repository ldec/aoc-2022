import unittest
from main import Position


class TestStringMethods(unittest.TestCase):
    def test_position_success(self):
        origin = Position(2, 1)
        to_test = [
            Position(1, 0),
            Position(1, 1),
            Position(1, 2),
            Position(2, 0),
            Position(2, 1),
            Position(2, 2),
            Position(3, 0),
            Position(3, 1),
            Position(3, 2),
        ]

        for position in to_test:
            with self.subTest(origin=origin, position=position):  # added statement
                self.assertTrue(origin.is_touching(position))

    def test_position_error(self):
        origin = Position(2, 1)
        to_test = [
            Position(0, 0),
            Position(-1, 0),
            Position(-1, -1),
            Position(3, -1),
        ]

        for position in to_test:
            with self.subTest(origin=origin, position=position):  # added statement
                self.assertFalse(origin.is_touching(position))


if __name__ == "__main__":
    unittest.main()
