
from httpx import AsyncClient, Response

from app.core.models_mixins.mixin_status import StatusEnum
from app.users.models import UserRoleEnum
from app.users.models import User


# ==================================================================================== #
#                  CREATE USER
# ==================================================================================== #

# global data:
user_data_creation =  {
    "username":"usernametest",
    "password":"testpassword123",
    "email":"test@test.com",
    "phone_number":"123456789",
    "birth":"2000-02-02",
} 

async def test_create_normal_user_success(client: AsyncClient):

    response = await client.post(url="/users/", json=user_data_creation)

    # print(response.json())
    assert response.status_code == 201
    assert response.json()["username"] == "usernametest"
    assert response.json()["email"] == "test@test.com"
    assert response.json()["role"] == UserRoleEnum.PATIENT.value


async def test_create_user_fail_username_taken(client: AsyncClient, create_user_response: Response):

    # 2nd user creation with same name:
    response = await client.post(url="/users/", json=user_data_creation)

    assert create_user_response.status_code == 201
    assert response.status_code == 409
    assert "user already exist" in response.text.lower()
    assert "username" in response.text.lower()


async def test_create_user_fail_email_taken(client: AsyncClient, create_user_response: Response):

    data = {**user_data_creation, "username":"usernametest2"}

    # 2nd user:
    response = await client.post(url="/users/", json=data)

    assert create_user_response.status_code == 201
    assert response.status_code == 409
    assert "user already exist" in response.text.lower()
    assert "email" in response.text.lower()


async def test_create_user_fail_pw_no_digits(client: AsyncClient):

    data = {**user_data_creation, "password":"password"}

    response = await client.post(url="/users/", json=data)

    assert response.status_code == 422
    assert "value_error" in response.text.lower()
    assert "password" in response.text.lower()
    assert "must contain at least one digit" in response.text.lower()


async def test_create_user_fail_pw_no_alpha(client: AsyncClient):

    data = {**user_data_creation, "password":"123456"}

    response = await client.post(url="/users/", json=data)

    assert response.status_code == 422
    assert "value_error" in response.text.lower()
    assert "password" in response.text.lower()
    assert "must contain at least one alpha" in response.text.lower()


async def test_create_user_fail_pw_too_short(client: AsyncClient):

    data = {**user_data_creation, "password":"a2"}

    response = await client.post(url="/users/", json=data)

    assert response.status_code == 422
    assert "string_too_short" in response.text.lower()
    assert "password" in response.text.lower()
    assert "String should have at least 5 characters" in response.text


async def test_create_user_fail_pw_too_long(client: AsyncClient):

    data = {**user_data_creation, 
            "password":"787987EGZEGEGZGEGaB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3aB3"
            }

    response = await client.post(url="/users/", json=data)

    assert response.status_code == 422
    assert "string_too_long" in response.text.lower()
    assert "password" in response.text.lower()
    assert "String should have at most 150 characters" in response.text


async def test_create_user_fail_username_too_short(client: AsyncClient):

    data = {**user_data_creation, "username":"a"}

    response = await client.post(url="/users/", json=data)

    assert response.status_code == 422
    assert "string_too_short" in response.text
    assert "String should have at least 3 characters" in response.text
    assert "username" in response.text
    


async def test_create_user_fail_username_too_long(client: AsyncClient):

    data = {**user_data_creation, 
            "username":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbbccccccccccccccccccccc"
            }

    response = await client.post(url="/users/", json=data)

    assert response.status_code == 422
    assert "string_too_long" in response.text
    assert "String should have at most 50 characters" in response.text
    assert "username" in response.text



async def test_create_user_fail_username_prohibed_chars(client: AsyncClient):

    data = {**user_data_creation, 
            "username":"@@$$+="
            }

    response = await client.post(url="/users/", json=data)

    assert response.status_code == 422
    assert "value_error" in response.text
    assert "must be alphanumeric" in response.text
    assert "username" in response.text




    

async def test_create_user_fail_invalid_email(client: AsyncClient):

    data = {**user_data_creation,
            "email":"bad_email"
            }

    response = await client.post(url="/users/", json=data)

    assert response.status_code == 422
    assert "value_error" in response.text
    assert "value is not a valid email address" in response.text
    assert "bad_email" in response.text



