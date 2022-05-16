from typing import Callable
import pandas as pd

import datetime


class Agency:

    def __init__(self, agency_df: pd.DataFrame) -> None:

        self.df = agency_df

        self.id: str = str(self.df['agency_id'][0])
        self.name: str = str(self.df['agency_name'][0])
        self.url: str = str(self.df['agency_url'][0])
        self.timezone: str = str(self.df['agency_timezone'][0])
        self.lang: str = str(self.df['agency_lang'][0])
        self.phone: str = str(self.df['agency_phone'][0])

        self.routes: dict[str, Route] = {}
        self.stops: dict[str, Stop] = {}
        self.services: dict[str, Service] = {}
        self.shapes: dict[str, Shape] = {}
        self.trips: dict[str, Trip] = {}
        self.stop_times: list[StopTime] = []

    def __str__(self) -> str:

        return f"🚇 ID: {self.id} Name: {self.name}"

    def generate_routes(self, routes_df: pd.DataFrame) -> None:

        for i, row in routes_df.iterrows():

            id = row['route_id']
            self.routes[id] = Route(row)

    def generate_stops(self, stops_df: pd.DataFrame) -> None:

        for i, row in stops_df.iterrows():

            id = row['stop_id']
            self.stops[id] = Stop(row)

    def generate_services(self, services_df: pd.DataFrame) -> None:

        for i, row in services_df.iterrows():

            id = row['service_id']
            self.services[id] = Service(row)

    def generate_shapes(self, shapes_df: pd.DataFrame) -> None:

        unique_shapes = shapes_df['shape_id'].unique()

        for unique_shape in unique_shapes:

            shape_df = shapes_df[shapes_df['shape_id'] == unique_shape]
            self.shapes[unique_shape] = Shape(unique_shape, shape_df)

    def generate_trips(self, trips_df: pd.DataFrame) -> None:

        for i, row in trips_df.iterrows():

            id = row['trip_id']
            self.trips[id] = Trip(row)

    def generate_stop_times(self, stop_times_df: pd.DataFrame) -> None:

        for i, row in stop_times_df.iterrows():

            self.stop_times.append(StopTime(row))

    def _cross_reference_trips(self) -> None:

        for trip in self.trips.values():

            trip.assign_route(self.routes[trip.route_id])
            trip.assign_service(self.services[trip.service_id])

            if len(trip.shape_id) > 0 and trip.shape_id != 'nan':
                trip.assign_shape(self.shapes[trip.shape_id])

    def _cross_reference_stops(self) -> None:

        for stop in self.stops.values():

            if len(stop.parent_station_id) > 0 and stop.parent_station_id != 'nan':
                stop.assign_parent_station(self.stops[stop.parent_station_id])

    def _cross_reference_stop_times(self) -> None:

        for stop_time in self.stop_times:

            stop_time.assign_stop(self.stops[stop_time.stop_id])
            stop_time.assign_trip(self.trips[stop_time.trip_id])

            stop_time.stop.add_stop_time(stop_time)
            stop_time.trip.add_stop_time(stop_time)

    def cross_reference_objects(self):

        self._cross_reference_trips()
        self._cross_reference_stops()
        self._cross_reference_stop_times()


class Route:

    def __init__(self, data_row: object) -> None:

        self.id: str = str(data_row['route_id'])
        self.agency_id = str(data_row['agency_id'])
        self.short_name: str = str(data_row['route_short_name'])
        self.long_name: str = str(data_row['route_long_name'])
        self.desc: str = str(data_row['route_desc'])
        self.type: str = str(data_row['route_type'])
        self.url: str = str(data_row['route_url'])
        self.color: str = str(data_row['route_color'])
        self.text_color: str = str(data_row['route_text_color'])

    def __str__(self) -> str:

        return f"📉 ID: {self.id} Long Name: {self.long_name}"


class Stop:

    def __init__(self, data_row: object) -> None:

        self.id: str = str(data_row['stop_id'])
        self.code: str = str(data_row['stop_code'])
        self.name: str = str(data_row['stop_name'])
        self.desc: str = str(data_row['stop_desc'])
        self.lat: str = str(data_row['stop_lat'])
        self.lon: str = str(data_row['stop_lon'])
        self.zone_id: str = str(data_row['zone_id'])
        self.url: str = str(data_row['stop_url'])
        self.location_type: str = str(data_row['location_type'])
        self.parent_station_id: str = str(data_row['parent_station'])

        self.parent_station: Stop = None
        self.child_stations: list[Stop] = []

        self.stop_times: list[StopTime] = []

    def __str__(self) -> str:

        return f"🛑 ID: {self.id} Name: {self.name}"

    def _add_child_station(self, child: Stop) -> None:

        self.child_stations.append(child)

    def assign_parent_station(self, parent_station: Stop) -> None:

        self.parent_station = parent_station
        self.parent_station._add_child_station(self)

    def add_stop_time(self, stop_time: StopTime) -> None:

        self.stop_times.append(stop_time)


