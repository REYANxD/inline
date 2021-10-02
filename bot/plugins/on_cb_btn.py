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


from telethon import events, Button
from bot import (
    BOT,
    LOGGER,
    ONCB_BTN_MOSHANAM_TEXT,
    PLEASE_WAIT_TEXT,
    PM_MEDIA_CAPTION,
    SPT_SRCHTGSBR_TEXT,
    TG_DUMP_CHAT_S
)
from bot.sessalc.search_imd_b import search_imd_b
from bot.helpers.telegram_user_search import (
    search_tg
)


@BOT.on(
    events.CallbackQuery
)
async def _(evt: events.CallbackQuery.Event):
    # NOTE: You should always answer,
    # but we want different conditionals to
    # be able to answer to differnetly
    # (and we can only answer once),
    # so we don't always answer here.
    # from_user_id = callback_query.from_user.id

    cb_data = evt.data.decode("UTF-8")

    if cb_data.startswith("DRWN|"):
        _, imdb_id = cb_data.split("|")
        imdb_response = await search_imd_b(imdb_id)
        if imdb_response.ok:
            try:
                imdb_result = imdb_response.description[0]
                await evt.answer(
                    message=PLEASE_WAIT_TEXT,
                    alert=False
                )
                search_query = f"{imdb_result.title} {imdb_result.year}"
                mesg_capn = (
                    f"<a href='{imdb_result.imdb_url}'>"
                    f"{imdb_result.title} ({imdb_result.year})"
                    "</a>"
                )
                start_at, limit = 0, 9

                search_results, next_offset, rtbt = await search_tg(
                    evt.client.USER,
                    search_query,
                    start_at,
                    limit,
                    is_inline=True
                )
                # LOGGER(__name__).info(search_results)
                next_page_number = start_at + 1
                # if len(search_results) == limit:
                #     search_results.append(
                #         [
                #             Button.inline(
                #                 text=NEXT_PAGE_BUTTON_TEXT,
                #                 data=f"nfs|{next_offset}|{next_page_number}|{limit}"
                #             )
                #         ]
                #     )
                # LOGGER(__name__).info(search_results)
                await evt.edit(
                    buttons=search_results
                )

            except IndexError:
                await evt.answer(
                    message=SPT_SRCHTGSBR_TEXT,
                    alert=True
                )
        else:
            await evt.answer(
                message=SPT_SRCHTGSBR_TEXT,
                alert=True
            )
    
    elif cb_data.startswith("igfs|"):
        await evt.answer(
            message=PLEASE_WAIT_TEXT,
            alert=False
        )
        _, message_id, _, _ = cb_data.split("|")
        message_id = int(message_id)
        TG_DB_CHAT = TG_DUMP_CHAT_S[0]
        required_message = await evt.client.get_messages(
            entity=TG_DB_CHAT,
            ids=message_id
        )
        await evt.edit(
            text=PM_MEDIA_CAPTION,
            file=required_message.media,
            buttons=[
                Button.inline(
                    text="go back",
                    data=evt.data
                )
            ]
        )

    else:
        await evt.answer(
            message=ONCB_BTN_MOSHANAM_TEXT,
            alert=False
        )
