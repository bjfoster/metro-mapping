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

    def __str__(self) -> str:

        return f"ID: {self.id}\nName: {self.name}\nTimezone: {self.timezone}"

    def generate_routes(self, routes_df: pd.DataFrame) -> None:
        
        self.routes: list[Route] = []
        
        for i, row in routes_df.iterrows():
            self.routes.append(Route(row))

    def generate_stops(self, stops_df: pd.DataFrame) -> None:

        self.stops: list[Stop] = []

        for i, row in stops_df.iterrows():
            self.stops.append(Stop(row))

    def generate_services(self, services_df: pd.DataFrame) -> None:

        self.services: list[Service] = []

        for i, row in services_df.iterrows():
            self.services.append(Service(row))

    def generate_shapes(self, shapes_df: pd.DataFrame) -> None:

        self.shapes: list[Shape] = []

        unique_shapes = shapes_df['shape_id'].unique()

        for unique_shape in unique_shapes:

            shape_df = shapes_df[shapes_df['shape_id'] == unique_shape]
            self.shapes.append(Shape(unique_shape, shape_df))

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

                header = "/-/-/🚂/-/-/\n"
                return header + f"ID: {self.id}\nShort Name: {self.short_name}\nLong Name: {self.long_name}"

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
        self.parent_station: str = str(data_row['parent_station'])

    def __str__(self) -> str:

        header = "/-/-/🛑/-/-/\n"
        return header + f"ID: {self.id}\nName: {self.name}"


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
        self.start_date: datetime.datetime = datetime.datetime.strptime(str(data_row['start_date']), date_format)
        self.end_date: datetime.datetime = datetime.datetime.strptime(str(data_row['end_date']), date_format)

    def __str__(self) -> str:

        header = "/-/-/🚦/-/-/\n"
        return header + f"ID: {self.id}"

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

        header = "/-/-/⏹/-/-/\n"
        return header + f"ID: {self.id}"

