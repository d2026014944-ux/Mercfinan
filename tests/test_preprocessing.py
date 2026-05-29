import unittest

from market_predictor.ml.preprocessing import normalize_window


class PreprocessingTest(unittest.TestCase):
    def test_normalize_window_is_pure_and_does_not_mutate_input(self) -> None:
        original = [2.0, 4.0, 6.0, 8.0]

        normalized = normalize_window(original)

        self.assertEqual(original, [2.0, 4.0, 6.0, 8.0])
        self.assertEqual(normalized, [0.0, 0.3333333333333333, 0.6666666666666666, 1.0])

    def test_normalize_window_values_stay_within_minus_one_to_one(self) -> None:
        original = [-3.5, -1.0, 0.0, 2.5, 10.0]

        normalized = normalize_window(original)

        self.assertTrue(all(-1.0 <= value <= 1.0 for value in normalized))


if __name__ == "__main__":
    unittest.main()
