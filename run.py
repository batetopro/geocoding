from geocoding import geocoding


if __name__ == "__main__":
    input_file = input("Input file: ")
    output_file = input("Output file: ")
    manager = geocoding.AddressManager(input_file, output_file)
    manager.run()
