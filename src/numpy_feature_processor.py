import numpy as np


class NumpyFeatureProcessor:

    def __init__(self, data):
        self.data = data
        self.array = None
        self.min_max_data = None
        self.standardized_data = None

    def validate_input(self):
        if not isinstance(self.data, list):
            raise TypeError("Input must be a list.")

        if len(self.data) == 0:
            raise ValueError("Input list cannot be empty.")

        if not all(
            isinstance(value, (int, float, np.number))
            for value in self.data
        ):
            raise ValueError("Dataset contains non-numeric values.")

        return True

    def convert_to_array(self):
        self.array = np.array(self.data)
        return self.array

    def get_array_info(self):
        return {
            "array": self.array,
            "dtype": self.array.dtype,
            "ndim": self.array.ndim,
            "shape": self.array.shape,
            "size": self.array.size
        }

    def calculate_minimum(self):
        return np.min(self.array)

    def calculate_maximum(self):
        return np.max(self.array)

    def calculate_mean(self):
        return np.mean(self.array)

    def calculate_standard_deviation(self):
        return np.std(self.array)

    def min_max_scale(self):
        minimum = self.calculate_minimum()
        maximum = self.calculate_maximum()

        if maximum == minimum:
            raise ValueError(
                "Cannot perform Min-Max Scaling when all values are identical."
            )

        self.min_max_data = (
            self.array - minimum
        ) / (maximum - minimum)

        return self.min_max_data

    def standardize(self):
        mean = self.calculate_mean()
        standard_deviation = self.calculate_standard_deviation()

        if standard_deviation == 0:
            raise ValueError(
                "Cannot perform Z-Score Standardization "
                "when standard deviation is zero."
            )

        self.standardized_data = (
            self.array - mean
        ) / standard_deviation

        return self.standardized_data

    def display_report(self):
        info = self.get_array_info()

        print("=" * 50)
        print(" NUMPY FEATURE PROCESSING REPORT")
        print("=" * 50)

        print(f"Original Data: {self.data}")
        print(f"NumPy Array: {info['array']}")
        print(f"Data Type: {info['dtype']}")
        print(f"Dimensions: {info['ndim']}")
        print(f"Shape: {info['shape']}")
        print(f"Size: {info['size']}")

        print(f"Minimum: {self.calculate_minimum()}")
        print(f"Maximum: {self.calculate_maximum()}")
        print(f"Mean: {self.calculate_mean():.4f}")
        print(
            f"Standard Deviation: "
            f"{self.calculate_standard_deviation():.4f}"
        )

        min_max = self.min_max_scale()
        standardized = self.standardize()

        print(f"Min-Max Scaled: {np.round(min_max, 4)}")
        print(
            f"Z-Score Standardized: "
            f"{np.round(standardized, 4)}"
        )

        print("=" * 50)


def main():
    data = [10, 20, 30, 40, 50]

    try:
        obj = NumpyFeatureProcessor(data)

        obj.validate_input()
        obj.convert_to_array()
        obj.display_report()

    except (TypeError, ValueError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()