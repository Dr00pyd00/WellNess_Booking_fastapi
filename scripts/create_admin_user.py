import asyncio



import app.all_models
from app.core.database import LocalSession
from app.core.security.pw_hashing import hash_pw
from app.users.models import User, UserRoleEnum
from app.core.config import app_settings


async def create_admin_user(
        username: str,
        password: str,
        email: str,
)->None:
    
    async with LocalSession() as db:

        try:
            hashed_pw = hash_pw(password)
            admin_user = User(
                username=username,
                password=hashed_pw,
                email=email,
                role=UserRoleEnum.ADMIN,
            )

            db.add(admin_user)
            await db.commit()
            await db.refresh(admin_user)

            print(f"Admin <{username}> Created !")

        except Exception as e:
            await db.rollback()
            print(f"Error to create admin: {e}")




if __name__ == "__main__":
    asyncio.run(
        create_admin_user(
            username=app_settings.admin_username,
            password=app_settings.admin_password,
            email=app_settings.admin_email
        )
    )


