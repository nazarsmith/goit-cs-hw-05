import asyncio
import aiopath

# import logging
import os

from models.models import parser
from utils.utils import read_folder, logging


async def main():
    args = parser.parse_args()
    a_source, a_destination = aiopath.AsyncPath(args.source[0]), aiopath.AsyncPath(
        args.destination[0]
    )
    if not await a_destination.exists():
        os.mkdir(a_destination)

    await read_folder(a_source, a_destination)


if __name__ == "__main__":

    logging.info("Running Sorter")
    asyncio.run(main())
    logger = logging.getLogger("Sorter")
