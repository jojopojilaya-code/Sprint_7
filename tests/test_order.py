import allure
import pytest
from data import color_selection, TestMessages
from api_methods import Order




class TestCreateOrder:

    @allure.title('Создание заказа')
    @pytest.mark.parametrize('color', color_selection)
    def test_create_order_successful_creation(self, random_order_data, color):
        random_order_data["color"] = color
        response = Order.create_order(random_order_data)
        assert response.status_code == TestMessages.ORDER_SUCCESSFUL_CREATION["code"]
        response_data = response.json()
        assert "track" in response_data
        assert isinstance(response_data["track"], str)


class TestListOfOrders:

    @allure.title('Получение списка заказов')
    def test_get_list_of_orders_successful(self):
        response = Order.get_list_of_orders()
        assert response.status_code == TestMessages.ORDER_GET_LIST_OF_ORDERS["code"]
        response_data = response.json()
        assert "orders" in response_data
        assert isinstance(response_data["orders"], list)
        if response_data["orders"]:
            assert isinstance(response_data["orders"][0], dict)