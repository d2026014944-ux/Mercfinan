import unittest
from pathlib import Path


class ArchitectureRulesTest(unittest.TestCase):
    def test_api_module_does_not_reference_training_pipeline(self) -> None:
        api_main = Path("apps/api/main.py").read_text(encoding="utf-8")

        self.assertNotIn("data_worker", api_main)
        self.assertIn("@app.post(\"/predict\"", api_main)


if __name__ == "__main__":
    unittest.main()
