from sqlalchemy import select, func, insert, delete, update
from sqlalchemy.orm import selectinload, joinedload
from helpers.func import valueOf, exceptionRaise, validate_list

import arrow

# -------------------------
# Utility functions Section
# -------------------------


# Paginated records
def paginatedQuery(model_, sort_, order_, selectList_, pageSize_=10, page_=0, relation_=None):
    if pageSize_ < 1:
        pageSize_ = 10

    if page_ < 1:
        page_ = 1

    offset = pageSize_ * (page_ - 1)

    if sort_:
        sort = sort_.lower()
        order = order_.upper()
        orderVar = model_.__dict__.get(sort)

        if order != valueOf.ASC.fulltext:
            orderVar = orderVar.desc()

    count_ = select([func.count(model_.id)]).\
        where(model_.deleted_at.is_(None))

    if relation_:
        stmt = select(model_).\
            where(model_.deleted_at.is_(None)).\
            options(selectinload(relation_)).\
            order_by(orderVar).\
            limit(pageSize_).offset(offset)

        return [stmt, count_]
    else:
        stmt = select(selectList_).\
            where(model_.deleted_at.is_(None)).\
            order_by(orderVar).\
            limit(pageSize_).offset(offset)

        return [stmt, count_]


# Find record data by Id
async def findRecordById(session_, model_, key_, returnId=False):
    try:
        flag_ = validate_list(key_)
        select_ = model_
        if returnId:
            select_ = model_.id

        if not flag_:
            stmt = select(select_).where(model_.id == key_).\
                where(model_.deleted_at.is_(None))
        else:
            stmt = select(select_).where(model_.id.in_(key_)).\
                where(model_.deleted_at.is_(None))

        result = await session_.execute(stmt)

        if flag_:
            return result.all()

        return result.scalar()
    except:
        exceptionRaise('findRecordById')


# Find record data by Id wth relation
async def findRecordByIdRelation(session_, model_, pk_, relation_):
    try:
        stmt = select(model_).where(model_.id == pk_).\
            where(model_.deleted_at.is_(None)).\
            options(selectinload(relation_))

        result = await session_.execute(stmt)

        return result.scalar()
    except:
        exceptionRaise('findRecordByIdRelation')


# Insert record into db, value suport List and Scalar type
async def insertQuery(session, model, value):
    try:
        stmt = insert(model).\
            values(value).returning(model.id)
        result = await session.execute(stmt)

        return result.all()
    except:
        exceptionRaise('insertQuery')


# Find record data by column name and it's value
# Set onlyId_ = True to return only Id value
async def findRecordByColumn(session_, model_, column_, value_, onlyId_=True):
    try:
        if onlyId_:
            stmt = select([model_.id]).where(column_ == value_).\
                filter(model_.deleted_at.is_(None))
        else:
            stmt = select(model_).where(column_ == value_).\
                filter(model_.deleted_at.is_(None))

        result = await session_.execute(stmt)
        record = result.scalar()
        # record = result.fetchone()
        return record
    except:
        exceptionRaise('findRecordByColumn')


# Find record data by column name and it's value (Background process)
# Set onlyId_ = True to return only Id value
async def findRecordByColumnCron(session_, model_, column_, value_, onlyId_=True):
    try:
        if onlyId_:
            stmt = select([model_.id]).where(column_ == value_).\
                filter(model_.deleted_at.is_(None))
        else:
            stmt = select(model_).where(column_ == value_).\
                filter(model_.deleted_at.is_(None))

        result = await session_.execute(stmt)
        record = result.fetchone()

        return record
    except:
        exceptionRaise('findRecordByColumn')


# Search record data by column name and it's value
# Set onlyId_ = True to return only Id value
async def searchRecordByColumn(session_, model_, column_, value_, onlyId_=True):
    try:
        if onlyId_:
            stmt = select([model_.id]).where(column_.ilike(f'%{value_}%')).\
                filter(model_.deleted_at.is_(None))
        else:
            stmt = select(model_).where(column_.ilike(f'%{value_}%')).\
                filter(model_.deleted_at.is_(None))

        result = await session_.execute(stmt)
        record = result.scalar()

        if not onlyId_:
            return record.to_dict()
        else:
            return record

    except:
        exceptionRaise('searchRecordByColumn')


# Soft delete record by Id
async def softDelbyId(session_, model_, pk_):
    try:
        flag_ = validate_list(pk_)
        a = arrow.utcnow().datetime
        if flag_:
            stmt = update(model_).where(model_.id.in_(pk_)).\
                where(model_.deleted_at.is_(None)).\
                values(deleted_at=a.replace(tzinfo=None)).\
                returning(model_.id)
        else:
            stmt = update(model_).where(model_.id == pk_).\
                where(model_.deleted_at.is_(None)).\
                values(deleted_at=a.replace(tzinfo=None)).\
                returning(model_.id)

        result = await session_.execute(stmt)

        if flag_:
            return result.all()

        return result.scalar()
    except:
        exceptionRaise('softDelbyId')


# Destroy record by Id
async def delRecordbyId(session_, model_, pk_):
    try:
        stmt = delete(model_).where(model_.id == pk_).\
            returning(model_.id)

        result = await session_.execute(stmt)
        return result.scalar()
    except:
        exceptionRaise('delRecordbyId')


# Update record by Id
async def updateById(session_, model_, pk_, values_):
    try:
        stmt = update(model_).where(model_.id == pk_).\
            where(model_.deleted_at.is_(None)).\
            values(values_).\
            returning(model_.id)

        result = await session_.execute(stmt)
        return result.scalar()
    except:
        exceptionRaise('updateById')


# Compare between 2 lists
async def compareList(l1, l2):
    if(l1 == l2):
        return True
    else:
        return False


# Find user by email
async def findUserByEmail(session_, model_, value_, relation_):
    try:
        if not relation_:
            stmt = select(model_).where(model_.email.ilike(f'%{value_}%')).\
                filter(model_.deleted_at.is_(None))
        else:
            stmt = select(model_).where(model_.email == value_).\
                where(model_.deleted_at.is_(None)).\
                options(selectinload(relation_))

        result = await session_.execute(stmt)
        record = result.scalar()

        return record
    except:
        exceptionRaise('findUserByEmail')
