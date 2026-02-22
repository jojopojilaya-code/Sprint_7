import allure
import random
import string
from faker import Faker
from api_methods import Courier, Order
from data import color_selection


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
            'login': login,
            'password': password,
            'firstName': first_name,
        }
        return payload


    @staticmethod
    def generate_random_order_data():
        faker = Faker(locale='ru_RU')
        order_data = {
            'firstName': Generator.generate_random_russian_string(10),
            'lastName': Generator.generate_random_russian_string(15),
            'address': Generator.generate_random_russian_string(20),
            'metroStation': faker.random_int(min=1, max=10, step=1),
            'phone': f"8{Generator.generate_random_numbers_as_string(10)}",
            'rentTime': faker.random_int(min=1, max=6, step=1),
            'deliveryDate': faker.date_between(start_date='+1d', end_date='+5d').isoformat(),
            'comment': Generator.generate_random_russian_string(5),
            'color': random.choice(color_selection),
        }
        return order_data