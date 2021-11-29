from sanic.log import logger
from sanic.exceptions import ServerError
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sanic.response import json
from enum import Enum
from json import dumps, loads
from itertools import groupby
from dateutil.parser import parse

import decimal
import datetime
import os
import arrow
import aiofiles
import uuid

# ------------------------
# Helper functions Section
# ------------------------


# Enum values for response type
class resType(Enum):
    OK = 200, 'Success'
    SUCCESS_UPD = 201, 'Record successfully updated.'
    SUCCESS_DEL = 204, 'Record successfully deleted.'
    INVALID_PARAMS = 400, 'Invalid input parameters. Please try again.'
    NO_UPD = 304, 'Nothing to update 🥱.'
    NO_RECORD = 10000, 'No record found.'
    EMAIL_EXISTED = 10001, 'The specified E-MAIL address already exists. Please try again.'
    INVALID_PK = 10002, 'Invalid record ID. Please try again.'
    MULTI_INSERT = 10003, 'Data not suitable for multiple insert. Please try again.'
    SINGLE_INSERT = 10004, 'Data not suitable for single insert. Please try again.'
    DUPLICATE = 10005, 'Found duplicate data in records. Please try again.'
    EXISTING = 10006, 'Found existing data in records. Please try again.'
    FAIL_DELETE = 10007, 'Record failed to delete. Please try again.'
    FAIL_UPD = 10008, 'Record failed to update. Please try again.'
    NO_INPUT = 10009, 'Expecting to receive data but none available. Please try again.'
    INVALID_AUTH = 10010, 'Wrong E-MAIL or PASSWORD. Please try again.'
    INVALID_KEY = 10111, 'Sorry your registration KEY is invalid. Please contact SYSTEM ADMIN and try again.'
    INVALID_IMG_TYPE = 10112, 'Invalid image type. Only JPG, JPEG or PNG formats are accepted.'
    INVALID_IMG_SIZE = 10113, 'Image size is larger than 2MB. Please try again.'
    NO_IMAGE_FOUND = 10114, 'No image found. Please try again.'
    INVALID_DATE = 10115, 'Invalid date input. Please use YYYY-MM-DD format and try again.'
    USER_EXIST = 10116, 'User already exists. Please try again.'
    INVALID_ROLE = 10117, 'Invalid role name. Please try again.'

    def __new__(cls, value, name):
        member = object.__new__(cls)
        member._value_ = value
        member.fulltext = name
        return member

    def __int__(self):
        return self.value


# Filter date, datetime to ISO, decimal to float
# MARK: for resJson() purpose
# TODO: will add more in future to data massage
def default(o):
    if isinstance(o, uuid.UUID):
        return str(o)
    elif type(o) is datetime.date or type(o) is datetime.datetime:
        return convertISO_TZ(o)
    elif type(o) is decimal.Decimal:
        return float(o)


# Enum values for settings
class valueOf(Enum):
    DATE_FORMAT = 1, 'YYYY-MM-DD'
    DATETIME_FORMAT = 2, 'YYYY-MM-DD HH:mm:ss'
    STRFTIME = 3, "%Y%m%d%H%M%S"
    TIME_ZONE = 4, os.getenv('TIMEZONE_ENV', 'UTC')
    UTC_ZONE = 5, 'UTC'
    ASC = 6, 'ASC'
    DESC = 7, 'DESC'
    UPLOAD_DIR = 8, './uploads'

    def __new__(cls, value, name):
        member = object.__new__(cls)
        member._value_ = value
        member.fulltext = name
        return member

    def __int__(self):
        return self.value


# Convert server UTC datetime to local
# MARK: For default() pupose
def convertISO_TZ(value):
    tz = valueOf.TIME_ZONE
    fmt = valueOf.DATETIME_FORMAT
    utc = arrow.get(value)
    return utc.to(tz.fulltext).format(fmt.fulltext)


# Check if string type
def validate_str(value: any):
    return isinstance(value, str)


# Check if list type
def validate_list(value: any):
    return isinstance(value, list)


# API responses
def resJson(value: any = resType.OK, data: any = None, count=0, statusFlag=False):
    o_data = None

    if validate_list(data):
        o_data = loads(dumps(data, default=default))
        return json({
            "status": int(value),
            "message": value.fulltext,
            "data": o_data,
            "total": count
        })

    if validate_str(data):
        o_data = str(data)
    else:
        o_data = loads(dumps(data, default=default))

    if statusFlag:
        flag = int(value)
    else:
        flag = 200

    return json({
        "status": int(value),
        "message": value.fulltext,
        "data": o_data
    }, flag)


# Raise an exception if system error
def exceptionRaise(value: str, code: int = 501):
    raise ServerError("Something went wrong at: " + value, status_code=code)


