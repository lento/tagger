# -*- coding: utf-8 -*-
#
# This file is part of Tagger.
#
# Tagger is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tagger is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Tagger.  If not, see <http://www.gnu.org/licenses/>.
#
# Original Copyright (c) 2010, Lorenzo Pierfederici <lpierfederici@gmail.com>
# Contributor(s): 
#
"""Helper functions for models"""

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from tagger.model import DBSession, Tag, TagData, Language, Page

def tags_from_string(s, create=True, lang=None):
    if lang is None:
        lang = DBSession.query(Language).first().id
    alltags = dict([(t.id, t) for t in DBSession.query(Tag)])
    alltagsdata = dict([(d.name, d) for d in DBSession.query(TagData)])
    tagnames = s and s.split(', ') or []
    tags = []
    for tagname in tagnames:
        if tagname in alltags:
            tag = alltags[tagname]
        elif tagname in alltagsdata:
            tag = alltagsdata[tagname].parent
        elif create:
            tag = Tag(tagname, lang)
            DBSession.add(tag)
        tags.append(tag)
    return tags

def get_page(pageid):
    """Return a page given its id or its article/string_id path"""
    try:
        if isinstance(pageid, int) or pageid.isdigit():
            page = DBSession.query(Page).get(pageid)
        elif '/' in pageid:
            articleid, pageid = pageid.split('/')
            query = DBSession.query(Page)
            query = query.filter_by(string_id=pageid, article_id=articleid)
            page = query.one()
        else:
            page = None
    except NoResultFound, MultipleResultsFound:
        page = None
    return page

