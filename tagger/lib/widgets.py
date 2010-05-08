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
from tw.forms import SingleSelectField, FileField, PasswordField
from tw.dynforms import CascadingSingleSelectField, HidingTableForm
from tw.dynforms import HidingSingleSelectField
from tw.forms.validators import All, Regex, NotEmpty, UnicodeString, MaxLength
from tw.forms.validators import OneOf, Email
from tagger.lib.render import media_types


TF_SIZE = 44    # TextField
TA_COLS = 50    # TextArea
TA_ROWS = 5
SF_SIZE = 10    # SelectField

############################################################
# Forms
############################################################

# Login
class FormLogin(TableForm):
    """Login form"""
    class fields(WidgetsList):
        came_from = HiddenField()
        logins = HiddenField()
        login = TextField(label_text=l_('User Name'))
        password = PasswordField(label_text=l_('Password'))


# Tag
class FormTagNew(TableForm):
    """New Tag form"""
    class fields(WidgetsList):
        languageid = SingleSelectField(label_text=l_('Language'), size=SF_SIZE)
        name = TextField(label_text=l_('Name'), size=TF_SIZE,
                        validator=All(UnicodeString, NotEmpty, MaxLength(255)))


class FormTagEdit(TableForm):
    """Edit Tag form"""
    class fields(WidgetsList):
        _method = HiddenField(default='PUT', validator=None)
        tagid = HiddenField(validator=NotEmpty)
        id_ = TextField(size=TF_SIZE, validator=None, disabled=True)
        languageid = CascadingSingleSelectField(label_text=l_('Language'),
                            size=SF_SIZE, cascadeurl=tg.url('/tag/translation'),
                            extra=['tagid'])
        name = TextField(label_text=l_('Name'), size=TF_SIZE,
                        validator=All(UnicodeString, NotEmpty, MaxLength(255)))


class FormTagDelete(TableForm):
    """Delete Tag confirmation form"""
    class fields(WidgetsList):
        _method = HiddenField(default='DELETE', validator=None)
        tagid = HiddenField(validator=NotEmpty)
        id_ = TextField(size=TF_SIZE, validator=None, disabled=True)


# Language
class FormLanguageNew(TableForm):
    """New language form"""
    class fields(WidgetsList):
        languageid = TextField(label_text='ID',
                        validator=All(UnicodeString, NotEmpty, MaxLength(5)))
        name = TextField(label_text=l_('Name'), size=TF_SIZE,
                        validator=All(UnicodeString, NotEmpty, MaxLength(50)))


class FormLanguageEdit(TableForm):
    """Edit language form"""
    class fields(WidgetsList):
        _method = HiddenField(default='PUT', validator=None)
        languageid = HiddenField(validator=NotEmpty)
        id_ = TextField(validator=None, disabled=True)
        name = TextField(label_text=l_('Name'), size=TF_SIZE,
                        validator=All(UnicodeString, NotEmpty, MaxLength(50)))


class FormLanguageDelete(TableForm):
    """Delete language confirmation form"""
    class fields(WidgetsList):
        _method = HiddenField(default='DELETE', validator=None)
        languageid = HiddenField(validator=NotEmpty)
        id_ = TextField(validator=None, disabled=True)
        name_ = TextField(label_text=l_('Name'), size=TF_SIZE, validator=None,
                                                                disabled=True)


# Category
class FormCategoryNew(TableForm):
    """New category form"""
    class fields(WidgetsList):
        languageid = SingleSelectField(label_text=l_('Language'), size=SF_SIZE)
        name = TextField(label_text=l_('Name'), size=TF_SIZE,
                        validator=All(UnicodeString, NotEmpty, MaxLength(50)))
        description = TextArea(label_text=l_('Description'), rows=TA_ROWS,
                                                                cols=TA_COLS)


