from sanic import Blueprint


class FileController():
    f = Blueprint("files", url_prefix="/uploads")

    f.static("/images", "./uploads/images", name="images")
    f.static("/files", "./uploads/files", name="files")

    # MARK: get image path, need app instance
    # print(app.url_for("static", name="files.images", filename="20211118083559.jpg"))