async def test_create_user_fail_birth_in_future(client: AsyncClient):

    data = {**user_data_creation,
            "birth":"2099-02-02"
            }

    response = await client.post(url="/users/", json=data)

    assert response.status_code == 422
    assert "value_error" in response.text
    assert "must be greater than now" in response.text.lower()
    assert "birth" in response.text


async def test_create_user_fail_birth_too_old(client: AsyncClient):

    data = {**user_data_creation,
            "birth":"1900-02-02"
            }

    response = await client.post(url="/users/", json=data)

    assert response.status_code == 422
    assert "value_error" in response.text
    assert "can\'t be greater than 120 years" in response.text.lower()
    assert "birth" in response.text



# ==================================================================================== #
#                  GET ME 
# ==================================================================================== #

async def test_get_me_success(client: AsyncClient, create_user_response: Response, get_created_user_token):

    assert create_user_response.status_code == 201

    token = get_created_user_token

    response = await client.get(url="users/me",
                          headers={
                              "Authorization":f"Bearer {token}"
                          })
    
    assert response.status_code == 200
    assert "\"username\":\"usernametest\"" in response.text


async def test_get_me_admin_success(client: AsyncClient, get_admin_user_token):

    response = await client.get(url="users/me",
                          headers={
                              "Authorization":f"Bearer {get_admin_user_token}"
                          })
    
    assert response.status_code == 200
    assert response.json()["role"] == UserRoleEnum.ADMIN.value




async def test_get_me_fail_bad_token(client: AsyncClient, create_user_response: Response, get_created_user_token):

    assert create_user_response.status_code == 201

    token = "bad_token"

    response = await client.get(url="users/me",
                          headers={
                              "Authorization":f"Bearer {token}"
                          })
    
    assert response.status_code == 401
    assert "Invalid Token Credentials." in response.text




async def test_get_me_fail_no_token(client: AsyncClient, create_user_response: Response, get_created_user_token):

    assert create_user_response.status_code == 201


    response = await client.get(url="users/me")

    assert response.status_code == 401
    assert "Not authenticated" in response.text


# ==================================================================================== #
#                  UPDATE USER PROFILE
# ==================================================================================== #

async def test_update_user_success(client: AsyncClient,create_user_response: Response, get_created_user_token:str ):

    data_to_update = {"username":"UPDATEDusername"}

    response = await client.patch("/users/me", 
                            json=data_to_update, 
                            headers={"Authorization":f"Bearer {get_created_user_token}"
                            })
    
    assert create_user_response.status_code == 201
    assert response.status_code == 200
    assert response.json()["username"] == "UPDATEDusername"
    assert response.json()["id"] == create_user_response.json()["id"]


async def test_update_user_fail_no_token(client: AsyncClient,create_user_response: Response ):

    data_to_update = {"username":"UPDATEDusername"}

    response = await client.patch("/users/me", 
                            json=data_to_update, 
                            )
    
    assert create_user_response.status_code == 201
    assert response.status_code == 401
    assert "Not authenticated" in response.text



# ==================================================================================== #
#                  UPDATE USER PASSWORD
# ==================================================================================== #

async def test_update_user_password_success(client: AsyncClient, create_user_response: Response, get_created_user_token:str):

    assert create_user_response.status_code == 201

    response = await client.patch(url="users/me/password",
                 json={
                     "old_password": user_data_creation["password"],
                     "new_password": "UPDATEDpassword123"
                 },
                 headers={
                     "Authorization":f"Bearer {get_created_user_token}"
                 })
    

    assert response.status_code == 200
    assert response.json()["id"] == create_user_response.json()["id"]



    

async def test_update_user_password_fail_no_token(client: AsyncClient, create_user_response: Response):

    assert create_user_response.status_code == 201

    response = await client.patch(url="users/me/password",
                 json={
                     "old_password": user_data_creation["password"],
                     "new_password": "UPDATEDpassword123"
                 },)
    

    assert response.status_code == 401
    assert "Not authenticated" in response.text


    

# ==================================================================================== #
#                  SOFT DELETE USER
# ==================================================================================== #

