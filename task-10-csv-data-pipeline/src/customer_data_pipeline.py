from pathlib import Path
import pandas as pd
import numpy as np


class CustomerDataPipeline:
    REQUIRED_COLUMNS = [
        "CustomerID", "Age", "Income", "Experience",
        "PurchaseAmount", "Purchased"
    ]
    NUMERIC_COLUMNS = ["Age", "Income", "Experience", "PurchaseAmount"]

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.cleaned_df = None
        self.summary = {}

    def validate_file(self):
        if not isinstance(self.file_path, (str, Path)):
            raise TypeError("file_path must be a string or pathlib Path.")
        path = Path(self.file_path)
        if path.suffix.lower() != ".csv":
            raise ValueError("Only CSV files are supported.")
        if not path.is_file():
            raise FileNotFoundError(f"CSV file does not exist: {path}")

    def load_data(self):
        self.validate_file()
        self.df = pd.read_csv(self.file_path)
        return self.df

    def validate_columns(self):
        if self.df is None:
            raise RuntimeError("Load the CSV before validating columns.")
        missing = [col for col in self.REQUIRED_COLUMNS if col not in self.df.columns]
        if missing:
            raise ValueError(f"Required columns are missing: {missing}")

    def inspect_dataset(self):
        print("\\n--- Dataset Inspection ---")
        print("Shape:", self.df.shape)
        print("Rows:", self.df.shape[0])
        print("Columns:", self.df.shape[1])
        print("Column names:", self.df.columns.tolist())
        print("\\nData types:\\n", self.df.dtypes)
        print("\\nMemory usage (bytes):\\n", self.df.memory_usage(deep=True))
        return self.df.info()

    def generate_quality_report(self):
        report = pd.DataFrame({
            "DataType": self.df.dtypes.astype(str),
            "MissingCount": self.df.isna().sum(),
            "MissingPercentage": (self.df.isna().sum() / len(self.df) * 100).round(2),
            "UniqueValues": self.df.nunique(dropna=True)
        })
        self.summary["quality_report"] = report
        print("\\n--- Data Quality Report ---\\n", report)
        report.to_csv("output/data_quality_report.csv", index=True)
        return report

    def find_duplicates(self):
        duplicates = self.df.duplicated()
        print("\\nDuplicate rows:", int(duplicates.sum()))
        if duplicates.any():
            print(self.df.loc[duplicates])
        return self.df.loc[duplicates].copy()

    def remove_duplicates(self):
        self.cleaned_df = self.df.drop_duplicates().copy()
        return self.cleaned_df

    def handle_missing_values(self):
        if self.cleaned_df is None:
            raise RuntimeError("Remove duplicates before imputing missing values.")
        for col in ["Age", "Income", "PurchaseAmount"]:
            self.cleaned_df[col] = pd.to_numeric(self.cleaned_df[col], errors="coerce")
            median_value = self.cleaned_df[col].median()
            self.cleaned_df[col] = self.cleaned_df[col].fillna(median_value)
        for col in ["Experience", "Purchased"]:
            self.cleaned_df[col] = pd.to_numeric(self.cleaned_df[col], errors="coerce")
        return self.cleaned_df

    def detect_invalid_values(self):
        df = self.cleaned_df
        invalid = {
            "Age <= 0": df[df["Age"] <= 0],
            "Income < 0": df[df["Income"] < 0],
            "Experience < 0": df[df["Experience"] < 0],
            "PurchaseAmount < 0": df[df["PurchaseAmount"] < 0],
            "Purchased not 0/1": df[~df["Purchased"].isin([0, 1])]
        }
        print("\\n--- Invalid Value Checks ---")
        for issue, rows in invalid.items():
            print(f"{issue}: {len(rows)} row(s)")
        self.summary["invalid_value_counts"] = {k: len(v) for k, v in invalid.items()}
        return invalid

    def validate_cleaned_data(self):
        df = self.cleaned_df
        if df.isna().any().any():
            raise ValueError("Cleaned dataset still contains missing values.")
        if df.duplicated().any():
            raise ValueError("Cleaned dataset still contains duplicate rows.")
        for col in self.NUMERIC_COLUMNS + ["Purchased"]:
            if not pd.api.types.is_numeric_dtype(df[col]):
                raise TypeError(f"{col} must have a numeric data type.")
        if not df["Purchased"].isin([0, 1]).all():
            raise ValueError("Purchased must contain only 0 or 1.")
        return True

    def create_features(self):
        # Use NaN when Experience is zero; avoid division-by-zero.
        self.cleaned_df["IncomePerExperience"] = (
            self.cleaned_df["Income"] /
            self.cleaned_df["Experience"].replace(0, np.nan)
        )
        self.cleaned_df["IncomePerExperience"] = (
            self.cleaned_df["IncomePerExperience"].replace([np.inf, -np.inf], np.nan)
        )
        self.cleaned_df["IncomePerExperience"] = self.cleaned_df[
            "IncomePerExperience"
        ].fillna(0)

        bins = [-np.inf, 2000, 5000, np.inf]
        labels = ["Low", "Medium", "High"]
        # Assignment says <2000 Low, 2000–5000 Medium, >5000 High.
        self.cleaned_df["PurchaseCategory"] = pd.cut(
            self.cleaned_df["PurchaseAmount"],
            bins=[-np.inf, 2000, 5000, np.inf],
            labels=labels,
            right=True,
            include_lowest=True
        )
        # Exactly 2000 is Medium per task; fix boundary explicitly.
        self.cleaned_df.loc[self.cleaned_df["PurchaseAmount"] == 2000, "PurchaseCategory"] = "Medium"
        self.cleaned_df.loc[self.cleaned_df["PurchaseAmount"] == 5000, "PurchaseCategory"] = "Medium"
        return self.cleaned_df

    def create_age_group(self):
        self.cleaned_df["AgeGroup"] = np.select(
            [self.cleaned_df["Age"] < 30, self.cleaned_df["Age"].between(30, 40)],
            ["Young", "Adult"],
            default="Senior"
        )
        return self.cleaned_df

    def get_high_value_customers(self):
        return self.cleaned_df[self.cleaned_df["PurchaseAmount"] > 5000].copy()

    def sort_by_purchase_amount(self):
        return self.cleaned_df.sort_values("PurchaseAmount", ascending=False)

    def calculate_statistics(self):
        columns = ["Age", "Income", "Experience", "PurchaseAmount", "IncomePerExperience"]
        stats = self.cleaned_df[columns].agg(["mean", "median", "min", "max", "std"]).T
        print("\\n--- Statistics ---\\n", stats)
        self.summary["statistics"] = stats
        return stats

    def calculate_correlation(self):
        columns = ["Age", "Income", "Experience", "PurchaseAmount", "Purchased"]
        corr = self.cleaned_df[columns].corr(numeric_only=True)
        print("\\n--- Correlation ---\\n", corr)
        self.summary["correlation"] = corr
        return corr

    def analyze_by_purchase_status(self):
        grouped = self.cleaned_df.groupby("Purchased").agg(
            CustomerCount=("CustomerID", "count"),
            AverageAge=("Age", "mean"),
            AverageIncome=("Income", "mean"),
            AveragePurchaseAmount=("PurchaseAmount", "mean")
        )
        print("\\n--- Grouped by Purchase Status ---\\n", grouped)
        return grouped

    def perform_eda(self):
        df = self.cleaned_df
        result = {
            "total_customers": len(df),
            "average_age": df["Age"].mean(),
            "average_income": df["Income"].mean(),
            "median_income": df["Income"].median(),
            "highest_purchase": df["PurchaseAmount"].max(),
            "average_purchase": df["PurchaseAmount"].mean(),
            "purchasers": int((df["Purchased"] == 1).sum()),
            "non_purchasers": int((df["Purchased"] == 0).sum()),
            "most_common_age_group": df["AgeGroup"].mode().iloc[0],
            "most_common_purchase_category": df["PurchaseCategory"].mode().iloc[0]
        }
        self.summary["eda"] = result
        print("\\n--- EDA Summary ---")
        for key, value in result.items():
            print(f"{key}: {value}")
        pd.Series(result, name="Value").to_csv("output/eda_summary.csv")
        return result

    def export_clean_data(self):
        output_path = Path("output/cleaned_customer_data.csv")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.cleaned_df.to_csv(output_path, index=False)
        print(f"\\nCleaned dataset exported to: {output_path}")
        return output_path

    def generate_ml_ready_data(self):
        features = [
            "Age", "Income", "Experience", "PurchaseAmount",
            "IncomePerExperience"
        ]
        X = self.cleaned_df[features].copy()
        y = self.cleaned_df["Purchased"].copy()
        return X, y

    def run_pipeline(self):
        self.validate_file()
        self.load_data()
        self.validate_columns()
        self.inspect_dataset()
        self.generate_quality_report()
        self.find_duplicates()
        self.remove_duplicates()
        self.handle_missing_values()
        self.validate_cleaned_data()
        self.detect_invalid_values()
        self.create_features()
        self.create_age_group()
        self.calculate_statistics()
        self.perform_eda()
        self.calculate_correlation()
        self.analyze_by_purchase_status()
        self.get_high_value_customers()
        self.sort_by_purchase_amount()
        self.export_clean_data()
        print("\\nPipeline completed successfully.")


def main():
    pipeline = CustomerDataPipeline("data/customer_data.csv")
    try:
        pipeline.run_pipeline()
    except (FileNotFoundError, TypeError, ValueError, RuntimeError) as error:
        print("Pipeline failed:", error)


if __name__ == "__main__":
    main()
