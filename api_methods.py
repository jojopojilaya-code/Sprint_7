import copy

import allure
import requests

from data import EXCLUDE_PARAMETERS, TestMessages
from urls import Urls


class Courier:

    @staticmethod
    @allure.step('Регистрация курьера')
    def register_courier(courier_data):
        return requests.post(url=Urls.CREATE_COURIER, json=courier_data)

    @staticmethod
    def excludes_parameter_from_courier_registration_data(registered_courier_data, exclude):
        data_copy = copy.deepcopy(registered_courier_data)
        del data_copy[exclude]
        return data_copy

    @staticmethod
    def change_parameter_value_in_courier_registration_data(registered_courier_data, change):
        data_copy = copy.deepcopy(registered_courier_data)
        data_copy[change] = data_copy[change][:-1]
        return data_copy

    @staticmethod
    @allure.step('Авторизация курьера')
    def login_courier(registered_courier_data):
        data = copy.deepcopy(registered_courier_data)
        data.pop(EXCLUDE_PARAMETERS['firstName'], None)
        return requests.post(url=Urls.LOGIN_COURIER, json=data)

    @staticmethod
    @allure.step('Удаление курьера')
    def delete_courier(registered_courier_data):
        response = Courier.login_courier(registered_courier_data)
        if response.status_code == TestMessages.COURIER_SUCCESSFUL_AUTHORIZATION['code']:
            courier_id = response.json()['id']
            requests.delete(f"{Urls.DELETE_COURIER}{courier_id}")


class Order:

    @staticmethod
    @allure.step('Создать заказ')
    def create_order(order_data):
        response = requests.post(url=Urls.CREATE_ORDER, json=order_data)
        if response.status_code == TestMessages.ORDER_SUCCESSFUL_CREATION['code']:
            order_data['delete'] = response.json()['track']
        return response

    @staticmethod
    def delete_order_after_test(order_data):
        track = order_data['delete']
        requests.put(url=Urls.CANCEL_ORDER, json={'track': track})

    @staticmethod
    @allure.step('Получить список заказов')
    def get_list_of_orders():
        return requests.get(url=Urls.GET_LIST_OF_ORDERS)
