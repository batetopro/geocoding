

class DictStacker:
    @classmethod
    def stack(cls, data):
        result = {}
        for row in data:
            latlng = (
                round(row.lat * 10000) / 10000,
                round(row.lng * 10000) / 10000
            )
            if latlng not in result:
                result[latlng] = []
            result[latlng].append(row.owner)
        return result


class DistanceStacker:
    @classmethod
    def stack(cls, data):
        pass
