import unittest
import tempfile
from pathlib import Path
import pandas as pd
from src.customer_data_pipeline import CustomerDataPipeline

VALID = {
    "CustomerID": ["C1", "C2"],
    "Age": [25, 30],
    "Income": [30000, 40000],
    "Experience": [2, 0],
    "PurchaseAmount": [1000, 6000],
    "Purchased": [0, 1],
}

class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "sample.csv"
        pd.DataFrame(VALID).to_csv(self.path, index=False)

    def tearDown(self):
        self.tmp.cleanup()

    def test_1_valid_csv(self):
        p = CustomerDataPipeline(str(self.path))
        p.run_pipeline()
        self.assertIsNotNone(p.cleaned_df)

    def test_2_missing_file(self):
        p = CustomerDataPipeline(str(self.path.parent / "unknown.csv"))
        with self.assertRaises(FileNotFoundError): p.validate_file()

    def test_3_wrong_extension(self):
        p = CustomerDataPipeline(str(self.path.with_suffix(".txt")))
        with self.assertRaises(ValueError): p.validate_file()

    def test_4_missing_required_column(self):
        p = CustomerDataPipeline(str(self.path))
        p.load_data()
        p.df = p.df.drop(columns=["Income"])
        with self.assertRaises(ValueError): p.validate_columns()

    def test_5_missing_values_imputed(self):
        df = pd.DataFrame(VALID)
        df.loc[0, "Age"] = None
        df.to_csv(self.path, index=False)
        p = CustomerDataPipeline(str(self.path)); p.load_data()
        p.remove_duplicates(); p.handle_missing_values()
        self.assertFalse(p.cleaned_df[["Age", "Income", "PurchaseAmount"]].isna().any().any())

    def test_6_invalid_age_detected(self):
        df = pd.DataFrame(VALID); df.loc[0, "Age"] = -10
        df.to_csv(self.path, index=False)
        p = CustomerDataPipeline(str(self.path)); p.load_data()
        p.remove_duplicates(); p.handle_missing_values()
        self.assertEqual(len(p.detect_invalid_values()["Age <= 0"]), 1)

    def test_7_invalid_purchased_detected(self):
        df = pd.DataFrame(VALID); df.loc[0, "Purchased"] = 2
        df.to_csv(self.path, index=False)
        p = CustomerDataPipeline(str(self.path)); p.load_data()
        p.remove_duplicates(); p.handle_missing_values()
        self.assertEqual(len(p.detect_invalid_values()["Purchased not 0/1"]), 1)

    def test_8_zero_experience_no_division_error(self):
        p = CustomerDataPipeline(str(self.path)); p.load_data()
        p.remove_duplicates(); p.handle_missing_values(); p.create_features()
        self.assertEqual(p.cleaned_df.loc[1, "IncomePerExperience"], 0)

if __name__ == "__main__":
    unittest.main()
