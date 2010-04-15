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
import tg
from tg import config, url
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from tw.api import Widget, WidgetsList
from tw.forms import TableForm, TextField, TextArea, HiddenField
from tw.forms import SingleSelectField, FileField
from tw.dynforms import CascadingSingleSelectField, HidingTableForm
from tw.dynforms import HidingSingleSelectField
from tw.forms.validators import All, Regex, NotEmpty, UnicodeString, MaxLength
from tw.forms.validators import OneOf
from tagger.lib.render import media_types


############################################################
# Forms
############################################################

# Language
class FormLanguageNew(TableForm):
    """New language form"""
    class fields(WidgetsList):
        languageid = TextField(validator=All(UnicodeString, NotEmpty,
                                                                MaxLength(3)))
        name = TextField(validator=All(UnicodeString, NotEmpty, MaxLength(50)))


class FormLanguageEdit(TableForm):
    """Edit language form"""
    class fields(WidgetsList):
        _method = HiddenField(default='PUT', validator=None)
        languageid = HiddenField(validator=NotEmpty)
        id_ = TextField(validator=None, disabled=True)
        name = TextField(validator=All(UnicodeString, NotEmpty, MaxLength(50)))


class FormLanguageDelete(TableForm):
    """Delete language confirmation form"""
    class fields(WidgetsList):
        _method = HiddenField(default='DELETE', validator=None)
        languageid = HiddenField(validator=NotEmpty)
        id_ = TextField(validator=None, disabled=True)
        name_ = TextField(validator=None, disabled=True)


# Category
class FormCategoryNew(TableForm):
    """New category form"""
    class fields(WidgetsList):
        languageid = SingleSelectField(label_text=_('Language'), size=10)
        name = TextField(validator=All(UnicodeString, NotEmpty, MaxLength(50)))
        description = TextArea(rows=10)


class FormCategoryEdit(TableForm):
    """Edit category form"""
    class fields(WidgetsList):
        _method = HiddenField(default='PUT', validator=None)
        categoryid = HiddenField(validator=NotEmpty)
        id_ = TextField(validator=None, disabled=True)
        languageid = CascadingSingleSelectField(label_text=_('Language'),
                            size=10, cascadeurl=tg.url('/category/translation'),
                            extra=['categoryid'])
        name = TextField(validator=All(UnicodeString, NotEmpty, MaxLength(50)))
        description = TextArea(rows=10)


class FormCategoryDelete(TableForm):
    """Delete category confirmation form"""
    class fields(WidgetsList):
        _method = HiddenField(default='DELETE', validator=None)
        categoryid = HiddenField(validator=NotEmpty)
        id_ = TextField(validator=None, disabled=True)
        name_ = TextField(validator=None, disabled=True)


# Article
class FormArticleNew(TableForm):
    """New article form"""
    class fields(WidgetsList):
        categoryid = SingleSelectField(label_text=_('Category'), size=10)
        languageid = SingleSelectField(label_text=_('Language'), size=10)
        title = TextField(size=44, validator=All(UnicodeString, NotEmpty,
                                                                MaxLength(50)))
        text = TextArea(id='text', rows=20)


class FormArticleEdit(TableForm):
    """Edit article form"""
    class fields(WidgetsList):
        _method = HiddenField(default='PUT', validator=None)
        articleid = HiddenField(validator=NotEmpty)
        id_ = TextField(validator=None, disabled=True)
        categoryid = SingleSelectField(label_text=_('Category'), size=10)
        languageid = CascadingSingleSelectField(label_text=_('Language'),
                    size=10, cascadeurl=url('/article/translation'), extra=['articleid'])
        title = TextField(size=44, validator=All(UnicodeString, NotEmpty,
                                                                MaxLength(50)))
        text = TextArea(rows=30)


