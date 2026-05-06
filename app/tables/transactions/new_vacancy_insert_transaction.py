import logging
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from tables.models import SpatialInfo, ProvidersInfo, Vacancy


async def create_new_vacancy_transaction(**kwargs) -> bool:
    """
    Create DB transaction with received info

    :param provider_name:
    :param provider_link:
    :param vacancy_name:
    :param vacancy_type:
    :param vacancy_link:
    :param visibility:
    :param tags_array:
    :param hash:
    :param location_name:
    :param geom:
    """
    session_factory = await get_db_asession("bot")
    if not session_factory:
        return False

    try:
        async with session_factory as session:
            async with session.begin():
                provider_stmt = (
                    insert(ProvidersInfo)
                    .values(
                        provider_name=kwargs["provider_name"],
                        link=kwargs.get("provider_link", None)
                    )
                    .on_conflict_do_nothing(index_elements=["provider_name"])
                )


                vacancy_stmt = (
                    insert(Vacancy)
                    .values(
                        vacancy_name=kwargs["vacancy_name"],
                        vacancy_type=kwargs["vacancy_type"],
                        vacancy_link=kwargs.get("vacancy_link"),
                        visibility=kwargs.get("visibility", 0),
                        tags_array=kwargs.get("tags_array", []),
                        content_hash=kwargs["hash"]
                    )
                    .on_conflict_do_nothing(index_elements=["content_hash"])
                    .returning(Vacancy.id)
                )
                vac_res = await session.execute(vacancy_stmt)
                vacancy_id = vac_res.scalar()

                if not vacancy_id:
                    logging.info(f"Vacancy with hash {kwargs["hash"]} already exists.")
                    

                spatial_stmt = (
                    insert(SpatialInfo)
                    .values(
                        location_name=kwargs["location_name"],
                        geom=kwargs["geom"],
                        vacancy_id=vacancy_id
                    )
                )
                await session.execute(spatial_stmt)

        logging.info(f"Successfully created vacancy: {kwargs['vacancy_name']}")
        return True

    except Exception as e:
        logging.error(f"Failed to execute vacancy transaction: {e}")
        return False
