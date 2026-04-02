
from httpx import AsyncClient, Response

from app.users.models import UserRoleEnum


login_data = {
    "username":"usernametest",
    "password":"testpassword123"
}

# ==================================================================================== #
#                  LOGIN
# ==================================================================================== #

async def test_login_user_success(client: AsyncClient, create_user_response: Response):

    assert create_user_response.status_code == 201

    # login:
    response = await client.post(url="/login", data=login_data)

    assert response.status_code == 200
    assert "\"token_type\":\"Bearer\"" in response.text
    assert "access_token" in response.text




async def test_login_user_fail_bad_username(client: AsyncClient, create_user_response: Response):

    assert create_user_response.status_code == 201

    login_data_bad_username = {**login_data, "username":"bad"}

    # login:
    response = await client.post(url="/login", data=login_data_bad_username)

    assert response.status_code == 401
    assert "Invalid JWT Credentials" in response.text




async def test_login_user_fail_bad_password(client: AsyncClient, create_user_response: Response):

    assert create_user_response.status_code == 201

    login_data_bad_password = {**login_data, "password":"bad"}

    # login:
    response = await client.post(url="/login", data=login_data_bad_password)

    assert response.status_code == 401
    assert "Invalid JWT Credentials" in response.text

