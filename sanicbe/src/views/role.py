from helpers.helpers import (
    resJson,
    resType,
    exceptionRaise,
    capitalName,
    validate_list,
    capitalSentence,
    invertBool,
    listRemoveIf,
    count_list,
    find_duplicate,
    set_dict
)
from helpers.validator import paginateValidator, postRoleValidator
from utils.utils import (
    paginatedQuery,
    insertQuery,
    softDelbyId,
    findRecordById,
    findRecordByColumn,
    updateById
)
from sanic.log import logger
from sanic import Blueprint
from models.role import Role
from utils.auth import protected

# -----------------
# API Class Section
# -----------------


class RoleController():
    r = Blueprint('role', url_prefix='/')

    @r.get("/roles")
    @protected
    async def getRoles(request):
        try:
            session = request.ctx.session
            params = request.args
            # Input validation
            [valid, error] = paginateValidator(params)
            if not valid:
                return resJson(resType.INVALID_PARAMS, error, len(error))

            async with session.begin():
                size = int(params.get('pageSize', 10))
                page = int(params.get('page', 1))
                sort = str(params.get('sortParam', 'created_at'))
                order = str(params.get('sortBy', 'DESC'))
                select_items: any = [Role.id, Role.name,
                                     Role.description, Role.created_at]

                [stmt, count_] = paginatedQuery(
                    Role, sort, order, select_items, size, page)
                result = await session.execute(stmt)
                roles = result.all()

                result_dict = [dict(role) for role in roles]
                total_ = await session.execute(count_)
                total = total_.scalar()

            return resJson(resType.OK, result_dict, total)
        except:
            exceptionRaise('getRoles')

    @r.get("/role/<pk_:uuid>")
    @protected
    async def getRole(request, pk_):
        try:
            session = request.ctx.session
            async with session.begin():
                role = await findRecordById(session, Role, pk_)

            if not role:
                return resJson(resType.NO_RECORD)

            return resJson(resType.OK, role.to_dict())
        except:
            exceptionRaise('getRole')

    @r.post("/role")
    @protected
    async def createRole(request):
        try:
            session = request.ctx.session
            body = request.json
            # Input validation
            [valid, error] = postRoleValidator(body)
            if not valid:
                return resJson(resType.INVALID_PARAMS, error, len(error))

            if validate_list(body):
                return resJson(resType.SINGLE_INSERT)

            async with session.begin():
                output = None
                [role, err] = await roleMultiAndScalarValidate(session, [body])

                if err:
                    filtered = await listRemoveIf('status', [role])
                    return resJson(resType.EXISTING, filtered, len(filtered))

                result = await insertQuery(session, Role, role)

                for u in result:
                    output = dict(u)

            return resJson(resType.OK, output)
        except:
            exceptionRaise('createRole')

    @r.post("/roles")
    @protected
    async def createRoles(request):
        try:
            session = request.ctx.session
            body = request.json
            if not validate_list(body):
                return resJson(resType.MULTI_INSERT)

            async with session.begin():
                id_list_ = []
                [role, err, duplicate] = await roleMultiAndScalarValidate(session, body, True)

                if (err) and (len(duplicate) > 0):
                    return resJson(resType.DUPLICATE, duplicate, await count_list(duplicate))

                if (err) and (len(role) > 0):
                    if len(role) == 1:
                        list_ = [role]
                    else:
                        list_ = role
                    filtered = await listRemoveIf('status', list_)
                    return resJson(resType.EXISTING, filtered, await count_list(filtered))

                result = await insertQuery(session, Role, role)

                for u in result:
                    id_list_.append(dict(u))

            return resJson(resType.OK, id_list_, len(id_list_))
        except:
            exceptionRaise('createRoles')

    @r.delete("/role/<pk_:uuid>")
    @protected
    async def destroyRole(request, pk_):
        try:
            session = request.ctx.session
            resMsg = resType.SUCCESS_DEL
            async with session.begin():
                role = await findRecordById(session, Role, pk_)
                if not role:
                    return resJson(resType.NO_RECORD)

                destroy = await softDelbyId(session, Role, pk_)
                if not destroy:
                    resMsg = resType.FAIL_DELETE

            return resJson(resMsg, destroy)
        except:
            exceptionRaise('destroyRole')

    @r.put("/roles")
    @protected
    async def destroyRoles(request):
        try:
            session = request.ctx.session
            body = request.json
            resMsg = resType.SUCCESS_DEL
            async with session.begin():
                getIds = body.get('ids', [])
                if len(getIds) == 0:
                    return resJson(resType.NO_INPUT)

                # validate if record not exists
                role = await findRecordById(session, Role, getIds, True)
                valid_role = await set_dict(role)

                not_exists_ = await findNotExists(getIds, valid_role)

                if len(not_exists_) > 0:
                    return resJson(resType.NO_RECORD, not_exists_, len(not_exists_))

                destroy = await softDelbyId(session, Role, getIds)
                if not destroy:
                    resMsg = resType.FAIL_DELETE

                output = await set_dict(destroy)
            return resJson(resMsg, output, len(output))
        except:
            exceptionRaise('destroyRoles')

    @r.put("/role/<pk_:uuid>")
    @protected
    async def updateRole(request, pk_):
        try:
            session = request.ctx.session
            body = request.json
            # Input validation
            [valid, error] = postRoleValidator(body)
            if not valid:
                return resJson(resType.INVALID_PARAMS, error, len(error))

            resMsg = resType.SUCCESS_UPD
            async with session.begin():
                role_ = await findRecordById(session, Role, pk_)
                if not role_:
                    return resJson(resType.NO_RECORD)

                getName = body.get('name', None)
                getDesc = body.get('desc', None)

                convert_name = capitalName(getName)
                convert_desc = capitalSentence(getDesc)

                values_ = {}
                if (getName) and (role_.name != convert_name):
                    values_['name'] = convert_name

                if (getDesc) and (role_.description != convert_desc):
                    values_['description'] = convert_desc

                if len(values_) < 1:
                    return resJson(resType.NO_UPD, {})

                setRole_ = await updateById(session, Role, pk_, values_)
                if not setRole_:
                    resMsg = resType.FAIL_UPD

            return resJson(resMsg, setRole_)
        except:
            exceptionRaise('updateRole')


