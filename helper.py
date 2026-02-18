import copy

import requests
import allure
import random
import string
from urls import Urls
from faker import Faker
from data import color_selection, TestMessages, EXCLUDE_PARAMETERS




class Generator:

    @staticmethod
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for _ in range(length))
        return random_string


    @staticmethod
    def generate_random_russian_string(length):
        letters = [chr(i) for i in range(1072, 1105)]
        random_string = ''.join(random.choice(letters) for _ in range(length))
        return random_string


    @staticmethod
    def generate_random_numbers_as_string(length):
        numbers = '0123456789'
        random_numbers = ''.join(random.choice(numbers) for _ in range(length))
        return random_numbers


    @staticmethod
    def generate_payload():
        login = Generator.generate_random_string(10)
        password = Generator.generate_random_numbers_as_string(4)
        first_name = Generator.generate_random_string(10)
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        return payload


    @staticmethod
    def generate_random_order_data():
        faker = Faker(locale="ru_RU")
        order_data = {
            "firstName": Generator.generate_random_russian_string(10),
            "lastName": Generator.generate_random_russian_string(15),
            "address": Generator.generate_random_russian_string(20),
            "metroStation": faker.random_int(min=1, max=10, step=1),
            "phone": f"8{Generator.generate_random_numbers_as_string(10)}",
            "rentTime": faker.random_int(min=1, max=6, step=1),
            "deliveryDate": faker.date_between(start_date='+1d', end_date='+5d').isoformat(),
            "comment": Generator.generate_random_russian_string(5),
            "color": random.choice(color_selection)
        }
        return order_data


class Courier:

    @staticmethod
    @allure.step('Регистрация курьера')
    def register_courier(courier_data):
        response = requests.post(url=Urls.CREATE_COURIER, json=courier_data)
        return response


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
        del registered_courier_data[EXCLUDE_PARAMETERS["firstName"]]
        response = requests.post(url=Urls.LOGIN_COURIER, json=registered_courier_data)
        return response


    @staticmethod
    @allure.step('Удаление курьера')
    def delete_courier(registered_courier_data):
        response = Courier.login_courier(registered_courier_data)
        if response.status_code == TestMessages.COURIER_SUCCESSFUL_AUTHORIZATION["code"]:
            courier_id = response.json()["id"]
            requests.delete(f"{Urls.DELETE_COURIER}{courier_id}")


class Order:

    @staticmethod
    @allure.step('Создать заказ')
    def create_order(order_data):
        response = requests.post(url=Urls.CREATE_ORDER, json=order_data)
        if response.status_code == TestMessages.ORDER_SUCCESSFUL_CREATION["code"]:
            order_data["delete"] = response.json()["track"]
        return response


    @staticmethod
    def delete_order_after_test(order_data):
        track = order_data["delete"]
        requests.put(url=Urls.CANCEL_ORDER, json={
            "track": track
        })


    @staticmethod
    @allure.step('Получить список заказов')
    def get_list_of_orders():
        return requests.get(url=Urls.GET_LIST_OF_ORDERS)




