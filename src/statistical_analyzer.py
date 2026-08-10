class StatisticalAnalyzer:
    
    def __init__(self, numbers):
        self.numbers = numbers

    def validate_input(self):
        if not isinstance(self.numbers, list):
            raise TypeError("Input must be a list.")

        if len(self.numbers) == 0:
            raise ValueError("List cannot be empty.")

        for value in self.numbers:
            if not isinstance(value, (int, float)):
                raise TypeError("Input must contain only numerical values.")

    def calculate_mean(self):
        return sum(self.numbers) / len(self.numbers)

    def calculate_median(self):
        data = sorted(self.numbers)
        n = len(data)
        mid = n // 2

        if n % 2 == 1:
            return data[mid]
        else:
            return (data[mid - 1] + data[mid]) / 2

    def calculate_mode(self):
        frequency = {}

        for value in self.numbers:
            frequency[value] = frequency.get(value, 0) + 1

        max_count = max(frequency.values())

        if max_count == 1:
            return "No unique mode"

        modes = []

        for key, value in frequency.items():
            if value == max_count:
                modes.append(key)

        if len(modes) == 1:
            return modes[0]

        return modes

    def find_minimum(self):
        return min(self.numbers)

    def find_maximum(self):
        return max(self.numbers)

    def count_unique_values(self):
        return len(set(self.numbers))

    def display_result(self):
        print("=" * 40)
        print("STATISTICAL REPORT")
        print("=" * 40)
        print("Original Data :", self.numbers)
        print("Mean :", round(self.calculate_mean(), 2))
        print("Median :", self.calculate_median())
        print("Mode :", self.calculate_mode())
        print("Minimum :", self.find_minimum())
        print("Maximum :", self.find_maximum())
        print("Unique Values :", self.count_unique_values())
        print("=" * 40)


def main():
    numbers = [10, 20, 20, 30, 40, 50]

    try:
        analyzer = StatisticalAnalyzer(numbers)
        analyzer.validate_input()
        analyzer.display_result()
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()