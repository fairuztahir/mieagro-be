from sanic import Blueprint


class FileController():
    f = Blueprint("files", url_prefix="/uploads")

    f.static("/images", "./uploads/images", name="images")
    f.static("/files", "./uploads/files", name="files")
