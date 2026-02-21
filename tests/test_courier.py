import allure
from api_methods import Courier
from data import TestMessages, EXCLUDE_PARAMETERS, CHANGE_PARAMETERS




class TestCreateCourier:

    @allure.title('Создание курьера')
    def test_create_courier_successful_creation(self, random_courier_data):
        response = Courier.register_courier(random_courier_data)
        assert response.status_code == TestMessages.COURIER_SUCCESSFUL_CREATION["code"]
        assert response.json()["ok"] == TestMessages.COURIER_SUCCESSFUL_CREATION["message"]


    @allure.title('Нельзя создать двух одинаковых курьеров')
    def test_create_two_identical_couriers_courier_not_created(self, random_courier_data):
        Courier.register_courier(random_courier_data)
        response = Courier.register_courier(random_courier_data)
        assert response.status_code == TestMessages.COURIER_LOGIN_ALREADY_IN_USE["code"]
        assert response.json()["message"] == TestMessages.COURIER_LOGIN_ALREADY_IN_USE["message"]


    @allure.title('Регистрация курьера - json не содержит поля - login')
    def test_create_courier_without_login_field_not_created(self, random_courier_data):
        payload = Courier.excludes_parameter_from_courier_registration_data(random_courier_data,
                                                                            exclude=EXCLUDE_PARAMETERS["login"])
        response = Courier.register_courier(payload)
        assert response.status_code == TestMessages.COURIER_NOT_ENOUGH_REGISTER_DATA["code"]
        assert response.json()["message"] == TestMessages.COURIER_NOT_ENOUGH_REGISTER_DATA["message"]


    @allure.title('Регистрация курьера - json не содержит поля - password')
    def test_create_courier_without_password_field_not_created(self, random_courier_data):
        payload = Courier.excludes_parameter_from_courier_registration_data(random_courier_data,
                                                                            exclude=EXCLUDE_PARAMETERS["password"])
        response = Courier.register_courier(payload)
        assert response.status_code == TestMessages.COURIER_NOT_ENOUGH_REGISTER_DATA["code"]
        assert response.json()["message"] == TestMessages.COURIER_NOT_ENOUGH_REGISTER_DATA["message"]


    @allure.title('Регистрация курьера - json не содержит поля - firstName')
    def test_create_courier_without_firstname_field_successful_created(self, random_courier_data):
        payload = Courier.excludes_parameter_from_courier_registration_data(random_courier_data,
                                                                            exclude=EXCLUDE_PARAMETERS["firstName"])
        response = Courier.register_courier(payload)
        assert response.status_code == TestMessages.COURIER_SUCCESSFUL_CREATION["code"]
        assert response.json()["ok"] == TestMessages.COURIER_SUCCESSFUL_CREATION["message"]


class TestLoginCourier:

    @allure.title('Авторизация курьера')
    def test_login_courier_successful_authorized(self, random_courier_data):
        Courier.register_courier(random_courier_data)
        response = Courier.login_courier(random_courier_data)
        assert response.status_code == TestMessages.COURIER_SUCCESSFUL_AUTHORIZATION["code"]
        response_data = response.json()
        assert "id" in response_data
        assert isinstance(response_data["id"], int)
        assert response_data["id"] > 0


    @allure.title('Авторизация курьера - json не содержит поля - логин')
    def test_login_courier_without_login_not_authorized(self, random_courier_data):
        Courier.register_courier(random_courier_data)
        payload = Courier.excludes_parameter_from_courier_registration_data(random_courier_data,
                                                                            exclude=EXCLUDE_PARAMETERS["login"])
        response = Courier.login_courier(payload)
        assert response.status_code == TestMessages.COURIER_NOT_ENOUGH_AUTHORIZATION_DATA["code"]
        assert response.json()["message"] == TestMessages.COURIER_NOT_ENOUGH_AUTHORIZATION_DATA["message"]


    @allure.title('Авторизация курьера - json не содержит поля - password')
    def test_login_courier_without_password_not_authorized(self, random_courier_data):
        Courier.register_courier(random_courier_data)
        payload = Courier.excludes_parameter_from_courier_registration_data(random_courier_data,
                                                                            exclude=EXCLUDE_PARAMETERS["password"])
        response = Courier.login_courier(payload)
        assert response.status_code == TestMessages.COURIER_NOT_ENOUGH_AUTHORIZATION_DATA["code"]
        assert response.json()["message"] == TestMessages.COURIER_NOT_ENOUGH_AUTHORIZATION_DATA["message"]


    @allure.title('Авторизация курьера если неправильно указать логин')
    def test_courier_with_non_existent_login_not_authorized(self, random_courier_data):
        Courier.register_courier(random_courier_data)
        payload = Courier.change_parameter_value_in_courier_registration_data(random_courier_data,
                                                                              change=CHANGE_PARAMETERS["login"])
        response = Courier.login_courier(payload)
        assert response.status_code == TestMessages.COURIER_ACCOUNT_NOT_FOUND["code"]
        assert response.json()["message"] == TestMessages.COURIER_ACCOUNT_NOT_FOUND["message"]


    @allure.title('Авторизация курьера если неправильно указать пароль')
    def test_courier_with_non_existent_password_not_authorized(self, random_courier_data):
        Courier.register_courier(random_courier_data)
        payload = Courier.change_parameter_value_in_courier_registration_data(random_courier_data,
                                                                              change=CHANGE_PARAMETERS["password"])
        response = Courier.login_courier(payload)
        assert response.status_code == TestMessages.COURIER_ACCOUNT_NOT_FOUND["code"]
        assert response.json()["message"] == TestMessages.COURIER_ACCOUNT_NOT_FOUND["message"]