# Capital letter at begin, after dot
def capitalSentence(value: str):
    if (not value) or (value == ''):
        return None

    convert = '. '.join(
        map(lambda s: s.strip().capitalize(), value.split('.')))
    add_dot = addDotEndSentence(convert)
    return add_dot


# Convert cap letter each strings
def capitalName(value: str):
    if (not value) or (value == ''):
        return None
    return str.title(value)


# Convert str to small cap
def lowerString(value: str):
    if (not value) or (value == ''):
        return None
    return value.lower()


# Convert str to capital letter
def upperString(value: str):
    if (not value) or (value == ''):
        return None
    return value.upper()


# Add dot at the end on string/sentence
# MARK: For capitalSentence purpose
def addDotEndSentence(value: str):
    if (not value) or (value == ''):
        return None
    return value.strip() + "."


# Reverse bool value
def invertBool(value: bool):
    if value:
        return False
    else:
        return True


# Pop list data if meet condition
async def listRemoveIf(key_, list_):
    await sortList(list_, key_)
    for i, elem in reversed_enumerate(list_):
        if elem[key_] == True:
            list_.pop(i)
    return list_


# Reverse List data
# MARK: For listRemoveIf purpose
def reversed_enumerate(collection: list):
    for i in range(len(collection)-1, -1, -1):
        yield i, collection[i]


# Reverse List data using lambda
# MARK: For listRemoveIf & find_duplicate purpose
async def sortList(data, sortValue, orderAsc=False):
    return data.sort(key=lambda x: x.get(sortValue), reverse=orderAsc)


# Count with duplicate compared to len()
async def count_list(list):
    count = 0
    for element in list:
        count += 1
    return count


# Find duplicate data
async def find_duplicate(data, key_):
    list_ = []
    await sortList(data, key_)
    for x, g in groupby(data):
        if (count := len(list(g))) > 1:
            list_.append({key_: x[key_], 'count': count})
    return list_


# Lazy load w/out custom to_dict() in model
async def set_dict(proxy_):
    return [dict(row) for row in proxy_]


# Return python datetime
def getUTCDate(add=False):
    getDate = datetime.datetime.now()

    if add:
        getDate = datetime.datetime.now() + datetime.timedelta(hours=1)

    return getDate


# Hash challenge
async def make_hash(value):
    return pbkdf2_sha256.hash(value)


# validate challenge
async def is_hash_valid(value, hashed):
    return pbkdf2_sha256.verify(value, hashed)


# convert float number to int
# MARK: for pagination loop purpose
def count_loop_page(total, page_size):
    DIVIDE = total / page_size
    if (DIVIDE - int(DIVIDE) == 0):
        return 0
    else:
        return int(DIVIDE) + 1


# Image upload type validation
async def valid_file_type(file_name, file_type):
    file_name_type = file_name.split('.')[-1]
    if (file_name_type == "jpeg" or file_name_type == "jpg") and file_type == "image/jpeg":
        return True
    elif file_name_type == "png" and file_type == "image/png":
        return True
    return False


# Image upload size validation, 2010000 bit = 2.01 mb
async def valid_file_size(file_body):
    if len(file_body) < 2010000:
        return True
    return False


# Write file to path dir & del old file.
async def write_file(path, body, oldPath=None):
    async with aiofiles.open(path, 'wb') as f:
        await f.write(body)
    f.close()

    if oldPath:
        os.remove(f"./uploads{oldPath}")

    return True


# Set path for images type
async def getPathImage(file_name, defaultName=False):
    file_name_type = file_name.split('.')[-1]
    if defaultName:
        setName = file_name
    else:
        setName = datetime.datetime.now().strftime(
            valueOf.STRFTIME.fulltext)+'.'+file_name_type

    setPath = f"{valueOf.UPLOAD_DIR.fulltext}/images/{str(setName)}"
    return [setName, setPath]


# Set path for files type
async def getPathFile(file_name, defaultName=False):
    file_name_type = file_name.split('.')[-1]
    if defaultName:
        setName = file_name
    else:
        setName = datetime.datetime.now().strftime(
            valueOf.STRFTIME.fulltext)+'.'+file_name_type

    setPath = f"{valueOf.UPLOAD_DIR.fulltext}/files/{str(setName)}"
    return [setName, setPath]

# Validate uploads path


async def createUploadPath(app):
    # Create uploads folder if doesn't exist
    if not os.path.exists(app.config.UPLOAD_DIR+'/images'):
        os.makedirs(app.config.UPLOAD_DIR+'/images')

    if not os.path.exists(app.config.UPLOAD_DIR+'/files'):
        os.makedirs(app.config.UPLOAD_DIR+'/files')
    return True


async def is_valid_date(date):
    if date:
        try:
            parsed_value = parse(date)
            fmt = valueOf.DATE_FORMAT
            expected = arrow.get(parsed_value).format(fmt.fulltext)
            return [True, expected]
        except:
            return [False, None]
    return [False, None]
