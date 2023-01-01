"""Main module."""


import requests
import geocoder


from .models import AddressRow
from .readwrite import CsvReader, AddressGroupsWriter
from .group_matcher import DictGroupMatcher, DistanceGroupMatcher


def main():
    input_file = input("Input file: ")
    output_file = input("Output file: ")
    manager = AddressManager(input_file, output_file, group_matcher=DistanceGroupMatcher())
    manager.run()


class AddressGeocoder:
    def __init__(self):
        self._session = requests.Session()

    def __del__(self):
        self._session.close()

    def lookup(self, address):
        raise NotImplemented()

    def encode(self, rows):
        result = []
        for k, row in enumerate(rows):
            latlng = self.lookup(row.address)
            if latlng:
                row.set_latlng(latlng)
            result.append(row)
        return result


class DummyAddressEncoder(AddressGeocoder):
    mapping = {
        "ul. Shipka 34, 1000 Sofia, Bulgaria": (42.69299, 23.34007),
        "1 Guanghua Road, Beijing, China 100020": (39.91392, 116.46064),
        "ул. Шипка 34, София, България": (42.6929848, 23.340067),
        "Shipka Street 34, Sofia, Bulgaria": (42.69299, 23.34007),
        "1 Guanghua Road, Chaoyang District, Beijing, P.R.C 100020": (39.91392, 116.46064),
        "Konrad-Adenauer-Straße 7, 60313 Frankfurt am Main, Germany": (50.11568, 8.687338),
    }

    def lookup(self, address):
        return self.mapping.get(address)


class BingAddressEncoder(AddressGeocoder):
    def lookup(self, address):
        return geocoder.bing(address, session=self._session).latlng


class LocationIQAddressEncoder(AddressGeocoder):
    def lookup(self, address):
        return geocoder.locationiq(address, session=self._session).latlng


class AddressManager:
    def __init__(self, input_file, output_file, geo_encoder=None, group_matcher=None):
        self._input_reader = CsvReader(input_file)
        self._output_writer = AddressGroupsWriter(output_file)
        self._geocoder = geo_encoder
        self._group_matcher = group_matcher

    @property
    def reader(self):
        return self._input_reader

    @property
    def writer(self):
        return self._output_writer

    @property
    def geocoder(self):
        if self._geocoder is None:
            self._geocoder = BingAddressEncoder()
        return self._geocoder

    @property
    def group_matcher(self):
        if self._group_matcher is None:
            self._group_matcher = DictGroupMatcher()
        return self._group_matcher

    def run(self):
        data = self.reader.read()
        self.geocoder.encode(data)
        self.writer.write(self.group_matcher.group(data))