class FormCategoryEdit(TableForm):
    """Edit category form"""
    class fields(WidgetsList):
        _method = HiddenField(default='PUT', validator=None)
        categoryid = HiddenField(validator=NotEmpty)
        id_ = TextField(size=TF_SIZE, validator=None, disabled=True)
        languageid = CascadingSingleSelectField(label_text=l_('Language'),
                        size=SF_SIZE, cascadeurl=tg.url('/category/translation'),
                        extra=['categoryid'])
        name = TextField(label_text=l_('Name'), size=TF_SIZE,
                        validator=All(UnicodeString, NotEmpty, MaxLength(50)))
        description = TextArea(label_text=l_('Description'), rows=TA_ROWS,
                                                                cols=TA_COLS)


class FormCategoryDelete(TableForm):
    """Delete category confirmation form"""
    class fields(WidgetsList):
        _method = HiddenField(default='DELETE', validator=None)
        categoryid = HiddenField(validator=NotEmpty)
        id_ = TextField(size=TF_SIZE, validator=None, disabled=True)
        name_ = TextField(label_text=l_('Name'), size=TF_SIZE, validator=None,
                                                                disabled=True)


# Article
class FormArticleNew(TableForm):
    """New article form"""
    class fields(WidgetsList):
        categoryid = SingleSelectField(label_text=l_('Category'), size=SF_SIZE)
        languageid = SingleSelectField(label_text=l_('Language'), size=SF_SIZE)
        title = TextField(label_text=l_('Title'), size=TF_SIZE,
                        validator=All(UnicodeString, NotEmpty, MaxLength(50)))
        text = TextArea(label_text=l_('Text'), rows=20, cols=TA_COLS)
        tagids = TextField(label_text=l_('Tags'), size=TF_SIZE,
                        attrs=dict(title=l_('Comma separated list of tags')))


class FormArticleEdit(TableForm):
    """Edit article form"""
    class fields(WidgetsList):
        _method = HiddenField(default='PUT', validator=None)
        articleid = HiddenField(validator=NotEmpty)
        id_ = TextField(size=TF_SIZE, validator=None, disabled=True)
        categoryid = SingleSelectField(label_text=l_('Category'), size=SF_SIZE)
        languageid = CascadingSingleSelectField(label_text=l_('Language'),
                        size=SF_SIZE, cascadeurl=url('/article/translation'),
                        extra=['articleid'])
        title = TextField(label_text=l_('Title'), size=TF_SIZE,
                        validator=All(UnicodeString, NotEmpty, MaxLength(50)))
        text = TextArea(label_text=l_('Text'), rows=20, cols=TA_COLS)
        tagids = TextField(label_text=l_('Tags'), size=TF_SIZE,
                        attrs=dict(title=l_('Comma separated list of tags')))


class FormArticleDelete(TableForm):
    """Delete article confirmation form"""
    class fields(WidgetsList):
        _method = HiddenField(default='DELETE', validator=None)
        articleid = HiddenField(validator=NotEmpty)
        id_ = TextField(size=TF_SIZE, validator=None, disabled=True)
        title_ = TextField(label_text=l_('Title'), size=TF_SIZE, validator=None,
                                                                disabled=True)


# Link
class FormLinkNew(TableForm):
    """New link form"""
    class fields(WidgetsList):
        uri = TextField(label_text='URI', size=TF_SIZE,
                        validator=All(UnicodeString, NotEmpty, MaxLength(255)))
        languageid = SingleSelectField(label_text=l_('Language'), size=SF_SIZE)
        name = TextField(label_text=l_('Name'), size=TF_SIZE,
                        validator=All(UnicodeString, NotEmpty, MaxLength(255)))
        description = TextArea(label_text=l_('Description'), rows=TA_ROWS,
                                                                cols=TA_COLS)
        tagids = TextField(label_text=l_('Tags'), size=TF_SIZE,
                        attrs=dict(title=l_('Comma separated list of tags')))


