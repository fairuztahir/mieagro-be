from helpers.helpers import (
    resJson,
    resType,
    exceptionRaise,
    capitalName,
    lowerString,
    validate_list,
    make_hash,
    valid_file_type,
    valid_file_size,
    getPathImage,
    write_file
)
from helpers.validator import paginateValidator, postUserValidator, updateUserValidator
from utils.utils import (
    paginatedQuery,
    insertQuery,
    findRecordByIdRelation,
    findRecordByColumn,
    findRecordById,
    softDelbyId,
    updateById
)
from utils.auth import protected
from sanic.log import logger
from sanic import Blueprint
from models.user import User
from models.role import Role

# -----------------
# API Class Section
# -----------------


class UserController():
    u = Blueprint('user', url_prefix='/')

    @u.get("/users")
    @protected
    async def getUsers(request):
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
                select_items: any = [User.id, User.fname, User.lname,
                                     User.email, User.challenge, User.avatar_url, User.created_at, User.role]

                [stmt, count_] = paginatedQuery(User, sort, order, select_items,
                                                size, page, User.role)

                users = []
                for row in await session.execute(stmt):
                    users.append(row.User.to_dict())

                total_ = await session.execute(count_)
                total = total_.scalar()

            return resJson(resType.OK, users, total)
        except:
            exceptionRaise('getUsers')

    @u.get("/user/<pk_:uuid>")
    @protected
    async def getUser(request, pk_):
        try:
            session = request.ctx.session
            async with session.begin():
                user = await findRecordByIdRelation(session, User, pk_, User.role)

            if not user:
                return resJson(resType.NO_RECORD)

            return resJson(resType.OK, user.to_dict())
        except:
            exceptionRaise('getUser')

    @u.post("/user")
    @protected
    async def createUser(request):
        try:
            session = request.ctx.session
            body = request.form
            img = request.files.get('avatar', None)
            if validate_list(body):
                return resJson(resType.SINGLE_INSERT)

            # Input validation
            [valid, error] = postUserValidator(body)
            if not valid:
                return resJson(resType.INVALID_PARAMS, error, len(error))

            async with session.begin():
                output = None
                [user, exist] = await userMultiAndScalarValidate(session, [body])
                if exist:
                    return resJson(resType.EMAIL_EXISTED)

                result = await insertQuery(session, User, user)

                for u in result:
                    output = dict(u)

                if img and img.type != 'text/plain':
                    [file_name, file_path, flag_] = await validateImage(img)

                    if flag_:
                        return resJson(flag_)

                    values_ = {"avatar_url": f"/images/{file_name}"}
                    setUser_ = await updateById(session, User, output['id'], values_)
                    if not setUser_:
                        return resJson(resType.FAIL_UPD)

            return resJson(resType.OK, output)
        except:
            exceptionRaise('createUser')

    @u.post("/users")
    @protected
    async def createUserMany(request):
        try:
            session = request.ctx.session
            body = request.json

            validate_ = validate_list(body)
            if not validate_:
                return resJson(resType.MULTI_INSERT)

            async with session.begin():

                id_list_ = []
                [user_list, exist_list] = await userMultiAndScalarValidate(session, body, validate_)
                if exist_list:
                    return resJson(resType.EMAIL_EXISTED, exist_list, len(exist_list))

                result = await insertQuery(session, User, user_list)

                for u in result:
                    id_list_.append(dict(u))

            return resJson(resType.OK, id_list_, len(id_list_))
        except:
            exceptionRaise('createUsers')

    @u.put("/user/<pk_:uuid>")
    @protected
    async def updateUser(request, pk_):
        try:
            session = request.ctx.session
            body = request.json
            resMsg = resType.SUCCESS_UPD
            # Input validation
            [valid, error] = updateUserValidator(body)
            if not valid:
                return resJson(resType.INVALID_PARAMS, error, len(error))

            async with session.begin():
                user_ = await findRecordByIdRelation(session, User, pk_, User.role)
                if not user_:
                    return resJson(resType.NO_RECORD)

                getfName = body.get('first_name', None)
                getlName = body.get('last_name', None)
                getEmail = body.get('email', None)
                getChallenge = body.get('challenge', None)
                getRole = body.get('role', None)
                getStatus = body.get('status', None)

                # TODO: implement schema validation for mandatory field
                convert_fname = capitalName(getfName)
                convert_lname = capitalName(getlName)
                convert_email = lowerString(getEmail)

                values_ = {}
                if (getfName) and (user_.fname != convert_fname):
                    values_['fname'] = convert_fname

                if (getfName) and (user_.lname != convert_lname):
                    values_['lname'] = convert_lname

                if (getEmail) and (user_.email != convert_email):
                    getId = await checkEmailExist(session, getEmail)
                    if getId:
                        return resJson(resType.USER_EXIST)

                    values_['email'] = convert_email

                if getChallenge:
                    hashed = await make_hash(getChallenge)
                    values_['challenge'] = hashed

                if getRole:
                    role_ = await findRecordByColumn(session, Role, Role.name, capitalName(getRole))
                    if not role_:
                        return resJson(resType.INVALID_ROLE, {})
                    if role_ != user_.role_id:
                        values_['role_id'] = role_

                if (getStatus != None) and (bool(getStatus) != user_.status):
                    values_['status'] = bool(getStatus)

                if len(values_) < 1:
                    return resJson(resType.NO_UPD, {})

                setUser_ = await updateById(session, User, pk_, values_)
                if not setUser_:
                    resMsg = resType.FAIL_UPD

            return resJson(resMsg, setUser_)
        except:
            exceptionRaise('updateUser')

    @u.delete("/user/<pk_:uuid>")
    @protected
    async def destroyUser(request, pk_):
        try:
            session = request.ctx.session
            resMsg = resType.SUCCESS_DEL
            async with session.begin():
                user = await findRecordById(session, User, pk_)
                if not user:
                    return resJson(resType.NO_RECORD)

                destroy = await softDelbyId(session, User, pk_)
                if not destroy:
                    resMsg = resType.FAIL_DELETE

            return resJson(resMsg, destroy)
        except:
            exceptionRaise('destroyUser')

    @u.post("/user/avatar/<pk_:uuid>")
    @protected
    async def uploadAvatar(request, pk_):
        try:
            session = request.ctx.session
            body = request.files.get('avatar', None)
            if (not body) or (body.type == 'text/plain'):
                return resJson(resType.NO_IMAGE_FOUND)

            # print(request.ip)
            async with session.begin():
                # Find user if exist
                user_ = await findRecordByIdRelation(session, User, pk_, User.role)
                if not user_:
                    return resJson(resType.NO_RECORD)

                # get old image url
                user_ = user_.to_dict()
                # Store image file
                [file_name, file_path, flag_] = await validateImage(body, user_['avatar_url'])

                if flag_:
                    return resJson(flag_)

                values_ = {"avatar_url": f"/images/{file_name}"}
                setUser_ = await updateById(session, User, pk_, values_)
                if not setUser_:
                    return resJson(resType.FAIL_UPD)

            return resJson(resType.OK, setUser_)
        except:
            exceptionRaise('uploadAvatar')


