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


from telethon import Button, TelegramClient
from bot import (
    TG_DUMP_CHAT_S
)
from .human_bytes import humanbytes


async def search_tg(
    _u: TelegramClient,
    sqr: str,
    astr: int,
    lmtn: int,
    is_inline: bool = False
):
    TG_DB_CHAT = TG_DUMP_CHAT_S[0]
    t_r = 0  # mtls.total
    search_results = []
    __tmp_id_s = []
    mtls = 0
    async for mt_ls in _u.iter_messages(
        entity=TG_DB_CHAT,
        limit=lmtn,
        offset_id=astr,
        search=sqr
    ):
        mtls = mt_ls.id
        if mt_ls.id in __tmp_id_s:
            continue
        sltm = mt_ls
        if sltm and sltm.reply_to_msg_id:
            __tmp_id_s.append(sltm.id)
            sltm = await sltm.get_reply_message()
        if (
            sltm and
            sltm.document
        ):
            description = sltm.raw_text.split(
                "\n"
            )[0]
            if (
                "#ID_" in description or
                description == ""
            ):
                description = sltm.file.name
            hfs = humanbytes(sltm.file.size)
            cb_strt_dta = "tgfs"
            if is_inline:
                cb_strt_dta = "igfs"
            search_results.append(
                [
                    Button.inline(
                        text=f"{hfs} | {description}",
                        data=f"{cb_strt_dta}|{sltm.id}|{astr}|{lmtn}"
                    )
                ]
            )
            __tmp_id_s.append(sltm.id)
    return search_results, mtls, t_r
