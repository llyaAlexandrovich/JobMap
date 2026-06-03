import logging
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert


from tables.models import SpatialInfo, ProvidersInfo, Vacancy, Tag, CompanyInfo
from tables.models.relationship.m2m_vacancies_tags import vacancies_tags
from tables import get_db_asession



async def create_new_vacancy_transaction(**kwargs) -> bool:
    """
    Create DB transaction with received 

    :param provider_name:
    :param provider_link:
    :param vacancy_name:
    :param vacancy_type:
    :param vacancy_link:
    :param visibility:
    :param tags_array:
    :param hash:
    :param location_name:
    :param company_name:
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
                        provider_link=kwargs["provider_link"]
                    )
                    .on_conflict_do_nothing(index_elements=["provider_name"])
                )
                await session.execute(provider_stmt)


                spatial_stmt = (
                    insert(SpatialInfo)
                    .values(
                        location_name=kwargs["location_name"],
                        geom=kwargs["geom"]
                    )
                    .returning(SpatialInfo.id)
                )
                spatial_res = await session.execute(spatial_stmt)
                location_id = spatial_res.scalar()


                company_stmt = (
                    insert(CompanyInfo)
                    .values(
                        company_name=kwargs["company_name"]
                    )
                    .on_conflict_do_nothing(index_elements=["company_name"])
                    .returning(CompanyInfo.id)
                )
                company_res = await session.execute(company_stmt)
                company_id = company_res.scalar()

                vacancy_stmt = (
                    insert(Vacancy)
                    .values(
                        vacancy_name=kwargs["vacancy_name"],
                        vacancy_type=kwargs.get("vacancy_type", 0),
                        vacancy_link=kwargs.get("vacancy_link"),
                        visibility=kwargs.get("visibility", 0),
                        hash=kwargs["hash"],
                        location=location_id,
                        company=company_id
                    )
                    .on_conflict_do_nothing(index_elements=["hash"])
                    .returning(Vacancy.id)
                )
                vac_res = await session.execute(vacancy_stmt)
                vacancy_id = vac_res.scalar()

                if not vacancy_id:
                    logging.info(f"Vacancy with hash \"{kwargs['hash']}\" already exists.")
                    return False


                if kwargs.get("tags_array"):
                    for tag_name in kwargs["tags_array"]:
                        tag_stmt = insert(Tag).values(tag_name=tag_name).on_conflict_do_nothing()
                        await session.execute(tag_stmt)

                        t_id_res = await session.execute(select(Tag.id).where(Tag.tag_name == tag_name))
                        tag_id = t_id_res.scalar()

                        await session.execute(
                            insert(vacancies_tags).values(vacancy_id=vacancy_id, tag_id=tag_id)
                        )
        return True

    except Exception as e:
        logging.error(f"Vacancy transaction error: {e}")
        return False

