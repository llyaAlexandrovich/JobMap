import logging
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError

from tables.models import SpatialInfo, ProvidersInfo, Vacancy, Tag, CompanyInfo
from tables.models.relationship.m2m_vacancies_tags import vacancies_tags
from tables import get_db_asession


async def create_new_vacancy_transaction(**kwargs) -> bool:
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


                spatial_stmt = select(SpatialInfo.id).where(SpatialInfo.location_name == kwargs["location_name"])
                spatial_res = await session.execute(spatial_stmt)
                location_id = spatial_res.scalar()

                if not location_id:
                    try:

                        new_spatial = SpatialInfo(location_name=kwargs["location_name"], geom=kwargs["geom"])
                        session.add(new_spatial)
                        await session.flush()
                        location_id = new_spatial.id
                    except IntegrityError:

                        
                        spatial_res = await session.execute(spatial_stmt)
                        location_id = spatial_res.scalar()


                if not location_id:
                    logging.error(f"Could not get or create location_id for {kwargs['location_name']}")
                    return False


                company_stmt = select(CompanyInfo.id).where(CompanyInfo.company_name == kwargs["company_name"])
                company_res = await session.execute(company_stmt)
                company_id = company_res.scalar()

                if not company_id:
                    try:
                        new_company = CompanyInfo(company_name=kwargs["company_name"])
                        session.add(new_company)
                        await session.flush()
                        company_id = new_company.id
                    except IntegrityError:
                        await session.rollback()
                        company_res = await session.execute(company_stmt)
                        company_id = company_res.scalar()

                if not company_id:
                    logging.error(f"Could not get or create company_id for {kwargs['company_name']}")
                    return False


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


                tags_array = kwargs.get("tags_array")
                if tags_array and vacancy_id:
                    tag_ids = []
                    for tag_name in tags_array:
                        tag_sel = select(Tag.id).where(Tag.tag_name == tag_name)
                        tag_sel_res = await session.execute(tag_sel)
                        t_id = tag_sel_res.scalar()

                        if not t_id:
                            try:
                                new_tag = Tag(tag_name=tag_name)
                                session.add(new_tag)
                                await session.flush()
                                t_id = new_tag.id
                            except IntegrityError:
                                await session.rollback()
                                tag_sel_res = await session.execute(tag_sel)
                                t_id = tag_sel_res.scalar()
                        
                        if t_id:
                            tag_ids.append(t_id)


                    if tag_ids:
                        m2m_values = [{"vacancy_id": vacancy_id, "tag_id": t_id} for t_id in tag_ids]
                        m2m_stmt = (
                            insert(vacancies_tags)
                            .values(m2m_values)
                            .on_conflict_do_nothing()
                        )
                        await session.execute(m2m_stmt)
                    
        return True

    except Exception as e:
        logging.error(f"Vacancy transaction error: {e}")
        return False