class FormLinkEdit(TableForm):
    """Edit link form"""
    class fields(WidgetsList):
        _method = HiddenField(default='PUT', validator=None)
        linkid = HiddenField(validator=NotEmpty)
        id_ = TextField(size=TF_SIZE, validator=None, disabled=True)
        uri = TextField(label_text='URI', size=TF_SIZE,
                        validator=All(UnicodeString, NotEmpty, MaxLength(255)))
        languageid = CascadingSingleSelectField(label_text=l_('Language'),
                        size=SF_SIZE, cascadeurl=tg.url('/link/translation'),
                        extra=['linkid'])
        name = TextField(label_text=l_('Name'), size=TF_SIZE,
                        validator=All(UnicodeString, NotEmpty, MaxLength(255)))
        description = TextArea(label_text=l_('Description'), rows=TA_ROWS,
                                                                cols=TA_COLS)
        tagids = TextField(label_text=l_('Tags'), size=TF_SIZE,
                        attrs=dict(title=l_('Comma separated list of tags')))


class FormLinkDelete(TableForm):
    """Delete link confirmation form"""
    class fields(WidgetsList):
        _method = HiddenField(default='DELETE', validator=None)
        linkid = HiddenField(validator=NotEmpty)
        id_ = TextField(size=TF_SIZE, validator=None, disabled=True)
        uri_ = TextField(label_text='URI', size=TF_SIZE, validator=None,
                                                                disabled=True)


# Media
class FormMediaNew(HidingTableForm):
    """New media form"""
    class fields(WidgetsList):
        mediatype = HidingSingleSelectField(label_text=l_('Type'), size=SF_SIZE,
            options=[''] + media_types,
            mapping={'image': ['uploadfile'],
                     'video': ['uploadfile', 'fallbackfile'],
                     'youtube': ['uri'],
                     'vimeo': ['uri'],
                    },
            validator=All(NotEmpty, OneOf(media_types)),
        )
        uri = TextField(label_text='URI', size=TF_SIZE,
                                validator=All(UnicodeString, MaxLength(255)))
        uploadfile = FileField(label_text=l_('File to upload'))
        fallbackfile = FileField(label_text=l_('Fallback file'))

        languageid = SingleSelectField(label_text=l_('Language'), size=SF_SIZE)
        name = TextField(label_text=l_('Name'), size=TF_SIZE,
                        validator=All(UnicodeString, NotEmpty, MaxLength(255)))
        description = TextArea(label_text=l_('Description'), rows=TA_ROWS,
                                                                cols=TA_COLS)
        tagids = TextField(label_text=l_('Tags'), size=TF_SIZE,
                        attrs=dict(title=l_('Comma separated list of tags')))


class FormMediaEdit(TableForm):
    """Edit media form"""
    class fields(WidgetsList):
        _method = HiddenField(default='PUT', validator=None)
        mediaid = HiddenField(validator=NotEmpty)
        id_ = TextField(size=TF_SIZE, validator=None, disabled=True)
        mediatype_ = TextField(label_text=l_('Type'), size=TF_SIZE,
                                                validator=None, disabled=True)
        uri = TextField(label_text='URI', size=TF_SIZE,
                                validator=All(UnicodeString, MaxLength(255)))
        languageid = CascadingSingleSelectField(label_text=l_('Language'),
                        size=SF_SIZE, cascadeurl=tg.url('/media/translation'),
                        extra=['mediaid'])
        name = TextField(label_text=l_('Name'), size=TF_SIZE,
                        validator=All(UnicodeString, NotEmpty, MaxLength(255)))
        description = TextArea(label_text=l_('Description'), rows=TA_ROWS,
                                                                cols=TA_COLS)
        tagids = TextField(label_text=l_('Tags'), size=TF_SIZE,
                        attrs=dict(title=l_('Comma separated list of tags')))


