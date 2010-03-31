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
from tw.forms import SingleSelectField
from tw.forms.validators import All, Regex, NotEmpty, UnicodeString, MaxLength

# Language
class FormLanguageNew(TableForm):
    """New language form"""
    class fields(WidgetsList):
        language_id = TextField(validator=All(UnicodeString, NotEmpty,
                                                                MaxLength(3)))
        name = TextField(validator=All(UnicodeString, NotEmpty, MaxLength(50)))


class FormLanguageEdit(TableForm):
    """Edit language form"""
    class fields(WidgetsList):
        _method = HiddenField(default='PUT', validator=None)
        language_id = HiddenField(validator=NotEmpty)
        id_ = TextField(validator=None, disabled=True)
        name = TextField(validator=All(UnicodeString, NotEmpty, MaxLength(50)))


class FormLanguageDelete(TableForm):
    """Delete language confirmation form"""
    class fields(WidgetsList):
        _method = HiddenField(default='DELETE', validator=None)
        language_id = HiddenField(validator=NotEmpty)
        id_ = TextField(validator=None, disabled=True)
        name_ = TextField(validator=None, disabled=True)

# Category
class FormCategoryNew(TableForm):
    """New category form"""
    class fields(WidgetsList):
        name = TextField(validator=All(UnicodeString, NotEmpty, MaxLength(50)))
        description = TextArea(rows=10)


class FormCategoryEdit(TableForm):
    """Edit category form"""
    class fields(WidgetsList):
        _method = HiddenField(default='PUT', validator=None)
        category_id = HiddenField(validator=NotEmpty)
        id_ = TextField(validator=None, disabled=True)
        name = TextField(validator=All(UnicodeString, NotEmpty, MaxLength(50)))
        description = TextArea(rows=10)


class FormCategoryDelete(TableForm):
    """Delete category confirmation form"""
    class fields(WidgetsList):
        _method = HiddenField(default='DELETE', validator=None)
        category_id = HiddenField(validator=NotEmpty)
        id_ = TextField(validator=None, disabled=True)
        name_ = TextField(validator=None, disabled=True)


# Category
class FormArticleNew(TableForm):
    """New article form"""
    class fields(WidgetsList):
        category_id = SingleSelectField(label_text='category', size=10)
        language_id = SingleSelectField(label_text='language', size=10)
        title = TextField(size=44, validator=All(UnicodeString, NotEmpty, MaxLength(50)))
        text = TextArea(rows=20)


class FormArticleEdit(TableForm):
    """Edit article form"""
    class fields(WidgetsList):
        _method = HiddenField(default='PUT', validator=None)
        article_id = HiddenField(validator=NotEmpty)
        id_ = TextField(validator=None, disabled=True)
        title = TextField(validator=All(UnicodeString, NotEmpty, MaxLength(50)))
        category_id = SingleSelectField(label_text='category', size=10)
        language_id = SingleSelectField(label_text='language', size=10)
        text = TextArea(rows=30)


class FormArticleDelete(TableForm):
    """Delete article confirmation form"""
    class fields(WidgetsList):
        _method = HiddenField(default='DELETE', validator=None)
        article_id = HiddenField(validator=NotEmpty)
        id_ = TextField(validator=None, disabled=True)
        title_ = TextField(validator=None, disabled=True)



