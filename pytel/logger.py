# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >.

from datetime import date
from logging import (
    Handler,
    CRITICAL,
    ERROR,
    DEBUG,
    WARNING,
    disable,
    getLogger,
    basicConfig,
    LogRecord,
    currentframe,
    __file__,
)
from sys import stderr
from typing import Union
from loguru import logger as pylog

pylog.remove(0)
pylog.add(
    sink="logs/pytel-{}.log".format(date.today().strftime("%Y-%m-%d")),
    format="{time:YY/MM/DD HH:mm:ss} | {level: <8}| {name: ^15} | {function: ^15} | {line: >3} : {message}",
    rotation="1 days",
    backtrace=True,
    diagnose=True,
)
pylog.add(
    stderr,
    format="<green>{time:YY/MM/DD HH:mm:ss}</green> | <yellow>{level}</yellow> | {name}:{function}:{line} | {message}",
    level="INFO",
    colorize=True,
)
pylog.opt(lazy=True, colors=True)


class InterceptHandler(Handler):
    """
    param record: record to logs.
    """

    def emit(self, record: LogRecord) -> None:
        try:
            level: Union[str, int] = pylog.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = (
            currentframe(),
            2,
        )
        while frame and frame.f_code.co_filename == __file__:
            frame = frame.f_back  # type: ignore
            depth += 1
        pylog.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


disable(DEBUG)
getLogger("asyncio").setLevel(ERROR)
getLogger("pyrogram").setLevel(ERROR)
getLogger("pyrogram.client").setLevel(WARNING)
getLogger("pyrogram.session.auth").setLevel(CRITICAL)
getLogger("pyrogram.session.session").setLevel(CRITICAL)
getLogger("pytgcalls").setLevel(ERROR)
getLogger("tgcalls").setLevel(ERROR)

getLogger("urllib3").disabled = True
getLogger("urllib3.connectionpool").disabled = True
getLogger("io").disabled = True

basicConfig(handlers=[InterceptHandler()], level=0, force=True)
