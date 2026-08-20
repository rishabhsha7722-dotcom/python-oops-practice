import numpy as np


class NumpyDatasetAnalyzer:

    def __init__(self, data):
        self.data = data
        self.array = None

    def validate_input(self):
        if not isinstance(self.data, list):
            raise TypeError("Dataset must be a list.")

        if len(self.data) == 0:
            raise ValueError("Dataset cannot be empty.")

        if not all(isinstance(row, list) for row in self.data):
            raise TypeError("Each row must be a list.")

        column_count = len(self.data[0])

        if column_count == 0:
            raise ValueError("Rows cannot be empty.")

        for row in self.data:
            if len(row) != column_count:
                raise ValueError(
                    "All rows must contain the same number of columns."
                )

            for value in row:
                if not isinstance(value, (int, float, np.number)):
                    raise TypeError(
                        "Dataset contains non-numeric values."
                    )

    def convert_to_array(self):
        self.array = np.array(self.data, dtype=float)
        return self.array

    def get_dataset_info(self):
        if self.array is None:
            self.convert_to_array()

        return {
            "rows": self.array.shape[0],
            "columns": self.array.shape[1],
            "dimensions": self.array.ndim,
            "size": self.array.size,
            "data_type": self.array.dtype
        }

    def get_column(self, column_index):
        return self.array[:, column_index]

    def get_row(self, row_index):
        return self.array[row_index, :]

    def calculate_column_mean(self):
        return np.mean(self.array, axis=0)

    def calculate_column_minimum(self):
        return np.min(self.array, axis=0)

    def calculate_column_maximum(self):
        return np.max(self.array, axis=0)

    def calculate_column_std(self):
        return np.std(self.array, axis=0)

    def scale_features(self):
        minimum = np.min(self.array, axis=0)
        maximum = np.max(self.array, axis=0)

        denominator = maximum - minimum

        scaled = np.zeros_like(self.array, dtype=float)

        non_constant = denominator != 0

        scaled[:, non_constant] = (
            (self.array[:, non_constant] - minimum[non_constant])
            / denominator[non_constant]
        )

        scaled[:, ~non_constant] = 0.0

        return scaled

    def feature_summary(self):
        return {
            "mean": self.calculate_column_mean(),
            "minimum": self.calculate_column_minimum(),
            "maximum": self.calculate_column_maximum(),
            "std": self.calculate_column_std()
        }

    def display_report(self):
        info = self.get_dataset_info()

        print("\n========== DATASET REPORT ==========")

        print(f"Rows       : {info['rows']}")
        print(f"Columns    : {info['columns']}")
        print(f"Dimensions : {info['dimensions']}")
        print(f"Size       : {info['size']}")
        print(f"Data Type  : {info['data_type']}")

        print("\nColumn 0:")
        print(self.get_column(0))

        print("\nFirst Row:")
        print(self.get_row(0))

        print("\nColumn Mean:")
        print(self.calculate_column_mean())

        print("\nColumn Minimum:")
        print(self.calculate_column_minimum())

        print("\nColumn Maximum:")
        print(self.calculate_column_maximum())

        print("\nColumn Standard Deviation:")
        print(self.calculate_column_std())

        print("\nMin-Max Scaled Features:")
        print(self.scale_features())

        summary = self.feature_summary()

        print("\nFeature Summary:")
        print("Mean     :", summary["mean"])
        print("Minimum  :", summary["minimum"])
        print("Maximum  :", summary["maximum"])
        print("Std      :", summary["std"])

    def split_features_target(self, target_index):
        X = np.delete(self.array, target_index, axis=1)
        y = self.array[:, target_index]

        return X, y


def main():

    data = [
        [25, 30000, 2],
        [30, 45000, 5],
        [35, 60000, 8],
        [40, 80000, 12],
        [45, 100000, 15]
    ]

    try:
        analyzer = NumpyDatasetAnalyzer(data)

        analyzer.validate_input()
        analyzer.convert_to_array()

        analyzer.display_report()

    except (TypeError, ValueError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()