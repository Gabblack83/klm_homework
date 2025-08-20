import os
from shutil import rmtree, copytree, copy2

from common.conventions import VUE_FOLDER, VUE_DIST_FOLDER, VUE_STATIC_FOLDER


def build_vue() -> None:

    os.chdir(VUE_FOLDER)
    rmtree(VUE_DIST_FOLDER, ignore_errors=True)
    rmtree(VUE_STATIC_FOLDER, ignore_errors=True)

    os.system("npm run build")

    if not os.path.exists(VUE_STATIC_FOLDER):
        os.makedirs(VUE_STATIC_FOLDER)

    vue_files: list[str] = os.listdir(VUE_DIST_FOLDER)
    for file in vue_files:
        source = VUE_DIST_FOLDER.joinpath(file)

        if os.path.isdir(source):
            copytree(source, VUE_STATIC_FOLDER.joinpath(file))
        else:
            copy2(source, VUE_STATIC_FOLDER.joinpath(file))


if __name__ == "__main__":
    build_vue()