# -----------------
# functions section
# -----------------

async def userMultiAndScalarValidate(session, body, multi=False):
    try:
        user_, user_list, exist_list, temp_role, temp_id = None, [], [], None, None

        for b in body:
            getfName = b.get('first_name', None)
            getlName = b.get('last_name', None)
            getEmail = b.get('email', None)
            getChallenge = b.get('challenge', None)
            getRole = b.get('role', 'user')

            getId = await checkEmailExist(session, getEmail)
            if getId:
                existing = {"record": getEmail, "status": False}
                exist_list.append(existing)
            else:
                if getRole != temp_role:
                    role_ = await findRecordByColumn(session, Role, Role.name, capitalName(getRole))
                    if not role_:
                        role_ = await findRecordByColumn(session, Role, Role.name, capitalName('user'))

                    temp_role = getRole
                    temp_id = role_

                hashed = await make_hash(getChallenge)
                convert_fname = capitalName(getfName)
                convert_lname = capitalName(getlName)
                convert_email = lowerString(getEmail)

                user_ = {"fname": convert_fname, "lname": convert_lname,
                         "email": convert_email, "challenge": hashed, "role_id": temp_id}

                if multi:
                    user_list.append(user_)

        if multi:
            return [user_list, exist_list]

        return [user_, exist_list]
    except:
        exceptionRaise('userMultiAndScalarValidate')


async def validateImage(body, oldPath=None):
    try:
        image_type = body.type
        image_body = body.body
        image_name = lowerString(body.name)
        flag = None
        validate_type = await valid_file_type(image_name, image_type)
        if not validate_type:
            flag = resType.INVALID_IMG_TYPE

        validate_size = await valid_file_size(image_body)
        if not validate_size:
            flag = resType.INVALID_IMG_SIZE

        [file_name, file_path] = await getPathImage(image_name)

        if not flag:
            await write_file(file_path, image_body, oldPath)

        return [file_name, file_path, flag]
    except:
        exceptionRaise('validateImage')


async def checkEmailExist(session, email):
    flag = True
    user_id = await findRecordByColumn(session, User, User.email, lowerString(email), True)
    if not user_id:
        flag = False

    return flag


# class UserSchema(Schema):
#     id = fields.Integer(required=True)
#     email = fields.Email(required=True)
#     password = fields.String(required=True, validate=[Length(min=4)])


# class Auth(HTTPMethodView):
#     async def get(self, request):
#         return json({"hello": "world"})

#     async def post(self, request):
#         logger.info(request.json)
#         res, errs = UserSchema(exclude=['id']).load(request.json)
#         if errs:
#             return json({"valid": False, "data": errs}, status=400)

#         async with request.app.db.acquire() as conn:
#             _user = await conn.fetchrow('''
#             SELECT * FROM users WHERE email=$1
#             ''', res['email'])

#         if not (
#                 _user and
#                 pbkdf2_sha256.verify(res['password'], _user['password'])
#         ):
#             return json({
#                 "valid": False,
#                 "data": 'Wrong email or password'
#             }, status=401)

#         data = UserSchema(exclude=['password']).dump(_user).data

#         token = uuid.uuid4().hex

#         await request.app.redis.set(token, ujson.dumps(data))

#         return json({"valid": True, "data": {"access_token": token}})
