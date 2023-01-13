from math import radians, cos, sin, asin, sqrt


AVG_EARTH_RADIUS = 6371  # in km
ROUND_DICT_STACKER = 10000
MAX_CLUSTER_DISTANCE = 5  # in m


class AddressGroupMatcher:
    @classmethod
    def group(cls, data):
        raise NotImplemented()


class DictGroupMatcher(AddressGroupMatcher):
    @classmethod
    def group(cls, data):
        result = {}
        for row in data:
            if row.lat is None and row.lng is None:
                key = "NONE"
            else:
                key = (
                    round(row.lat * ROUND_DICT_STACKER) / ROUND_DICT_STACKER,
                    round(row.lng * ROUND_DICT_STACKER) / ROUND_DICT_STACKER
                )
            if key not in result:
                result[key] = []
            result[key].append(row.owner)
        return result


class DistanceGroupMatcher(AddressGroupMatcher):
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
    def group(cls, data):
        vertices, result = filter_none_latlng_and_get_vertices(data)
        distance_matrix = create_distance_matrix(vertices, cls.distance)
        cluster_matrix = [None for _ in vertices]
        current_cluster = 0

        for vertex in range(len(vertices)):
            if cluster_matrix[vertex] is not None:
                continue

            queue = [vertex]
            while len(queue) > 0:
                source = queue.pop(0)
                if cluster_matrix[source] is not None:
                    continue
                cluster_matrix[source] = current_cluster

                for target in range(source, len(vertices)):
                    if distance_matrix[source][target] < MAX_CLUSTER_DISTANCE:
                        queue.append(target)
            current_cluster += 1

        for row_index, cluster in enumerate(cluster_matrix):
            if cluster not in result:
                result[cluster] = []
            result[cluster].append(vertices[row_index].owner)
        return result


def create_distance_matrix(data, func):
    return [[func(item_1, item_2) for item_2 in data] for item_1 in data]


def filter_none_latlng_and_get_vertices(data):
    result = {}
    vertices = []

    for row in data:
        if row.lat is None and row.lng is None:
            if "NONE" not in result:
                result["NONE"] = []
            result["NONE"].append(row.owner)
        else:
            vertices.append(row)

    return vertices, result
