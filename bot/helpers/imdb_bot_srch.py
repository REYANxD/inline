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


from telethon import Button, events, TelegramClient
from telethon.tl.types import (
    InputWebDocument,
    InputBotInlineResult
)
from bot import (
    SIQ_IM_OIC_POL,
    SIQ_IM_CIO_WND,
    TG_DERP_ID_ONE,
    TG_DERP_ID_TWO
)
from ..sessalc.search_imd_b import search_imd_b


async def search_imdb_in_line(
    _b: TelegramClient,
    event: events.InlineQuery.Event,
    sqr: str,
    astr: int,
    lmtn: int
):
    imdb_api_resps = await search_imd_b(sqr)
    search_results = []
    if imdb_api_resps.ok:
        for imdb_res in imdb_api_resps.description:
            if not imdb_res.imdb_id.startswith("tt"):
                # we only need movie titles,
                # not personalities
                continue
            mesg_capn = (
                f"<a href='{imdb_res.imdb_url}'>"
                f"{imdb_res.title} ({imdb_res.year})"
                "</a>"
            )
            conteent = InputWebDocument(
                url=imdb_res.photo_url.replace(
                    "._V1_",
                    # credits:
                    # https://github.com/iytdl/iytdl/blob/master/src/iytdl/sql_cache.py#L96
                    "._V1_UX1080"
                ),
                size=TG_DERP_ID_ONE,
                mime_type="image/jpeg",
                attributes=[]
            )
            thuumb = InputWebDocument(
                url=imdb_res.photo_url.replace(
                    "._V1_",
                    # credits:
                    # https://github.com/code-rgb/droid/blob/master/droid/modules/youtube.py#L154
                    "._V1_UX480"
                ),
                size=TG_DERP_ID_TWO,
                mime_type="image/jpeg",
                attributes=[]
            )
            
            search_results.append(
                InputBotInlineResult(
                    id=f"{imdb_res.imdb_id} {astr} {lmtn}",
                    type="photo",
                    send_message=await event.builder._message(
                        text=mesg_capn,
                        media=conteent,
                        buttons=[
                            Button.inline(
                                text=SIQ_IM_CIO_WND,
                                data=f"DRWN|{imdb_res.imdb_id}"
                            ),
                            Button.switch_inline(
                                text=SIQ_IM_OIC_POL,
                                query=sqr,
                                same_peer=True
                            )
                        ]
                    ),
                    title=imdb_res.aka,
                    description=imdb_res.imdb_title_type,
                    url=imdb_res.imdb_url,
                    thumb=thuumb,
                    content=conteent
                )
            )

    return search_results, len(search_results)
