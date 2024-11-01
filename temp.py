from tortoise.expressions import Q
from app.controllers import database_controller

q = Q()
q &= Q(status__contains=1)


async def get_database_list():
    total, database_objs = await database_controller.list(
        page=1,
        page_size=10,
        search=q,
        order=["id"],
        prefetch=["create_by_id"],
    )
    print(database_objs)
    return total, database_objs


if __name__ == "__main__":
    import asyncio

    asyncio.run(get_database_list())
