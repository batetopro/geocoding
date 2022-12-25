import csv


from .models import AddressRow


class CsvReader:
    def __init__(self, input_file):
        self._input_file = input_file
        self._data = None

    @property
    def input_file(self):
        return self._input_file

    @property
    def data(self):
        if self._data is None:
            self._data = self.read()
        return self._data

    def read(self):
        line_count = 0
        data = []

        # TODO: handle with BOM with encoding="utf-8-sig", but the first line is skipped, so it is not important
        with open(self.input_file, mode='r', encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                line_count += 1

                if line_count == 1:
                    continue

                data.append(AddressRow(
                    owner=row[0],
                    address=row[1]
                ))

        return data


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
