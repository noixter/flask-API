import random

from faker import Faker

from app.users.models import User

faker = Faker()


class TestUserRestService:

    ENDPOINT = '/users/'

    def test_endpoint_list_users(
        self,
        client,
        admin_authenticated,
        create_normal_user
    ):
        _, token = admin_authenticated
        response = client.get(
            self.ENDPOINT, headers={'Authorization': 'Bearer {}'.format(token)}
        )
        assert response.status_code == 200
        assert len(response.json.get('users')) > 1
        assert response.json.get('count')

    def test_endpoint_get_a_user(
        self,
        client,
        admin_authenticated,
        create_normal_user
    ):
        _, token = admin_authenticated
        response = client.get(
            f'{self.ENDPOINT}{create_normal_user.id}',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        assert response.status_code == 200
        assert response.json.get('role')
        assert response.json.get('first_name') == create_normal_user.first_name
        assert response.json.get('last_name') == create_normal_user.last_name
        assert response.json.get('email') == create_normal_user.email

    def test_endpoint_create_a_user(
        self,
        client,
        admin_authenticated,
    ):
        _, token = admin_authenticated
        user_data = {
            'first_name': 'test',
            'last_name': 'test',
            'email': faker.email(),
            'password': faker.pystr(),
            'role_id': random.choice([1, 2])
        }
        response = client.post(
            self.ENDPOINT,
            json=user_data,
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        assert response.status_code == 201
        assert response.json.get('first_name') == user_data.get('first_name')
        assert response.json.get('last_name') == user_data.get('last_name')
        assert response.json.get('email') == user_data.get('email')

    def test_endpoint_modify_a_user(
        self,
        client,
        admin_authenticated,
        create_normal_user
    ):
        _, token = admin_authenticated
        modified_data = {
            'email': faker.email()
        }
        response = client.put(
            f'{self.ENDPOINT}{create_normal_user.id}',
            json=modified_data,
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        assert response.status_code == 200
        assert response.json.get('message') == 'updated'
        user = User.query.get(create_normal_user.id)
        assert user.email == modified_data.get('email')

    def test_endpoint_delete_a_user(
        self,
        client,
        admin_authenticated,
        create_normal_user
    ):
        _, token = admin_authenticated
        response = client.delete(
            f'{self.ENDPOINT}{create_normal_user.id}',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        assert response.status_code == 204
        user = User.query.get(create_normal_user.id)
        assert not user

    def test_endpoint_cannot_delete_itself(
        self,
        client,
        user_authenticated
    ):
        user, token = user_authenticated
        response = client.delete(
            f'{self.ENDPOINT}{user.id}',
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        assert response.status_code == 403
        assert response.json.get('message') == 'User cannot perform this operation'

    def test_endpoint_perform_an_unauthorized_action(
        self,
        client,
        user_authenticated
    ):
        user, token = user_authenticated
        response = client.post(
            self.ENDPOINT,
            json={},
            headers={'Authorization': 'Bearer {}'.format(token)}
        )
        assert response.status_code == 403
        assert response.json.get('message') == \
               'user is not allowed to perform this action'
