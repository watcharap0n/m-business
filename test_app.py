from fastapi.testclient import TestClient
from app import app
from test_modules.api_setting import TestAPP

client = TestClient(app)

id_query_customer = '/60e566c51e2a43c3bb7d93eb'
id_query_import = '/60ef28f2976caa3fa14f2512'


def test_post_customer_success():
    test = TestAPP(api='/api/customer')
    response = client.post(
        test.api_include(),
        json=test.data
    )
    res_data = test.response_json(response.json())
    assert response.status_code == 201
    assert res_data == test.data


def test_put_customer_success():
    test = TestAPP(api='/api/customer')
    response = client.put(
        test.api_include(id_query_customer),
        json=test.query_data(name='weeraborirak', email='wera.watchrapon@gmail.com')
    )
    assert response.status_code == 200
    assert response.json() == {'message': 'success'}


def test_delete_customer_success():
    test = TestAPP(api='/api/customer')
    response = client.delete(
        test.api_include(id_query_customer)
    )
    assert response.status_code == 204
    assert response.json() == {'message': 'success'}


def test_post_import_success():
    test = TestAPP(api='/api/import')
    response = client.post(
        test.api_include(),
        json=test.data
    )
    res_data = test.response_json(response.json())
    assert response.status_code == 201
    assert res_data == test.data


def test_put_import_success():
    test = TestAPP(api='/api/import')
    response = client.put(
        test.api_include(id_query_import),
        json=test.query_data(name='weeraborirak', email='wera.watchrapon@gmail.com')
    )
    assert response.status_code == 200
    assert response.json() == {'message': 'success'}


def test_delete_import_success():
    test = TestAPP(api='/api/import')
    response = client.delete(test.api_include(id_query_import))
    assert response.status_code == 204
    assert response.json() == {'message': 'success'}


def test_login():
    test = TestAPP(api='/secure/login')
    response = client.post(
        test.api_include(),
        json=test.data_login
    )
    assert response.status_code == 200