from httpx import AsyncClient


# ==================================================================================== #
#                  CREATE USER
# ==================================================================================== #

async def test_create_normal_user_success(client: AsyncClient):

    data =  {
    "username":"usernametest",
    "password":"testpassword123",
    "email":"test@test.com",
    "phone_number":"123456789",
    "birth":"2000-02-02",
} 

    response = await client.post(url="/users/", json=data)

    print(response.text)

    assert response.status_code == 201
