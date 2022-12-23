

class AddressRow:
    def __init__(self, owner, address):
        self._owner = owner
        self._address = address
        self._lat = None
        self._lng = None

    @property
    def owner(self):
        return self._owner

    @property
    def address(self):
        return self._address

    @property
    def lat(self):
        return self._lat

    @property
    def lng(self):
        return self._lng

    def set_latlng(self, latlng):
        self._lat = latlng[0]
        self._lng = latlng[1]

    def __repr__(self):
        return "AddressRow(owner='{}', address='{}', latlng={},{})".format(
            self.owner, self.address, self.lat, self.lng)
