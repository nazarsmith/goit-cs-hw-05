import aioshutil
import logging
import os
import time

from matplotlib import pyplot as plt
from aiopath import AsyncPath

log_name = f"{time.time()}_logs.log"
logging.basicConfig(
    filename=log_name,
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)


async def read_folder(src_path: AsyncPath, dest_path: AsyncPath):
    if src_path == dest_path:
        logging.info(f"Skipping {src_path}, destination file is the same as source.")
        return
    elif await src_path.is_dir():
        async for child in src_path.iterdir():
            await read_folder(child, dest_path)
    elif await src_path.is_file():
        await copy_file(src_path, dest_path)


async def copy_file(src_path: AsyncPath, dest_path: AsyncPath):
    try:
        extension = os.path.basename(src_path).split(".")[-1]
        sub_dir = dest_path / extension
        file_path = AsyncPath(sub_dir / src_path.name)
        logging.debug(f"Copying {src_path} into {sub_dir}")

        if not await sub_dir.exists():
            await sub_dir.mkdir(parents=True, exist_ok=True)
            os.chmod(sub_dir, mode=0o777)
        await aioshutil.copyfile(src_path, sub_dir / file_path)
    except PermissionError:
        logging.debug(f"Couldn't copy {src_path} due to insufficient permissions.")
    except FileNotFoundError:
        if not await dest_path.exists():
            logging.debug(f"Destination path not found. Creating..")
            await dest_path.mkdir(parents=True, exist_ok=True)
            os.chmod(dest_path, mode=0o777)
    except aioshutil.SameFileError:
        err_message = f"""
            An attempt to copy a file that already exists {src_path}
            in the destination directory detected. Skipping operation..
            """.replace(
            "\n", " "
        )
        logging.error(err_message)
    except Exception as err:
        logging.error(f'"{err}" caught. Something went wrong.')


def draw_plot(results):
    results = {
        k: v for k, v in sorted(results.items(), key=lambda item: item[1], reverse=True)
    }
    ticks = range(len(results))
    x_labels = list(results.keys())
    y_labels = list(results.values())

    if len(results) > 10:
        ticks = range(10)
        x_labels = list(results.keys())[:10]
        y_labels = list(results.values())[:10]

    plt.bar(ticks, y_labels, align="center")
    plt.xticks(ticks, x_labels)

    plt.show()
