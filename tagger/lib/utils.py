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
from tagger.model import DBSession, Associable, Tag

def find_related(tags, max_results=10):
    """Return a list of related objects

    Each element of the list is a tuple in the form:
    (object, number of tags in common, creation date of the object)
    """
    tags = isinstance(tags, set) and tags or set(tags)
    tagids = [t.id for t in tags]
    query = DBSession.query(Associable)
    query = query.filter(Associable.tags.any(Tag.id.in_(tagids)))
    results = query.all()
    results = [(o, len(set(o.tags) & tags), o.associated.created)
                                                            for o in results]
    results.sort(key=itemgetter(1, 2), reverse=True)
    if max_results > 0:
        return results[:max_results]
    else:
        return results


