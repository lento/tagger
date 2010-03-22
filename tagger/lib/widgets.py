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
"""Custom widgets for tagger"""

import re
from tg import config, url
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from tw.api import Widget, WidgetsList
from tw.forms import TableForm, TextField, TextArea, HiddenField
from tw.forms import MultipleSelectField
from tw.forms.validators import Regex, NotEmpty

# Category
class FormCategoryNew(TableForm):
    """New category form"""
    class fields(WidgetsList):
        name = TextField(validator=NotEmpty)
        description = TextArea(rows=10)


class FormCategoryEdit(TableForm):
    """Edit tag form"""
    class fields(WidgetsList):
        _method = HiddenField(default='PUT', validator=None)
        category_id = HiddenField(validator=NotEmpty)
        id_ = TextField(validator=None, disabled=True)
        name = TextField(validator=NotEmpty)
        description = TextArea(rows=10)


class FormCategoryDelete(TableForm):
    """Delete tag confirmation form"""
    class fields(WidgetsList):
        _method = HiddenField(default='DELETE', validator=None)
        category_id = HiddenField(validator=NotEmpty)
        id_ = TextField(validator=None, disabled=True)
        name_ = TextField(validator=None, disabled=True)



