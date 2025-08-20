import os

from dotenv import load_dotenv
from flask import Flask, send_file

from build_vue.build import build_vue
from common.conventions import VUE_STATIC_FOLDER

app = Flask(__name__)

load_dotenv()
LOCAL_DEV_ENV: bool = os.getenv("LOCAL_DEV_ENV") == "True"


@app.route("/", defaults={"folder": "", "file_name": "index.html"}, methods=["GET"])
@app.route("/<folder>/<file_name>", methods=["GET"])
def get_static_files(folder: str, file_name):
    if LOCAL_DEV_ENV and file_name == "index.html":
        build_vue()

    static_file = VUE_STATIC_FOLDER.joinpath(folder).joinpath(file_name)
    if os.path.exists(static_file) and os.path.isfile(static_file):
        return send_file(static_file)


if __name__ == "__main__":
    if LOCAL_DEV_ENV:
        build_vue()
    app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8001)))