class FormMediaDelete(TableForm):
    """Delete media confirmation form"""
    class fields(WidgetsList):
        _method = HiddenField(default='DELETE', validator=None)
        mediaid = HiddenField(validator=NotEmpty)
        id_ = TextField(size=TF_SIZE, validator=None, disabled=True)
        mediatype_ = TextField(label_text=l_('Type'), size=TF_SIZE,
                                                validator=None, disabled=True)
        uri_ = TextField(label_text='URI', size=TF_SIZE, validator=None,
                                                                disabled=True)


# Comment
class FormCommentNew(TableForm):
    """New comment form"""
    class fields(WidgetsList):
        came_from = HiddenField(validator=NotEmpty)
        associableid = HiddenField(validator=NotEmpty)
        name = TextField(label_text=l_('Name'), size=TF_SIZE,
                        validator=All(UnicodeString, NotEmpty, MaxLength(255)))
        email = TextField(label_text=l_('E-Mail'), size=TF_SIZE,
                        validator=All(Email, NotEmpty))
        text = TextArea(label_text=l_('Text'), rows=TA_ROWS, cols=TA_COLS)


class FormCommentEdit(TableForm):
    """Edit comment form"""
    class fields(WidgetsList):
        _method = HiddenField(default='PUT', validator=None)
        commentid = HiddenField(validator=NotEmpty)
        id_ = TextField(size=TF_SIZE, validator=None, disabled=True)
        date_ = TextField(label_text=l_('Date'), size=TF_SIZE, validator=None,
                                                                disabled=True)
        to_ = TextField(label_text=l_('To'), size=TF_SIZE, validator=None,
                                                                disabled=True)
        name = TextField(label_text=l_('Name'), size=TF_SIZE,
                        validator=All(UnicodeString, NotEmpty, MaxLength(255)))
        email = TextField(label_text=l_('E-Mail'), size=TF_SIZE,
                        validator=All(Email, NotEmpty))
        text = TextArea(label_text=l_('Text'), rows=TA_ROWS, cols=TA_COLS)


class FormCommentDelete(TableForm):
    """Delete comment confirmation form"""
    class fields(WidgetsList):
        _method = HiddenField(default='DELETE', validator=None)
        commentid = HiddenField(validator=NotEmpty)
        id_ = TextField(size=TF_SIZE, validator=None, disabled=True)
        date_ = TextField(label_text=l_('Date'), size=TF_SIZE, validator=None,
                                                                disabled=True)
        to_ = TextField(label_text=l_('To'), size=TF_SIZE, validator=None,
                                                                disabled=True)
        name_ = TextField(label_text=l_('Name'), size=TF_SIZE, validator=None,
                                                                disabled=True)
        text_ = TextArea(label_text=l_('Text'), rows=TA_ROWS, cols=TA_COLS,
                                                validator=None, disabled=True)


# Settings
class FormSettings(TableForm):
    """Edit Settings form"""
    class fields(WidgetsList):
        n_banner_media = HiddenField(name='name', default='banner_media')
        v_banner_media = SingleSelectField(label_text=l_('Banner Media'),
                                                    name='value', size=SF_SIZE)
        n_banner_link = HiddenField(name='name', default='banner_link')
        v_banner_link = SingleSelectField(label_text=l_('Banner Link'),
                                                    name='value', size=SF_SIZE)


############################################################
# Sidebar widgets
############################################################

class SideArticle(Widget):
    """Show a article summary in the sidebar"""
    params = ['article']
    template = 'mako:tagger.templates.widgets.side_article'


class SideMedia(Widget):
    """Show a media summary in the sidebar"""
    params = ['media']
    template = 'mako:tagger.templates.widgets.side_media'


class SideLink(Widget):
    """Show a link summary in the sidebar"""
    params = ['link']
    template = 'mako:tagger.templates.widgets.side_link'


############################################################
# Misc widgets
############################################################

class ObjectTitle(Widget):
    """Show a object title"""
    params = ['obj', 'lang', 'add_link']
    template = 'mako:tagger.templates.widgets.object_title'

    add_link = False

