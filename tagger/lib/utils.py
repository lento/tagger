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
"""Tagger utilities"""

from operator import itemgetter
from sqlalchemy import desc
from tagger.model import DBSession, Associable, Tag

def find_related(tags=set(), obj=None, max_results=10):
    """Return a list of related objects

    Each element of the list is a tuple in the form:
    (object, number of tags in common, creation date of the object)
    """
    if obj:
        tags = set(obj.tags)
    tagids = [t.id for t in tags]
    query = DBSession.query(Associable)
    query = query.filter(Associable.tags.any(Tag.id.in_(tagids)))
    query = query.order_by(desc('created'))
    results = query.all()
    if obj:
        results.remove(obj.associable)
    results = [(o, len(set(o.tags) & tags)) for o in results]
    results.sort(key=itemgetter(1), reverse=True)
    if max_results > 0:
        return results[:max_results]
    else:
        return results

def find_recent(max_results=10):
    """Return a list of recent objects
    
    Each element of the list is a tuple in the form:
    (object, creation date of the object)
    """
    query = DBSession.query(Associable)
    query = query.order_by(desc('created'))
    if max_results > 0:
        query = query.limit(max_results)
    results = query.all()
    return results