class FormArticleDelete(TableForm):
    """Delete article confirmation form"""
    class fields(WidgetsList):
        _method = HiddenField(default='DELETE', validator=None)
        articleid = HiddenField(validator=NotEmpty)
        id_ = TextField(validator=None, disabled=True)
        title_ = TextField(validator=None, disabled=True)


# Link
class FormLinkNew(TableForm):
    """New link form"""
    class fields(WidgetsList):
        uri = TextField(validator=All(UnicodeString, NotEmpty, MaxLength(255)))
        languageid = SingleSelectField(label_text=_('Language'), size=10)
        name = TextField(label_text=l_('Name'),
                        validator=All(UnicodeString, NotEmpty, MaxLength(255)))
        description = TextArea(rows=10)


class FormLinkEdit(TableForm):
    """Edit link form"""
    class fields(WidgetsList):
        _method = HiddenField(default='PUT', validator=None)
        linkid = HiddenField(validator=NotEmpty)
        id_ = TextField(validator=None, disabled=True)
        uri = TextField(validator=All(UnicodeString, NotEmpty, MaxLength(255)))
        languageid = CascadingSingleSelectField(label_text=_('Language'),
                            size=10, cascadeurl=tg.url('/link/translation'),
                            extra=['linkid'])
        name = TextField(label_text=l_('Name'),
                        validator=All(UnicodeString, NotEmpty, MaxLength(255)))
        description = TextArea(rows=10)


class FormLinkDelete(TableForm):
    """Delete link confirmation form"""
    class fields(WidgetsList):
        _method = HiddenField(default='DELETE', validator=None)
        linkid = HiddenField(validator=NotEmpty)
        id_ = TextField(validator=None, disabled=True)
        uri_ = TextField(validator=None, disabled=True)


# Media
class FormMediaNew(HidingTableForm):
    """New media form"""
    class fields(WidgetsList):
        mediatype = HidingSingleSelectField(label_text=l_('Type'), size=10,
            options=[''] + media_types,
            mapping={'image': ['uploadfile'],
                     'video': ['uploadfile', 'fallbackfile'],
                     'youtube': ['uri'],
                     'vimeo': ['uri'],
                    },
            validator=All(NotEmpty, OneOf(media_types)),
        )
        uri = TextField(label_text=l_('URI'),
                                validator=All(UnicodeString, MaxLength(255)))
        uploadfile = FileField(label_text=l_('File to upload'))
        fallbackfile = FileField(label_text=l_('Fallback file'))

        languageid = SingleSelectField(label_text=l_('Language'), size=10)
        name = TextField(label_text=l_('Name'),
                        validator=All(UnicodeString, NotEmpty, MaxLength(255)))
        description = TextArea(rows=10)


class FormMediaEdit(TableForm):
    """Edit media form"""
    class fields(WidgetsList):
        _method = HiddenField(default='PUT', validator=None)
        mediaid = HiddenField(validator=NotEmpty)
        id_ = TextField(validator=None, disabled=True)
        mediatype_ = TextField(label_text=l_('Type'), validator=None,
                                                                disabled=True)
        uri = TextField(label_text=l_('URI'),
                                validator=All(UnicodeString, MaxLength(255)))
        languageid = CascadingSingleSelectField(label_text=l_('Language'),
                            size=10, cascadeurl=tg.url('/media/translation'),
                            extra=['mediaid'])
        name = TextField(label_text=l_('Name'),
                        validator=All(UnicodeString, NotEmpty, MaxLength(255)))
        description = TextArea(label_text=l_('Description'), rows=10)


class FormMediaDelete(TableForm):
    """Delete media confirmation form"""
    class fields(WidgetsList):
        _method = HiddenField(default='DELETE', validator=None)
        mediaid = HiddenField(validator=NotEmpty)
        id_ = TextField(validator=None, disabled=True)
        mediatype_ = TextField(label_text=l_('Type'), validator=None,
                                                                disabled=True)
        uri_ = TextField(label_text=l_('URI'), validator=None, disabled=True)

