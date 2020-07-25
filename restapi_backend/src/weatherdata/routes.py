from http import HTTPStatus

from flask import request, jsonify, current_app, Blueprint
import pandas as pd

from ..extensions import db
from ..exceptions import APIError
from ..utils import Role, with_rollback_and_raise_exception
from .models import WeatherDataset, WindSensorData, TempHumiditySensorData
from .schemas import get_weatherdata_payload_schema, weather_dataset_schema
from ..utils import access_level_required, json_with_rollback_and_raise_exception

weatherdata_blueprint = Blueprint('data', __name__, url_prefix='/api/v1/data')


@weatherdata_blueprint.route('', methods=['PUT'])
@access_level_required(Role.PUSH_USER)
@json_with_rollback_and_raise_exception
def add_or_update_weather_datasets():
    new_datasets = weather_dataset_schema.load(request.json)

    num_datasets_before_commit = WeatherDataset.query.count()
    db.session.add_all(new_datasets)
    db.session.commit()
    num_datasets_after_commit = WeatherDataset.query.count()
    num_new_datasets = num_datasets_after_commit - num_datasets_before_commit

    response = jsonify(new_datasets)
    current_app.logger.info('Committed {} datasets to the database, this are {} new entries'
                            .format(len(new_datasets), num_new_datasets))

    if num_new_datasets > 0:
        response.status_code = HTTPStatus.CREATED
    else:
        response.status_code = HTTPStatus.OK

    return response


@weatherdata_blueprint.route('', methods=['GET'])
@json_with_rollback_and_raise_exception
def get_weather_datasets():
    time_period = get_weatherdata_payload_schema.load(request.json)
    first = time_period["first_timepoint"]
    last = time_period["last_timepoint"]
    requested_sensors = time_period["sensors"]  # TODO: validation using marshmallow-enum ...

    requested_base_station_sensors, requested_entities, requested_temp_humidity_sensors, requested_wind_sensors = \
        _create_query_configuration(requested_sensors)

    if last < first:
        raise APIError('Last time \'{}\' is later than first time \'{}\''.format(last, first),
                       status_code=HTTPStatus.BAD_REQUEST)

    found_datasets = pd.read_sql(db.session.query(WeatherDataset)
                                 .filter(WeatherDataset.timepoint >= first)
                                 .filter(WeatherDataset.timepoint <= last)
                                 .join(WeatherDataset.wind)
                                 .join(WeatherDataset.temperature_humidity)
                                 .order_by(WeatherDataset.timepoint).with_entities(WeatherDataset.timepoint,
                                                                                   WeatherDataset.station_id,
                                                                                   TempHumiditySensorData.sensor_id,
                                                                                   *requested_entities)
                                 .statement,
                                 db.session.bind)

    if found_datasets.empty:
        return jsonify({}), HTTPStatus.OK

    found_datasets_per_station = _create_get_response_payload(found_datasets, requested_base_station_sensors,
                                                              requested_temp_humidity_sensors, requested_wind_sensors)

    response = jsonify(found_datasets_per_station)
    response.status_code = HTTPStatus.OK
    current_app.logger.info('Returned {} datasets from \'{}\'-\'{}\''.format(len(found_datasets), first, last))

    return response


def _create_get_response_payload(found_datasets, requested_base_station_sensors, requested_temp_humidity_sensors,
                                 requested_wind_sensors):
    combi_sensor_ids = found_datasets.sensor_id.unique()

    found_datasets_per_station = {}
    station_ids = found_datasets['station_id'].unique()
    for station_id in station_ids:
        station_datasets = found_datasets.loc[(found_datasets.station_id == station_id) &
                                              (found_datasets.sensor_id == "IN")]

        found_datasets_per_station[station_id] = \
            station_datasets.loc[:, requested_base_station_sensors].to_dict("list")
        found_datasets_per_station[station_id]["wind"] = \
            station_datasets.loc[:, requested_wind_sensors].to_dict("list")
        found_datasets_per_station[station_id]["temperature_humidity"] = {}
        for combi_sensor_id in combi_sensor_ids:
            found_datasets_per_station[station_id]["temperature_humidity"][combi_sensor_id] = \
                found_datasets.loc[(found_datasets.station_id == station_id) &
                                   (found_datasets.sensor_id == combi_sensor_id), requested_temp_humidity_sensors]\
                    .to_dict("list")
    return found_datasets_per_station


def _create_query_configuration(requested_sensors):
    do_configure_all = (len(requested_sensors) == 0)
    requested_base_station_sensors, requested_entities = _create_base_station_query_configuration(requested_sensors,
                                                                                                  do_configure_all)
    requested_wind_sensors = _create_wind_sensor_query_configuration(requested_entities, requested_sensors,
                                                                     do_configure_all)
    requested_temp_humidity_sensors = _create_temp_humidity_sensor_query_configuration(requested_entities,
                                                                                       requested_sensors,
                                                                                       do_configure_all)

    return requested_base_station_sensors, requested_entities, requested_temp_humidity_sensors, requested_wind_sensors


