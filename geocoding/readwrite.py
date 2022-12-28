import csv


from .models import AddressRow


class CsvReader:
    def __init__(self, input_file):
        self._input_file = input_file

    @property
    def input_file(self):
        return self._input_file

    def read(self):
        result = []
        with open(self.input_file, mode='r', encoding="utf-8-sig") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                result.append(AddressRow(owner=row["Name"], address=row["Address"]))
        return result


class AddressGroupsWriter:
    def __init__(self, output_file):
        self._output_file = output_file

    @property
    def output_file(self):
        return self._output_file

    def write(self, data):
        lines = []
        for row in data.values():
            lines.append(", ".join(sorted(row)) + "\n")

        with open(self._output_file, "w", encoding="utf-8") as file:
            file.writelines(sorted(lines))
