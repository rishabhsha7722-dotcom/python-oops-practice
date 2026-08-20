import pandas as pd


class PandasDataAnalyzer:

    REQUIRED_COLUMNS = [
        "Customer",
        "Age",
        "Income",
        "Experience",
        "Purchased"
    ]

    def __init__(self, data):
        self.data = data
        self.df = None
        self.cleaned_df = None

    # Step 3 - Create DataFrame
    def create_dataframe(self):
        self.df = pd.DataFrame(
            self.data,
            columns=self.REQUIRED_COLUMNS
        )

        print("\nDataFrame Created Successfully:")
        print(self.df)

        return self.df

    # Step 4 - Validate input
    def validate_input(self):
        if not isinstance(self.data, list):
            raise ValueError("Input data must be a list.")

        if len(self.data) == 0:
            raise ValueError("Dataset cannot be empty.")

        for record in self.data:
            if len(record) != len(self.REQUIRED_COLUMNS):
                raise ValueError(
                    "All records must contain exactly "
                    f"{len(self.REQUIRED_COLUMNS)} values."
                )

        if self.df is not None:
            missing_columns = [
                column for column in self.REQUIRED_COLUMNS
                if column not in self.df.columns
            ]

            if missing_columns:
                raise ValueError(
                    f"Missing required columns: {missing_columns}"
                )

        print("\nInput validation successful.")
        return True

    # Step 5 - Dataset information
    def get_dataset_info(self):
        if self.df is None:
            raise ValueError("DataFrame has not been created.")

        print("\n===== DATASET INFORMATION =====")
        print("Rows:", self.df.shape[0])
        print("Columns:", self.df.shape[1])
        print("Column Names:", list(self.df.columns))
        print("Shape:", self.df.shape)
        print("\nData Types:")
        print(self.df.dtypes)

        return {
            "rows": self.df.shape[0],
            "columns": self.df.shape[1],
            "column_names": list(self.df.columns),
            "shape": self.df.shape,
            "dtypes": self.df.dtypes
        }

    # Step 6 - Find missing values
    def find_missing_values(self):
        if self.df is None:
            raise ValueError("DataFrame has not been created.")

        missing = self.df.isnull()

        print("\n===== MISSING VALUE DETAILS =====")
        print(missing)

        return missing

    # Step 6 - Count missing values
    def count_missing_values(self):
        if self.df is None:
            raise ValueError("DataFrame has not been created.")

        missing_count = self.df.isnull().sum()

        print("\n===== MISSING VALUE COUNT =====")
        print(missing_count)

        print(
            "\nTotal Missing Values:",
            missing_count.sum()
        )

        return missing_count

    # Step 7 - Find duplicates
    def find_duplicates(self):
        if self.df is None:
            raise ValueError("DataFrame has not been created.")

        duplicates = self.df.duplicated()

        print("\n===== DUPLICATE RECORDS =====")
        print(self.df[duplicates])

        print("Duplicate Records:", duplicates.sum())

        return duplicates

    # Step 8 - Remove duplicates
    def remove_duplicates(self):
        if self.df is None:
            raise ValueError("DataFrame has not been created.")

        self.cleaned_df = self.df.drop_duplicates().copy()

        print("\n===== AFTER REMOVING DUPLICATES =====")
        print(self.cleaned_df)

        return self.cleaned_df

    # Step 9 - Fill missing Income values
    def fill_missing_values(self):
        if self.cleaned_df is None:
            raise ValueError(
                "Remove duplicates before filling missing values."
            )

        income_mean = self.cleaned_df["Income"].mean()

        self.cleaned_df["Income"] = (
            self.cleaned_df["Income"].fillna(income_mean)
        )

        print("\n===== AFTER FILLING MISSING INCOME =====")
        print(self.cleaned_df)

        print(
            "\nIncome Mean Used For Imputation:",
            income_mean
        )

        return self.cleaned_df

    # Step 10 - Filtering
    def filter_customers(self, min_income):
        if self.cleaned_df is None:
            raise ValueError("Cleaned DataFrame is not available.")

        filtered_df = self.cleaned_df[
            self.cleaned_df["Income"] >= min_income
        ]

        print(
            f"\n===== CUSTOMERS WITH INCOME >= {min_income} ====="
        )
        print(filtered_df)

        return filtered_df

    # Step 11 - Sorting
    def sort_by_income(self, ascending=True):
        if self.cleaned_df is None:
            raise ValueError("Cleaned DataFrame is not available.")

        sorted_df = self.cleaned_df.sort_values(
            by="Income",
            ascending=ascending
        )

        print("\n===== SORTED BY INCOME =====")
        print(sorted_df)

        return sorted_df

    # Step 12 - Statistics
    def calculate_statistics(self):
        if self.cleaned_df is None:
            raise ValueError("Cleaned DataFrame is not available.")

        numerical_columns = [
            "Age",
            "Income",
            "Experience",
            "Purchased"
        ]

        statistics = self.cleaned_df[numerical_columns].agg(
            ["mean", "min", "max", "std"]
        )

        print("\n===== NUMERICAL STATISTICS =====")
        print(statistics)

        return statistics

    # Step 13 - Feature Analysis
    def analyze_features(self):
        if self.cleaned_df is None:
            raise ValueError("Cleaned DataFrame is not available.")

        features = [
            "Age",
            "Income",
            "Experience",
            "Purchased"
        ]

        print("\n===== FEATURE ANALYSIS =====")

        for feature in features:
            print(f"\n{feature}")
            print("Mean:",
                  self.cleaned_df[feature].mean())
            print("Minimum:",
                  self.cleaned_df[feature].min())
            print("Maximum:",
                  self.cleaned_df[feature].max())
            print("Standard Deviation:",
                  self.cleaned_df[feature].std())

    # Step 14 - Target Analysis
    def analyze_target(self):
        if self.cleaned_df is None:
            raise ValueError("Cleaned DataFrame is not available.")

        purchased_count = (
            self.cleaned_df["Purchased"] == 1
        ).sum()

        not_purchased_count = (
            self.cleaned_df["Purchased"] == 0
        ).sum()

        print("\n===== PURCHASE ANALYSIS =====")
        print("Purchased:", purchased_count)
        print("Not Purchased:", not_purchased_count)

        return {
            "Purchased": purchased_count,
            "Not Purchased": not_purchased_count
        }

    # Step 15 - EDA
    def perform_eda(self):
        if self.cleaned_df is None:
            raise ValueError("Cleaned DataFrame is not available.")

        customer_count = len(self.cleaned_df)

        average_age = self.cleaned_df["Age"].mean()

        average_income = self.cleaned_df["Income"].mean()

        highest_income = self.cleaned_df["Income"].max()

        average_experience = (
            self.cleaned_df["Experience"].mean()
        )

        number_of_purchasers = (
            self.cleaned_df["Purchased"] == 1
        ).sum()

        eda_results = {
            "Customer Count": customer_count,
            "Average Age": average_age,
            "Average Income": average_income,
            "Highest Income": highest_income,
            "Average Experience": average_experience,
            "Number of Purchasers": number_of_purchasers
        }

        print("\n===== EXPLORATORY DATA ANALYSIS =====")

        for key, value in eda_results.items():
            print(f"{key}: {value}")

        return eda_results

    # Bonus Challenge
    def group_by_purchase_status(self):
        if self.cleaned_df is None:
            raise ValueError("Cleaned DataFrame is not available.")

        grouped = self.cleaned_df.groupby("Purchased").agg(
            Customer_Count=("Customer", "count"),
            Average_Age=("Age", "mean"),
            Average_Income=("Income", "mean"),
            Average_Experience=("Experience", "mean")
        )

        print("\n===== GROUP BY PURCHASE STATUS =====")
        print(grouped)

        return grouped

    # Step 16 - Final Report
    def display_report(self):
        if self.cleaned_df is None:
            raise ValueError("Cleaned DataFrame is not available.")

        statistics = self.calculate_statistics()
        target = self.analyze_target()

        print("\n")
        print("=" * 50)
        print("       CUSTOMER DATA ANALYSIS")
        print("=" * 50)

        print(
            "Original Dataset Shape:",
            self.df.shape
        )

        print(
            "Missing Income Values:",
            self.df["Income"].isnull().sum()
        )

        print(
            "Duplicate Records:",
            self.df.duplicated().sum()
        )

        print(
            "Rows After Cleaning:",
            len(self.cleaned_df)
        )

        print("\nFeature Statistics:")
        print(statistics)

        print("\nPurchase Analysis:")
        print("Purchased:", target["Purchased"])
        print("Not Purchased:", target["Not Purchased"])

        print("\nEDA Summary:")
        self.perform_eda()

        print("=" * 50)


# Step 17 - Main
def main():

    data = [
        ["C001", 25, 30000, 2, 0],
        ["C002", 30, 45000, 5, 1],
        ["C003", 35, None, 8, 1],
        ["C004", 40, 80000, 12, 1],
        ["C005", 45, 100000, 15, 0],
        ["C002", 30, 45000, 5, 1]
    ]

    try:
        analyzer = PandasDataAnalyzer(data)

        # Required workflow
        analyzer.create_dataframe()
        analyzer.validate_input()
        analyzer.get_dataset_info()
        analyzer.find_missing_values()
        analyzer.count_missing_values()
        analyzer.find_duplicates()
        analyzer.remove_duplicates()
        analyzer.fill_missing_values()
        analyzer.filter_customers(50000)
        analyzer.sort_by_income(ascending=True)
        analyzer.sort_by_income(ascending=False)
        analyzer.calculate_statistics()
        analyzer.analyze_features()
        analyzer.perform_eda()
        analyzer.analyze_target()
        analyzer.group_by_purchase_status()
        analyzer.display_report()

    except ValueError as error:
        print("\nInput Error:", error)

    except Exception as error:
        print("\nUnexpected Error:", error)


if __name__ == "__main__":
    main()