def _create_temp_humidity_sensor_query_configuration(requested_entities, requested_sensors, do_configure_all):
    requested_entities.extend([TempHumiditySensorData.temperature, TempHumiditySensorData.humidity])
    requested_temp_humidity_sensors = ["temperature", "humidity"]

    if not do_configure_all:
        if "temperature" not in requested_sensors:
            requested_temp_humidity_sensors.remove("temperature")
            requested_entities.remove(TempHumiditySensorData.temperature)
        if "humidity" not in requested_sensors:
            requested_temp_humidity_sensors.remove("humidity")
            requested_entities.remove(TempHumiditySensorData.humidity)

    return requested_temp_humidity_sensors


def _create_wind_sensor_query_configuration(requested_entities, requested_sensors, do_configure_all):
    requested_entities.extend(
        [WindSensorData.gusts, WindSensorData.direction, WindSensorData.wind_temperature, WindSensorData.speed])
    requested_wind_sensors = ["gusts", "direction", "wind_temperature", "speed"]

    if not do_configure_all:
        if "gusts" not in requested_sensors:
            requested_wind_sensors.remove("gusts")
            requested_entities.remove(WindSensorData.gusts)
        if "direction" not in requested_sensors:
            requested_wind_sensors.remove("direction")
            requested_entities.remove(WindSensorData.direction)
        if "wind_temperature" not in requested_sensors:
            requested_wind_sensors.remove("wind_temperature")
            requested_entities.remove(WindSensorData.wind_temperature)
        if "speed" not in requested_sensors:
            requested_wind_sensors.remove("speed")
            requested_entities.remove(WindSensorData.speed)

    return requested_wind_sensors


def _create_base_station_query_configuration(requested_sensors, do_configure_all):
    requested_entities = [WeatherDataset.pressure, WeatherDataset.uv, WeatherDataset.rain_counter]
    requested_base_station_sensors = ["timepoint", "pressure", "uv", "rain_counter"]

    if not do_configure_all:
        if "pressure" not in requested_sensors:
            requested_base_station_sensors.remove("pressure")
            requested_entities.remove(WeatherDataset.pressure)
        if "uv" not in requested_sensors:
            requested_base_station_sensors.remove("uv")
            requested_entities.remove(WeatherDataset.uv)
        if "rain_counter" not in requested_sensors:
            requested_base_station_sensors.remove("rain_counter")
            requested_entities.remove(WeatherDataset.rain_counter)

    return requested_base_station_sensors, requested_entities


@weatherdata_blueprint.route('/<id>', methods=['DELETE'])
@access_level_required(Role.PUSH_USER)
@with_rollback_and_raise_exception
def delete_weather_dataset(id):
    existing_dataset = WeatherDataset.query.get(id)
    if not existing_dataset:
        current_app.logger.info('Nothing to delete for dataset with id \'{}\' '.format(id))
        return '', HTTPStatus.NO_CONTENT

    db.session.delete(existing_dataset)
    db.session.commit()
    current_app.logger.info('Deleted dataset for time \'{}\' from the database'.format(existing_dataset.timepoint))

    response = jsonify(existing_dataset)
    response.status_code = HTTPStatus.OK

    return response


@weatherdata_blueprint.route('/<id>', methods=['GET'])
@with_rollback_and_raise_exception
def get_one_weather_dataset(id):
    dataset = WeatherDataset.query.get(id)
    if not dataset:
        raise APIError('No dataset with id \'{}\''.format(id), status_code=HTTPStatus.BAD_REQUEST)

    response = jsonify(dataset)
    response.status_code = HTTPStatus.OK
    current_app.logger.info('Returned dataset for id \'{}\''.format(id))

    return response


@weatherdata_blueprint.route('/limits', methods=['GET'])
@with_rollback_and_raise_exception
def get_available_time_period():
    min_max_query_result = db.session.query(db.func.min(WeatherDataset.timepoint).label("min_time"),
                                            db.func.max(WeatherDataset.timepoint).label("max_time")).one()
    first_timepoint = min_max_query_result.min_time
    last_timepoint = min_max_query_result.max_time

    if not first_timepoint or not last_timepoint:
        raise APIError('No data in the database', status_code=HTTPStatus.NOT_FOUND)

    time_range = {
        "first_timepoint": first_timepoint,
        "last_timepoint": last_timepoint
    }

    response = jsonify(time_range)
    response.status_code = HTTPStatus.OK
    current_app.logger.info('Returned available time period: \'{}\'-\'{}\''.format(time_range["first_timepoint"],
                                                                                   time_range["last_timepoint"]))

    return response
