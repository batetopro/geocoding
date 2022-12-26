"""Main module."""


import requests
import geocoder


from .models import AddressRow
from .readwrite import CsvReader, AddressGroupsWriter
from .group_matcher import DictGroupMatcher, DistanceGroupMatcher


def main():
    input_file = input("Input file: ")
    output_file = input("Output file: ")
    manager = AddressManager(input_file, output_file, stacker=DistanceGroupMatcher())
    manager.run()


class AddressGeocoder:
    def __init__(self):
        self._session = requests.Session()

    def __del__(self):
        self._session.close()

    def encode(self, rows):
        result = []
        for k, row in enumerate(rows):
            g = geocoder.bing(row.address, session=self._session)
            if g.latlng:
                row.set_latlng(g.latlng)
            result.append(row)
        return result


class AddressManager:
    def __init__(self, input_file, output_file, geo_encoder=None, stacker=None):
        self._input_reader = CsvReader(input_file)
        self._output_writer = AddressGroupsWriter(output_file)
        self._geocoder = geo_encoder
        self._stacker = stacker

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

    @property
    def stacker(self):
        if self._stacker is None:
            self._stacker = DictGroupMatcher()
        return self._stacker

    def run(self):
        data = self.reader.read()
        self.geocoder.encode(data)
        self.writer.write(self.stacker.group(data))
