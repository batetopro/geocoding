"""Main module."""
import csv
from dataclasses import dataclass


import requests
import geocoder


@dataclass(frozen=True)
class Address:
    owner: str
    value: str


class AddressReader:
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

                data.append(Address(
                    owner=row[0],
                    value=row[1]
                ))

        return data


class StackedAddressesWriter:
    def __init__(self, output_file):
        self._output_file = output_file

    @property
    def output_file(self):
        return self._output_file

    def write(self, data):
        pass


class AddressGeocoder:
    def __init__(self):
        self._session = requests.Session()

    def __del__(self):
        self._session.close()

    def encode(self, address):
        encoded = geocoder.bing(address, session=self._session)
        lat = round(encoded.latlng[0] * 10000) / 10000
        lng = round(encoded.latlng[1] * 10000) / 10000
        return lat, lng


class AddressStacker:
    def __init__(self, input_file, output_file, geocoder=None):
        self._input_reader = AddressReader(input_file)
        self._output_writer = output_file
        self._geocoder = geocoder

    @property
    def reader(self):
        return self._input_reader

    @property
    def writer(self):
        return self._output_writer

    @property
    def geocoder(self):
        if self._geocoder is None:
            self._geocoder = AddressGeocoder()
        return self._geocoder

    def stack_addresses(self):
        data = {}
        for address in self.reader.data:
            latlng = self.geocoder.encode(address.value)
            if latlng not in data:
                data[latlng] = []
            data[latlng].append(address.owner)
        self.writer.write(data)
