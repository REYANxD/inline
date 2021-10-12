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


import httpx
from bot import IMDB_SRCH_URL, DEF_AULT_NOSRCH_IMG
from .imdb import IMDb, IMDbResult


async def search_imd_b(search_query: str) -> IMDb:
    req_url = IMDB_SRCH_URL
    async with httpx.AsyncClient() as client:
        resp_one = await client.get(
            url=req_url,
            params={
                "q": search_query
            }
        )
    api_response = resp_one.json()
    imdb_src_resps = api_response.get("description")
    imdb_reslts = []
    for koda in imdb_src_resps:
        rating_ = koda.get("#RATING")
        user_rating = None
        if rating_:
            one = rating_.get("#ONLYRATING")
            two = rating_.get("#ONLYRATING")
            three = rating_.get("#NUMUSERRATINGS")
            user_rating = (
                f"⭐️ {one} / {two} (👀 {three})"
            )
        imdb_reslts.append(
            IMDbResult(
                koda.get("#IMDB_ID"),
                koda.get("#TITLE"),
                koda.get("#YEAR"),
                koda.get("#AKA"),
                koda.get("#IMDB_URL"),
                koda.get("#IMDB_IV"),
                koda.get("#ACTORS"),
                koda.get(
                    "#IMG_POSTER",
                    DEF_AULT_NOSRCH_IMG
                ),
                int(koda.get("photo_width", "640")),
                int(koda.get("photo_height", "640")),
                koda.get("#IMDb_TITLE_TYPE"),
                koda.get("#IMDb_SHORT_DESC"),
                koda.get("#MARINTG"),
                koda.get("#GENRE", []),
                user_rating
            )
        )
    return IMDb(
        api_response.get("ok"),
        api_response.get("error_code"),
        imdb_reslts
    )
