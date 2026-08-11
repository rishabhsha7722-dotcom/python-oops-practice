class MissingValueHandler:
    
    def __init__(self, data):
        self.data = data
        self.cleaned_data = []

    def validate_input(self):
        if not isinstance(self.data, list):
            raise TypeError("Input must be a list.")

        if len(self.data) == 0:
            raise ValueError("Input list cannot be empty.")

        for value in self.data:
            if value is not None and not isinstance(value, (int, float)):
                raise ValueError("Dataset contains invalid values.")

    def find_missing_indexes(self):
        indexes = []
        for i in range(len(self.data)):
            if self.data[i] is None:
                indexes.append(i)
        return indexes

    def count_missing_values(self):
        count = 0
        for value in self.data:
            if value is None:
                count += 1
        return count

    def calculate_mean(self):
        total = 0
        count = 0

        for value in self.data:
            if value is not None:
                total += value
                count += 1

        if count == 0:
            raise ValueError("No valid values exist to calculate the mean.")

        return total / count

    def fill_missing_values(self):
        mean = self.calculate_mean()
        self.cleaned_data = []

        for value in self.data:
            if value is None:
                self.cleaned_data.append(mean)
            else:
                self.cleaned_data.append(value)

    def display_report(self):
        self.fill_missing_values()

        print("=" * 40)
        print("MISSING VALUE REPORT")
        print("=" * 40)

        print("Original Data:")
        print(self.data)

        print("Total Values :", len(self.data))
        print("Missing Values :", self.count_missing_values())
        print("Missing Indexes :", self.find_missing_indexes())

        available = len(self.data) - self.count_missing_values()
        print("Available Values :", available)

        print("Mean :", self.calculate_mean())

        print("Cleaned Data:")
        print(self.cleaned_data)

        print("=" * 40)


def main():
    data = [25, 30, None, 40, None, 35, 28]

    try:
        obj = MissingValueHandler(data)
        obj.validate_input()
        obj.display_report()

    except Exception as error:
        print("Error:", error)


if __name__ == "__main__":
    main()