async def test_soft_delete_user_success(client: AsyncClient, create_user_response: Response, get_created_user_token:str, get_user_object):

    assert create_user_response.status_code == 201
    assert get_user_object.deleted_at == None

    response = await client.delete(url="users/me",
                                   headers={"Authorization":f"Bearer {get_created_user_token}"}
                                   )
    
    assert response.status_code == 200
    assert response.json()["deleted_at"] != None
    


async def test_soft_delete_user_fail_no_token(client: AsyncClient, create_user_response: Response, get_created_user_token:str, get_user_object):

    assert create_user_response.status_code == 201
    assert get_user_object.deleted_at == None

    response = await client.delete(url="users/me",
                                   )
    
    assert response.status_code == 401
    assert "Not authenticated" in response.text


async def test_soft_delete_fail_last_admin(client: AsyncClient,get_admin_user: User, get_admin_user_token: str):

    assert get_admin_user.role == UserRoleEnum.ADMIN
    assert get_admin_user.deleted_at == None

    response = await client.delete("users/me",
                                   headers={"Authorization":f"Bearer {get_admin_user_token} "})

    assert response.status_code == 403
    assert "can\'t delete last admin" in response.text



# ==================================================================================== #
#                  SWAP ROLE
# ==================================================================================== #

async def test_swap_role_success(client: AsyncClient, get_admin_user_token:str, get_user_object: User):

    assert get_user_object.role == UserRoleEnum.PATIENT # default value

    response = await client.patch(url=f"users/{get_user_object.id}/role",
                                  json={"new_role": str(UserRoleEnum.PRACTITIONER.value)},
                                  headers={"Authorization":f"Bearer {get_admin_user_token}"}
                                    )

    assert response.status_code == 200
    assert response.json()["role"] == UserRoleEnum.PRACTITIONER.value



async def test_swap_role_fail_no_admin(client: AsyncClient, get_created_user_token: str, get_user_object: User):

    assert get_user_object.role == UserRoleEnum.PATIENT # default value

    response = await client.patch(url=f"users/{get_user_object.id}/role",
                                  json={"new_role": str(UserRoleEnum.PRACTITIONER.value)},
                                  headers={"Authorization":f"Bearer {get_created_user_token}"}
                                    )

    assert response.status_code == 401
    assert "don\'t have required role" in response.text



async def test_swap_role_fail_self_admin(client: AsyncClient, get_admin_user_token: str, get_admin_user: User):

    assert get_admin_user.role == UserRoleEnum.ADMIN # default value

    response = await client.patch(url=f"users/{get_admin_user.id}/role",
                                  json={"new_role": str(UserRoleEnum.PRACTITIONER.value)},
                                  headers={"Authorization":f"Bearer {get_admin_user_token}"}
                                    )

    assert response.status_code == 403
    assert "admin can't change his own role" in response.text






# ==================================================================================== #
#                  SWAP STATUS
# ==================================================================================== #

async def test_swap_status_success(client: AsyncClient, get_admin_user_token:str, get_user_object: User):

    assert get_user_object.status == StatusEnum.ACTIVE # default value

    response = await client.patch(url=f"users/{get_user_object.id}/status",
                                  json={"new_status": str(StatusEnum.ARCHIVED.value)},
                                  headers={"Authorization":f"Bearer {get_admin_user_token}"}
                                    )

    assert response.status_code == 200
    assert response.json()["status"] == StatusEnum.ARCHIVED.value



async def test_swap_status_fail_no_admin(client: AsyncClient, get_created_user_token: str, get_user_object: User):

    assert get_user_object.status == StatusEnum.ACTIVE # default value

    response = await client.patch(url=f"users/{get_user_object.id}/status",
                                  json={"new_status": str(StatusEnum.ARCHIVED.value)},
                                  headers={"Authorization":f"Bearer {get_created_user_token}"}
                                    )

    assert response.status_code == 401
    assert "don\'t have required role" in response.text



async def test_swap_status_fail_self_admin(client: AsyncClient, get_admin_user_token: str, get_admin_user: User):

    assert get_admin_user.status == StatusEnum.ACTIVE # default value

    response = await client.patch(url=f"users/{get_admin_user.id}/status",
                                  json={"new_status": str(StatusEnum.ARCHIVED.value)},
                                  headers={"Authorization":f"Bearer {get_admin_user_token}"}
                                    )

    assert response.status_code == 403
    assert "admin can't change his own status" in response.text

