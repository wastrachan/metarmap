import datetime
from typing import List, TypedDict

from lxml import objectify

from .client import AviationWeatherClient


class MetarDict(TypedDict):
    raw_text: str
    station_id: str
    observation_time: datetime.datetime
    latitude: float
    longitude: float
    temp: float
    dewpoint: float
    wind_direction: int
    wind_speed: int
    visibility: float
    altimeter: float
    weather: str
    sky_condition: List[
        TypedDict(
            'SkyConditionDict',
            {
                'sky_cover': str,
                'cloud_base': str,
            })
        ]
    flight_category: str
    metar_type: str


def retrieve(stations: List, hours_before: int = 2, most_recent: bool = True) -> List[MetarDict]:
    """ Retrieve METAR from Aviationweather.gov for station(s)

    Args:
        stations (list): list of one or more stations
            (four character alphanumeric string, e.x. KRYY)
        hours_before (int): number of hours before current time to query for
        most_recent (bool): get the single most recent METAR
            (per station) for the specified time range

    Returns:
        List of METAR objects
    """
    stations = '%20'.join(stations)
    query_path = (
        f'?dataSource=metars'
        f'&requestType=retrieve'
        f'&format=xml'
        f'&stationString={stations}'
        f'&hoursBeforeNow={hours_before}'
        f'&mostRecentForEachStation={"true" if most_recent else "false"}'
    )
    client = AviationWeatherClient()
    response = client.get(query_path)
    root = objectify.fromstring(bytes(response.text, 'utf-8'))
    num_results = root.data.attrib.get('num_results', 0)
    results = []
    if num_results:
        for station in root.data.getchildren():
            station_dict = {
                'raw_text': str(station.raw_text),
                'station_id': str(station.station_id),
                'observation_time': datetime.datetime.fromisoformat(str(station.observation_time).replace('Z', '+00:00')),
                'latitude': float(station.latitude),
                'longitude': float(station.longitude),
                'temp': float(station.temp_c),
                'dewpoint': float(station.dewpoint_c),
                'wind_direction': int(station.wind_dir_degrees),
                'wind_speed': int(station.wind_speed_kt),
                'visibility': float(station.visibility_statute_mi),
                'altimeter': float(station.altim_in_hg),
                'weather': str(station.wx_string),
                'sky_condition': [],
                'flight_category': str(station.flight_category),
                'metar_type': str(station.metar_type),
            }
            sky_condition = []
            for condition in station.sky_condition:
                sky_condition.append({
                    'sky_cover': condition.attrib.get('sky_cover', ''),
                    'cloud_base': condition.attrib.get('cloud_base_ft_agl', None),
                })
            station_dict['sky_condition'] = sky_condition
            results.append(station_dict)
    return results
