"""Main module."""


import requests
import geocoder


from .models import AddressRow
from .readwrite import CsvReader, CsvWriter
from .stacker import DictStacker, DistanceStacker


class AddressGeocoder:
    def __init__(self):
        self._session = requests.Session()

    def __del__(self):
        self._session.close()

    def encode(self, rows):
        addresses = [r.address for r in rows]
        lookup = geocoder.bing(addresses, session=self._session, method='batch')
        for k, r in enumerate(lookup):
            rows[k].set_latlng(r.latlng)
        return rows


class AddressManager:
    def __init__(self, input_file, output_file, geo_encoder=None, stacker=None):
        self._input_reader = CsvReader(input_file)
        self._output_writer = CsvWriter(output_file)
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
            self._stacker = DictStacker()
        return self._stacker

    def run(self):
        self.geocoder.encode(self.reader.data)
        self.writer.write(self.stacker.stack(self.reader.data))