# -----------------
# functions section
# -----------------
async def roleMultiAndScalarValidate(session, body, multi=False):
    try:
        role_list, temp_list, temp_name, flag_ = [], [], None, False
        outer_flag = False

        for b in body:
            getName = str(b.get('name', None))
            getDesc = b.get('desc', None)

            if getName != temp_name:
                role_ = await findRecordByColumn(session, Role, Role.name, capitalName(getName))
                if role_:
                    flag_ = True
                    outer_flag = True
                else:
                    flag_ = False

                temp_name = getName

            convert_name = capitalName(getName)
            convert_desc = capitalSentence(getDesc)

            role_ = {"name": convert_name, "description": convert_desc}
            existing = {"record": temp_name, "status": invertBool(flag_)}

            if multi:
                role_list.append(role_)
                temp_list.append(existing)

        if multi:
            dup_list = await find_duplicate(role_list, 'name')
            if dup_list:
                outer_flag = True

            if outer_flag:
                return [temp_list, outer_flag, dup_list]

            return [role_list, outer_flag, None]

        if outer_flag:
            return [existing, outer_flag]

        return [role_, outer_flag]
    except:
        exceptionRaise('roleMultiAndScalarInput')


async def findNotExists(ori_, validated_):
    try:
        display_err = []
        for a in ori_:
            flag_ = False
            for b in validated_:
                if a == b.get('id'):
                    flag_ = True
                    break
            if not flag_:
                display_err.append(a)

        return display_err
    except:
        exceptionRaise('findNotExists')
