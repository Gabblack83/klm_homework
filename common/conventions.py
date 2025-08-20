from pathlib import Path

PROJECT_DIR: Path = Path(__file__).parent.parent

VUE_FOLDER: Path = PROJECT_DIR.joinpath("vue")

VUE_DIST_FOLDER: Path = VUE_FOLDER.joinpath("dist")

VUE_STATIC_FOLDER: Path = PROJECT_DIR.joinpath("static/vue_app")