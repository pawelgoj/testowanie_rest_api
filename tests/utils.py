import faker
from types import ModuleType


def get_unique_user_email_password(faker: ModuleType, already_created_users: list[dict], max_iterations: int = 20) -> dict:
    """max_iterations - max iterations to find unique data from faker"""
    """email, password"""
    if already_created_users != []:
        for i in range(max_iterations):
            new_user_data = {
                "email": faker.email(),
                "password": faker.password(length=12)
            }
            if not check_user_was_created(new_user_data, already_created_users):
                user_data = new_user_data
                break
            if i == max_iterations - 1:
                raise Exception("Not unique user was find!!!")

    else:
        user_data = {
            "email": faker.email(),
            "password": faker.password(length=12)
        }

    return user_data


def get_unique_user_data(faker: ModuleType, already_created_users: list[dict], max_iterations: int = 20) -> dict:
    """max_iterations - max iterations to find unique data from faker"""
    """first_name, last_name, job"""

    if already_created_users != []:
        for i in range(max_iterations):
            new_user_data = {
                "first_name": faker.first_name(),
                "last_name": faker.last_name(),
                "job": faker.job()
            }
            if not check_user_was_created(new_user_data, already_created_users):
                user_data = new_user_data
                break
            if i == max_iterations - 1:
                raise Exception("Not unique user was find!!!")

    else:
        user_data = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "job": faker.job()
        }

    return user_data


def check_user_was_created(new_user: dict, created_users: list[dict]) -> bool:
    """email and id must be unique"""
    checks = []
    for user in created_users:
        for key in new_user.keys():
            if key in user.keys():
                if new_user[key] == user[key] and key == "id":
                    return True
                elif new_user[key] == user[key] and key == "email":
                    return True
                elif new_user[key] != user[key]:
                    checks.append(False)
                else:
                    checks.append(True)
            else:
                checks.append(False)
        if all(checks):
            return True
    return False
