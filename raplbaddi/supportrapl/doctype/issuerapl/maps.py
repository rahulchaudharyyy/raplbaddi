import googlemaps
import abc


class MapClient(abc.ABC):
    def get_distance(origins: list[str], destinations: list[str]):
        pass


class GoogleMapClient(MapClient):
    def __init__(self) -> None:
        self.api_key = self._get_api_key()
        self.chunk_size = 25
        self.client = self._get_map_client()

    def _get_map_client(self):
        return googlemaps.Client(key=self.api_key)

    def _distance_matrix(self, origin, destinations):
        return self.client.distance_matrix(origin, destinations)

    def _get_api_key(self):
        return "AIzaSyAO5NhknKUS-KUOTjs48mRC9PBAWi2hB70"

    def _distance_matix(self, origin, destinations):
        dms = []
        for destination in self._split_addresses(destinations):
            dm = self._distance_matrix(
                origin=origin, destinations=destination
            )
            for i in range(len(dm['destination_addresses'])):
                dm['destination_addresses'][i] = destination[i]
            dms.append(dm)
        print(dms)
        return dms

    def get_distance(self, origin: str, destinations: list[str]):
        dms = self._distance_matix(origin, destinations)
        matrix = {}
        for dm in dms:
            if "rows" in dm and dm["rows"]:
                for i, row in enumerate(dm["rows"]):
                    if "elements" in row and row["elements"]:
                        for j, element in enumerate(row["elements"]):
                            origin_address = dm["destination_addresses"][j]
                            if "status" in element and element["status"] == "OK":
                                distance = int(element["distance"]["value"] / 1000)
                                matrix[origin_address] = distance
        options = [
            {
                "label": str(matrix[key]) + ": " + key,
                "value": str(matrix[key]) + ":" + key,
                "km": matrix[key],
            }
            for key in matrix
        ]
        options_sorted = sorted(options, key=lambda x: x["km"], reverse=False)
        return options_sorted

    def _split_addresses(self, destinations):
        return [
            destinations[i : i + self.chunk_size]
            for i in range(0, len(destinations), self.chunk_size)
        ]
