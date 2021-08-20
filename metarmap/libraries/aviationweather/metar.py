import datetime

try:
    from typing import Any, List, TypedDict
except ImportError:
    # TypedDict was not introduced until 3.8
    # use typing_extensions to support python 3.7
    from typing import Any, List
    from typing_extensions import TypedDict

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

        def safe_child(parent: object, child: str, default: Any = None) -> object:
            """ Return parent.child, or None if parent.child is not set """
            try:
                return getattr(parent, child)
            except AttributeError:
                return default

        for station in root.data.getchildren():
            station_dict = {
                'raw_text':         str(safe_child(station, 'raw_text', '')),
                'station_id':       str(safe_child(station, 'station_id', '')),
                'observation_time': datetime.datetime.fromisoformat(
                    str(safe_child(station, 'observation_time', '00000000')).replace('Z', '+00:00')
                ),
                'latitude':         float(safe_child(station, 'latitude', None)),
                'longitude':        float(safe_child(station, 'longitude', None)),
                'temp':             float(safe_child(station, 'temp_c', None)),
                'dewpoint':         float(safe_child(station, 'dewpoint_c', None)),
                'wind_direction':   int(safe_child(station, 'wind_dir_degrees', None)),
                'wind_speed':       int(safe_child(station, 'wind_speed_kt', None)),
                'visibility':       float(safe_child(station, 'visibility_statute_mi', None)),
                'altimeter':        float(safe_child(station, 'altim_in_hg', None)),
                'weather':          str(safe_child(station, 'wx_string', '')),
                'sky_condition':    [],
                'flight_category':  str(safe_child(station, 'flight_category', '')),
                'metar_type':       str(safe_child(station, 'metar_type', '')),
            }
            sky_condition = []
            sky_condition_data = safe_child(station, 'sky_condition', None)
            if sky_condition_data:
                for condition in sky_condition_data:
                    sky_condition.append({
                        'sky_cover': condition.attrib.get('sky_cover', ''),
                        'cloud_base': condition.attrib.get('cloud_base_ft_agl', None),
                    })
            station_dict['sky_condition'] = sky_condition
            results.append(station_dict)
    return results
