import pytest
from helper import Generator
from api_methods import Courier, Order
import copy




@pytest.fixture()
def random_courier_data():
    random_courier_data = Generator.generate_payload()
    random_courier_data_copy = copy.deepcopy(random_courier_data)
    yield random_courier_data
    Courier.delete_courier(random_courier_data_copy)


@pytest.fixture()
def random_order_data():
    random_order_data = Generator.generate_random_order_data()
    yield random_order_data
    Order.delete_order_after_test(random_order_data)
