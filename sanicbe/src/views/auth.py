from sanic import Blueprint
from sanic.log import logger
from models.user import User
from .user import userMultiAndScalarValidate
from helpers.func import (
    resJson,
    resType,
    lowerString,
    getUTCDate,
    is_hash_valid,
    validate_list,
    exceptionRaise
)
from helpers.validator import registerUserValidator
from helpers.query import insertQuery, updateById, findUserByEmail

import os
import jwt
from datetime import datetime

# -----------------
# API Class Section
# -----------------


class AuthController():
    a = Blueprint('auth', url_prefix='/')

    @a.post("/login")
    async def do_login(request):
        try:
            session = request.ctx.session
            body = request.json
            async with session.begin():
                GET_EMAIL = str(body.get('email', None))
                GET_CHALLENGE = str(body.get('challenge', None))
                LO_EMAIL = lowerString(GET_EMAIL)

                user_ = await findUserByEmail(session, User, LO_EMAIL, User.role)
                getUser_ = user_.to_dict()

                if not user_:
                    return resJson(resType.INVALID_AUTH)

                if not await is_hash_valid(GET_CHALLENGE, getUser_['challenge']):
                    return resJson(resType.INVALID_AUTH)

                setParam = {
                    "name": getUser_['name'],
                    "email": getUser_['email'],
                    "role": getUser_['role']['name'],
                    "exp": getUTCDate(True)
                }

                # Update last_login column
                await updateLastLogin(session, getUser_['id'], datetime.now())

                token = jwt.encode(
                    setParam, request.app.config.SECRET, algorithm="HS256")

            return resJson(resType.OK, {"name": getUser_['name'], "email": getUser_['email'], "token": token})
        except:
            exceptionRaise('do_login')

    @a.post("/register")
    async def do_register(request):
        try:
            session = request.ctx.session
            body = request.json
            # Input validation
            [valid, error] = registerUserValidator(body)
            if not valid:
                return resJson(resType.INVALID_PARAMS, error, len(error))

            GET_KEY = str(body.get('x-key', None))
            REG_KEY = os.getenv('REG_KEY', 'OtM1nterBWTzsoU')
            if GET_KEY != REG_KEY:
                return resJson(resType.INVALID_KEY)

            if validate_list(body):
                return resJson(resType.SINGLE_INSERT)

            async with session.begin():

                output = None
                [user, exist] = await userMultiAndScalarValidate(session, [body])
                if exist:
                    return resJson(resType.USER_EXIST)

                result = await insertQuery(session, User, user)

                for u in result:
                    output = dict(u)

            return resJson(resType.OK, output)
        except:
            exceptionRaise('do_register')


async def updateLastLogin(session, pk_: int, dateValue):
    values_ = {"status": True, "last_login": dateValue}
    setUser_ = await updateById(session, User, pk_, values_)
    if not setUser_:
        return False
    return True
