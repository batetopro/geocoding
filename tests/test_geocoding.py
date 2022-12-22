#!/usr/bin/env python

"""Tests for `geocoding` package."""


import os
import unittest

from geocoding import geocoding


BASE_DIR = os.path.basename(os.path.basename(__file__))


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
