from http import HTTPStatus

from flask import request, jsonify, current_app, Blueprint

from ..extensions import db
from ..exceptions import APIError
from ..utils import Role, with_rollback_and_raise_exception
from .models import BaseStationData, TimeRange, WeatherRawDataset, WindSensorData, CombiSensorData, \
    RainSensorData, WindSensorRawData, CombiSensorRawData
from ..utils import access_level_required, json_with_rollback_and_raise_exception, to_utc

weatherdata_blueprint = Blueprint('data', __name__, url_prefix='/api/v1/data')


@weatherdata_blueprint.route('', methods=['POST'])
@access_level_required(Role.PUSH_USER)
@json_with_rollback_and_raise_exception
def add_weather_dataset():
    new_dataset = _create_weather_dataset()

    existing_dataset = BaseStationData.query.filter_by(timepoint=new_dataset.timepoint).first()
    if not existing_dataset:
        db.session.add(new_dataset)
        db.session.commit()

        response = jsonify(new_dataset)
        current_app.logger.info('Added new dataset for time \'{}\' to the database'.format(new_dataset.timepoint))
        response.status_code = HTTPStatus.CREATED
    else:
        raise APIError('Dataset for time \'{}\' already in the database'.format(new_dataset.timepoint),
                       status_code=HTTPStatus.CONFLICT, location='/api/v1/data/{}'.format(existing_dataset.dataset_id))

    response.headers['location'] = '/api/v1/data/{}'.format(new_dataset.dataset_id)

    return response


def _create_weather_dataset():
    new_dataset = WeatherRawDataset.from_dict(request.json)

    all_combi_sensor_data = []
    for combi_sensor_data in new_dataset.temperature_humidity:
        all_combi_sensor_data.append(CombiSensorData(**combi_sensor_data.to_dict()))
    wind_sensor_data = WindSensorData(**new_dataset.wind.to_dict())
    rain_sensor_data = RainSensorData(rain_counter_in_mm=new_dataset.rain_counter)
    weather_dataset = BaseStationData(
        timepoint=new_dataset.timepoint,
        station_id=new_dataset.station,
        pressure=new_dataset.pressure,
        uv=new_dataset.uv,
        rain_sensor_data=rain_sensor_data,
        wind_sensor_data=wind_sensor_data,
        combi_sensor_data=all_combi_sensor_data
    )

    return weather_dataset


@weatherdata_blueprint.route('', methods=['GET'])
@json_with_rollback_and_raise_exception
def get_weather_datasets():
    time_period = TimeRange.from_dict(request.json)
    first = time_period.first_timepoint
    last = time_period.last_timepoint
    if last < first:
        raise APIError('Last time \'{}\' is later than first time \'{}\''.format(last, first),
                       status_code=HTTPStatus.BAD_REQUEST)

    base_datasets = (BaseStationData.query
                     .filter(BaseStationData.timepoint >= first)
                     .filter(BaseStationData.timepoint <= last)
                     .order_by(BaseStationData.timepoint)
                     .all())

    if not base_datasets:
        return jsonify({}), HTTPStatus.OK

    matching_datasets = _create_raw_datasets(base_datasets)
    response = jsonify(matching_datasets)
    response.status_code = HTTPStatus.OK
    current_app.logger.info('Returned {} datasets from \'{}\'-\'{}\''.format(len(matching_datasets), first, last))

    return response


def _create_raw_datasets(base_datasets):
    matching_datasets = []
    for dataset in base_datasets:
        raw_dataset = WeatherRawDataset(
            timepoint=dataset.timepoint,
            station=dataset.station_id,
            pressure=dataset.pressure,
            uv=dataset.uv,
            rain_counter=dataset.rain_sensor_data.rain_counter_in_mm,
            wind=WindSensorRawData(
                direction=dataset.wind_sensor_data.direction,
                speed=dataset.wind_sensor_data.speed,
                temperature=dataset.wind_sensor_data.temperature,
                gusts=dataset.wind_sensor_data.gusts
            ),
            temperature_humidity=[]
        )

        for temp_humidity_dataset in dataset.combi_sensor_data:
            raw_dataset.temperature_humidity.append(CombiSensorRawData(
                sensor_id=temp_humidity_dataset.sensor_id,
                temperature=temp_humidity_dataset.temperature,
                humidity=temp_humidity_dataset.humidity
            ))

        matching_datasets.append(raw_dataset)

    return matching_datasets


@weatherdata_blueprint.route('/<id>', methods=['PUT'])
@access_level_required(Role.PUSH_USER)
@json_with_rollback_and_raise_exception
def update_weather_dataset(id):
    json = request.json
    if not json:
        raise APIError('Required Content-Type is `application/json`', status_code=HTTPStatus.BAD_REQUEST)

    new_dataset = BaseStationData(**json)
    existing_dataset = BaseStationData.query.get(id)
    if not existing_dataset:
        raise APIError('No dataset with id \'{}\''.format(id), status_code=HTTPStatus.NOT_FOUND)

    if to_utc(new_dataset.timepoint) != to_utc(existing_dataset.timepoint):
        raise APIError('The time \'{}\' stored for id \'{}\' does not match the time \'{}\' of the submitted '
                       'dataset'.format(existing_dataset.timepoint, id, new_dataset.timepoint),
                       status_code=HTTPStatus.CONFLICT,
                       location='/api/v1/data/{}'.format(existing_dataset.dataset_id))

    existing_dataset.temp = new_dataset.temp
    existing_dataset.humidity = new_dataset.humidity
    db.session.commit()
    current_app.logger.info('Updated dataset for time \'{}\' to the database'.format(existing_dataset.timepoint))

    response = jsonify(existing_dataset)
    response.status_code = HTTPStatus.OK
    response.headers['location'] = '/api/v1/data/{}'.format(existing_dataset.dataset_id)

    return response


@weatherdata_blueprint.route('/<id>', methods=['DELETE'])
@access_level_required(Role.PUSH_USER)
@with_rollback_and_raise_exception
def delete_weather_dataset(id):
    existing_dataset = BaseStationData.query.get(id)
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
    dataset = BaseStationData.query.get(id)
    if not dataset:
        raise APIError('No dataset with id \'{}\''.format(id), status_code=HTTPStatus.BAD_REQUEST)

    response = jsonify(dataset)
    response.status_code = HTTPStatus.OK
    current_app.logger.info('Returned dataset for id \'{}\''.format(id))

    return response


@weatherdata_blueprint.route('/limits', methods=['GET'])
@with_rollback_and_raise_exception
def get_available_time_period():
    time_range = TimeRange(
        first_timepoint=db.session.query(BaseStationData.timepoint, db.func.min(BaseStationData.timepoint)).scalar(),
        last_timepoint=db.session.query(BaseStationData.timepoint, db.func.max(BaseStationData.timepoint)).scalar()
    )

    if not time_range.first_timepoint or not time_range.last_timepoint:
        raise APIError('No data in the database', status_code=HTTPStatus.NOT_FOUND)

    response = jsonify(time_range)
    response.status_code = HTTPStatus.OK
    current_app.logger.info('Returned available time period: \'{}\'-\'{}\''.format(time_range.first_timepoint,
                                                                                   time_range.last_timepoint))

    return response
