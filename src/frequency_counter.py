class FrequencyCounter:
    def __init__(self, numbers):
        
        self.numbers = numbers

    def validate_input(self):
        
        if not isinstance(self.numbers, list):
            raise TypeError("Error: Input must be a list.")

        if len(self.numbers) == 0:
            raise ValueError("Error: Input list cannot be empty.")

    def count_frequency(self):
    
        frequency = {}

        for number in self.numbers:
            if number in frequency:
                frequency[number] += 1
            else:
                frequency[number] = 1

        return frequency

    def display_result(self):
        frequency = self.count_frequency()

        print("Frequency Dictionary:")
        print(frequency)


def main():
    """
    Main function
    """
    try:
        # Sample Input
        numbers = [1, 2, 2, 3, 1, 5, 4, 2, 5, 5]

        # Create Object
        counter = FrequencyCounter(numbers)

        # Validate Input
        counter.validate_input()

        # Display Result
        counter.display_result()

    except Exception as error:
        print(error)


if __name__ == "__main__":
    main()