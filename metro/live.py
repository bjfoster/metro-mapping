from google.transit import gtfs_realtime_pb2

import urllib

class LiveService:

    api_key: str = "ImwtCNKCUE39Si1671KIa9AUK2KpcZBh9sAjKUMc"

    api_base_url: str = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs"

    realtime_feeds: dict[str, str] = {
        '1': api_base_url,
        '2': api_base_url,  
        '3': api_base_url,
        '4': api_base_url,
        '5': api_base_url,
        '5X': api_base_url,
        '6': api_base_url,
        '6X': api_base_url,
        '7': api_base_url,
        '7X': api_base_url,
        'GS': api_base_url + "-g",
        'A': api_base_url + "-ace",
        'B': api_base_url + "-bdfm",
        'C': api_base_url + "-ace",
        'D': api_base_url + "-bdfm",
        'E': api_base_url + "-ace",
        'F': api_base_url + "-bdfm",
        'FS': api_base_url + "-bdfm",
        'G': api_base_url + "-g",
        'J': api_base_url + "-jz",
        'L': api_base_url + "-l",
        'M': api_base_url + "-bdfm",
        'N': api_base_url + "-nqrw",
        'Q': api_base_url + "-nqrw",
        'R': api_base_url + "-nqrw",
        'H': None,
        'W': api_base_url + "-nqrw",
        'Z': api_base_url + "-jz",
        'SI': api_base_url + "-si"
    }

    def __init__(self):
        pass

    def get_gtfs_realtime_feed(self, url: str) -> gtfs_realtime_pb2.FeedMessage:

        feed = gtfs_realtime_pb2.FeedMessage()

        req = urllib.request.Request(url)
        req.add_header("x-api-key", self.api_key)

        response = urllib.request.urlopen(req)
        feed.ParseFromString(response.read())
        
        return feed