#!/usr/bin/env python

"""Tests for `geocoding` package."""


import os
import unittest
import filecmp


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

    def test_001_csv_reader(self):
        reader = geocoding.CsvReader(Settings.input_file)
        data = reader.read()

        self.assertEqual(len(data), 6)

        address = data[0]
        self.assertEqual(address.owner, 'Ivan Draganov')
        self.assertEqual(address.address, 'ul. Shipka 34, 1000 Sofia, Bulgaria')

    def test_002_geocoder(self):
        data = [
            geocoding.AddressRow(owner="Ilona Ilieva", address="ул. Шипка 34, София, България"),
            geocoding.AddressRow(owner="Ivan Draganov", address="ul. Shipka 34, 1000 Sofia, Bulgaria"),
            geocoding.AddressRow(owner="Dragan Doichinov", address="Shipka Street 34, Sofia, Bulgaria"),
            geocoding.AddressRow(owner="Dragomir Petkanov", address="metallica"),
        ]

        geocoder = geocoding.AddressGeocoder()
        geocoder.encode(data)

        self.assertEqual(data[1].lat, data[2].lat)
        self.assertEqual(data[1].lng, data[2].lng)
        self.assertIsNone(data[3].lat)
        self.assertIsNone(data[3].lng)

    def test_003_address_groups_writer(self):
        data = {
            'x': ['Ivan Draganov', 'Ilona Ilieva', 'Dragan Doichinov'],
            'y': ['Li Deng', 'Leon Wu'],
            'z': ['Frieda Müller'],
        }

        writer = geocoding.AddressGroupsWriter(Settings.output_file)
        writer.write(data)

        self.assertTrue(filecmp.cmp(Settings.output_file, Settings.expected_output_file))

    def test_004_dict_stacker(self):
        data = [
            geocoding.AddressRow(owner="Ilona Ilieva",
                                 address="ул. Шипка 34, София, България", lat=42.6929848, lng=23.340067),
            geocoding.AddressRow(owner="Ivan Draganov",
                                 address="ul. Shipka 34, 1000 Sofia, Bulgaria", lat=42.69299, lng=23.34007),
            geocoding.AddressRow(owner="Dragan Doichinov",
                                 address="Shipka Street 34, Sofia, Bulgaria", lat=42.69299, lng=23.34007),
            geocoding.AddressRow(owner="Dragomir Petkanov", address="metallica", lat=None, lng=None),
        ]
        stacker = geocoding.DictStacker()
        stacked = stacker.stack(data)
        self.assertEqual(len(stacked), 2)

    def test_005_distance_stacker(self):
        data = [
            geocoding.AddressRow(owner="Ilona Ilieva",
                                 address="ул. Шипка 34, София, България", lat=42.6929848, lng=23.340067),
            geocoding.AddressRow(owner="Ivan Draganov",
                                 address="ul. Shipka 34, 1000 Sofia, Bulgaria", lat=42.69299, lng=23.34007),
            geocoding.AddressRow(owner="Dragan Doichinov",
                                 address="Shipka Street 34, Sofia, Bulgaria", lat=42.69299, lng=23.34007),
            geocoding.AddressRow(owner="Dragomir Petkanov", address="metallica", lat=None, lng=None),
        ]
        stacker = geocoding.DistanceStacker()
        self.assertEqual(1, round(stacker.distance(data[0], data[1])))
        self.assertEqual(0, stacker.distance(data[1], data[2]))
        stacked = stacker.stack(data)
        self.assertEqual(len(stacked), 2)

    def test_006_address_manager(self):
        manager = geocoding.AddressManager(
            input_file=Settings.input_file,
            output_file=Settings.output_file
        )

        manager.run()

        self.assertTrue(filecmp.cmp(Settings.output_file, Settings.expected_output_file))

    def test_007_address_manager_distance(self):
        manager = geocoding.AddressManager(
            input_file=Settings.input_file,
            output_file=Settings.output_file,
            stacker=geocoding.DistanceStacker()
        )

        manager.run()

        self.assertTrue(filecmp.cmp(Settings.output_file, Settings.expected_output_file))