class Service:

    weekdays: tuple = ('monday',
                       'tuesday',
                       'wednesday',
                       'thursday',
                       'friday',
                       'saturday',
                       'sunday')

    def __init__(self, data_row: object) -> None:

        self.id: str = data_row['service_id']

        self.days: list[bool] = []
        for day in self.weekdays:
            self.days.append(bool(data_row[day]))

        date_format = f"%Y%m%d"
        self.start_date: datetime.datetime = datetime.datetime.strptime(
            str(data_row['start_date']), date_format)
        self.end_date: datetime.datetime = datetime.datetime.strptime(
            str(data_row['end_date']), date_format)

    def __str__(self) -> str:

        return f"🚏 ID: {self.id}"


class Shape:

    def __init__(self, shape_id: str, shape_df: pd.DataFrame):

        self.id = shape_id

        self.lat: list[float] = []
        self.lon: list[float] = []
        self.sequence: list[int] = []
        self.dist_traveled: list[float] = []

        for i, row in shape_df.iterrows():

            self.lat.append(float(row['shape_pt_lat']))
            self.lon.append(float(row['shape_pt_lon']))
            self.sequence.append(int(row['shape_pt_sequence']))
            self.dist_traveled.append(float(row['shape_dist_traveled']))

    def __str__(self) -> str:

        return f"➿ ID: {self.id}"


class Trip:

    def __init__(self, data_row: object) -> None:

        self.id: str = str(data_row['trip_id'])

        self.route_id: str = str(data_row['route_id'])
        self.service_id: str = str(data_row['service_id'])
        self.headsign: str = str(data_row['trip_headsign'])
        self.direction_id: int = int(data_row['direction_id'])
        self.block_id: str = str(data_row['block_id'])
        self.shape_id: str = str(data_row['shape_id'])

        self.route: Route = None
        self.service: Service = None
        self.shape: Shape = None
        self.stop_times: list[StopTime] = []

    def __str__(self) -> str:

        return f"🧭 ID: {self.id} Headsign: {self.headsign}"

    def assign_route(self, route: Route) -> None:

        self.route = route

    def assign_service(self, service: Service) -> None:

        self.service = service

    def assign_shape(self, shape: Shape) -> None:

        self.shape = shape

    def add_stop_time(self, stop_time: StopTime) -> None:

        self.stop_times.append(stop_time)


class StopTime:

    def __init__(self, data_row: object) -> None:

        self.trip_id: str = str(data_row['trip_id'])

        # TODO: Figure out way to handle 24:00:00+ time...
        #time_format = "%H:%M:%S"
        #self.arrival_time: datetime._time = datetime.datetime.strptime(str(data_row['arrival_time']), time_format).time()
        #self.departure_time: datetime._time = datetime.datetime.strptime(str(data_row['departure_time']), time_format).time()

        self.arrival_time: str = str(data_row['arrival_time'])
        self.departure_time: str = str(data_row['departure_time'])

        self.stop_id: str = str(data_row['stop_id'])
        self.stop_sequence: int = int(data_row['stop_sequence'])
        self.stop_headsign: str = str(data_row['stop_headsign'])
        self.pickup_type: int = int(data_row['pickup_type'])
        self.drop_off_type: int = int(data_row['drop_off_type'])
        self.shape_dist_traveled: float = float(
            data_row['shape_dist_traveled'])

        self.stop: Stop = None
        self.trip: Trip = None

    def __str__(self) -> str:

        return f"⌛: Route: {self.trip.route.id} Stop: {self.stop.name}: Arrival: {self.arrival_time} Departure: {self.departure_time}"

    def assign_stop(self, stop: Stop):

        self.stop = stop

    def assign_trip(self, trip: Trip):

        self.trip = trip


def generate_transfers(transfers_df: pd.DataFrame):

    def transfer(stop_from: Stop, stop_to: Stop) -> tuple[int, int]:

        from_df = transfers_df[transfers_df['from_stop_id'] == stop_from.id]

        if len(from_df) <= 0:
            return (None, None)

        to_df = from_df[from_df['to_stop_id'] == stop_to.id]

        if len(to_df) <= 0:
            return (None, None)

        return (int(to_df['min_transfer_time']), int(to_df['transfer_type']))

    return transfer
