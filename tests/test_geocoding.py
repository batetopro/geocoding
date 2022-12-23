#!/usr/bin/env python

"""Tests for `geocoding` package."""


import os
import unittest

from geocoding import geocoding


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class Settings:
    input_file = os.path.join(BASE_DIR, "data", "input.csv")
    output_file = os.path.join(BASE_DIR, "data", "output.txt")
    expected_output_file = os.path.join(BASE_DIR, "data", "expected_output.txt")


class TestGeocoding(unittest.TestCase):
    """Tests for `geocoding` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001_address_reader(self):
        reader = geocoding.AddressReader(Settings.input_file)
        self.assertEqual(len(reader.data), 6)

        address = reader.data[0]
        self.assertEqual(address.owner, 'Ivan Draganov')
        self.assertEqual(address.value, 'ul. Shipka 34, 1000 Sofia, Bulgaria')

    def test_002_geocoder(self):
        geocoder = geocoding.AddressGeocoder()
        latlng1 = geocoder.encode("ул. Шипка 34, София, България")
        latlng2 = geocoder.encode("ul. Shipka 34, 1000 Sofia, Bulgaria")
        latlng3 = geocoder.encode("Shipka Street 34, Sofia, Bulgaria")
        self.assertEqual(latlng1, latlng2)
        self.assertEqual(latlng2, latlng3)
