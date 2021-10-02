#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
#  GetSongsBot
#  Copyright (C) 2021 The Authors

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.

#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.


""" init """

# the logging things
import logging
import sys
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from .get_config import get_config


# the secret configuration specific things
# apparently, no error appears even if the path does not exists
try:
    load_dotenv(sys.argv[1])
except IndexError:
    load_dotenv("config.env")


# TODO: is there a better way?

# The Telegram API things
APP_ID = get_config("APP_ID", should_prompt=True)
API_HASH = get_config("API_HASH", should_prompt=True)
# Get these values from my.telegram.org
TG_BOT_TOKEN = get_config("TG_BOT_TOKEN", should_prompt=True)
TG_USER_SESSION = get_config("TG_USER_SESSION", should_prompt=True)
# search chat id
TG_DUMP_CHAT_S = [
    int(get_config("TG_DUMP_CHAT", should_prompt=True))
]
TG_BOT_SESSION = get_config("TG_BOT_SESSION", "bot")
# maximum message length in Telegram
MAX_MESSAGE_LENGTH = int(get_config("MAX_MESSAGE_LENGTH", "4096"))
# path to store log files
LOG_FILE_ZZGEVC = get_config("LOG_FILE_ZZGEVC")
# additional, optional configurations
TG_INLINE_SRCH_CACHE_TIME = int(
    get_config(
        "TG_INLINE_SRCH_CACHE_TIME",
        "300"
    )
)
TG_INLINE_SRCH_NUM_RESULTS = int(
    get_config(
        "TG_INLINE_SRCH_NUM_RESULTS",
        "9"
    )
)
# strings
PLZ_RATE_TEXT = get_config("PLZ_RATE_TEXT")
START_TEXT = get_config("START_TEXT")
LEGAL_DISCLAIMER_TEXT = get_config("LEGAL_DISCLAIMER_TEXT")
TG_SHARE_TEXT = get_config("TG_SHARE_TEXT")
SIQ_CC_TEXT = get_config("SIQ_CC_TEXT")
SIQ_TEXT = get_config("SIQ_TEXT")
STB_WURF_TEXT = get_config("STB_WURF_TEXT")
SPT_NTOIQ_TEXT = get_config("SPT_NTOIQ_TEXT")
SPT_YSEQI_TEXT = get_config("SPT_YSEQI_TEXT")
SPT_SRCHTGSBR_TEXT = get_config("SPT_SRCHTGSBR_TEXT")
ONCB_BTN_MOSHANAM_TEXT = get_config("ONCB_BTN_MOSHANAM_TEXT")
SIQ_IM_OIC_POL = get_config("SIQ_IM_OIC_POL")
# additional, optional strings
IMDB_SRCH_URL = get_config("IMDB_SRCH_URL")
DEF_AULT_NOSRCH_IMG = get_config("DEF_AULT_NOSRCH_IMG")
SIQ_IM_CIO_WND = get_config("SIQ_IM_CIO_WND")
TG_DERP_ID_ONE = int(get_config("TG_DERP_ID_ONE", "X"))
TG_DERP_ID_TWO = int(get_config("TG_DERP_ID_TWO", "Y"))
PLEASE_WAIT_TEXT = get_config("PLEASE_WAIT_TEXT")
PM_MEDIA_CAPTION = get_config("PM_MEDIA_CAPTION", " ")


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_ZZGEVC,
            maxBytes=20480,
            backupCount=1
        ),
        logging.StreamHandler()
    ]
)


def LOGGER(name: str) -> logging.Logger:
    """ get a Logger object """
    return logging.getLogger(name)


# hack :\
TG_BOT_ID = int(TG_BOT_TOKEN.split(":")[0])


from bot.bot import Bot  # noqa: E402
BOT = Bot()
