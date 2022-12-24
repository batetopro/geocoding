from math import radians, cos, sin, asin, sqrt


AVG_EARTH_RADIUS = 6371  # in km
ROUND_DICT_STACKER = 10000
MAX_CLUSTER_DISTANCE = 5  # in m


class DictStacker:
    @classmethod
    def stack(cls, data):
        result = {}
        for row in data:
            latlng = (
                round(row.lat * ROUND_DICT_STACKER) / ROUND_DICT_STACKER,
                round(row.lng * ROUND_DICT_STACKER) / ROUND_DICT_STACKER
            )
            if latlng not in result:
                result[latlng] = []
            result[latlng].append(row.owner)
        return result


class DistanceStacker:
    @classmethod
    def distance(cls, first_row, second_row):
        lat1 = radians(first_row.lat)
        lng1 = radians(first_row.lng)
        lat2 = radians(second_row.lat)
        lng2 = radians(second_row.lng)

        lat = lat2 - lat1
        lng = lng2 - lng1
        d = sin(lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(lng / 2) ** 2
        h = 2 * AVG_EARTH_RADIUS * asin(sqrt(d))

        return h * 1000

    @classmethod
    def stack(cls, data):
        result = {}
        m = []
        for i in range(len(data)):
            m.append([])
            for j in range(len(data)):
                m[i].append(cls.distance(data[i], data[j]))

        print(m)

        return result

