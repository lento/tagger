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
"""Functional test suite for the root controller"""

from nose.tools import assert_true, eq_

from tagger.tests import TestController
from tagger.model import DBSession, User, Language, Tag, Category, Article
from tagger.model import Media, Link, Comment, BannerContent
import transaction


class TestAdminController(TestController):
    """Tests for the method in the admin controller."""

    def _fill_db(self):
        tadm = DBSession.query(User).filter_by(user_name=u'test_admin').one()
        language = Language(u'xx', u'test language')
        DBSession.add(language)
        DBSession.flush()
        languageid = language.id
        return languageid, tadm

    def test_index(self):
        """controllers.admin.Controller.index is working properly"""
        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/admin', extra_environ=environ, status=200)

    def test_language(self):
        """controllers.admin.Controller.language is working properly"""
        languageid, tadm = self._fill_db()
        transaction.commit()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/admin/language', extra_environ=environ,
                                                                    status=200)
        
        tr = response.html.table.find('tr', languageid)
        eq_(str(tr('td')[0]), '<td>%s</td>' % languageid)
        eq_(str(tr('td')[1]), '<td>test language</td>')
        actions = tr('td')[2]
        eq_(str(actions('a')[0]['class']), 'icon edit overlay')
        eq_(str(actions('a')[1]['class']), 'icon delete overlay')

    def test_tag(self):
        """controllers.admin.Controller.tag is working properly"""
        languageid, tadm = self._fill_db()
        tag = Tag(u'test tag', u'xx')
        DBSession.add(tag)
        DBSession.flush()
        tagid = tag.id
        transaction.commit()
        
        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/admin/tag/', extra_environ=environ,
                                                                    status=200)

        tr = response.html.table('tr')[1]
        eq_(str(tr('td')[0]), '<td>%s</td>' % tagid)
        eq_(str(tr('td')[1]), '<td>test tag</td>')
        eq_(str(tr('td')[2]), '<td>%s</td>' % languageid)
        actions = tr('td')[3]
        eq_(str(actions('a')[0]['class']), 'icon edit overlay')
        eq_(str(actions('a')[1]['class']), 'icon delete overlay')

    def test_category(self):
        """controllers.admin.Controller.category is working properly"""
        languageid, tadm = self._fill_db()
        category = Category(u'test category', u'xx', u'a test category')
        DBSession.add(category)
        DBSession.flush()
        categoryid = category.id
        transaction.commit()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/admin/category/', extra_environ=environ,
                                                                    status=200)
        
        tr = response.html.table.find('tr', categoryid)
        eq_(str(tr('td')[0]), '<td>%s</td>' % categoryid)
        eq_(str(tr('td')[1]), '<td>test category</td>')
        eq_(str(tr('td')[2]), '<td>a test category</td>')
        eq_(str(tr('td')[3]), '<td>%s</td>' % languageid)
        actions = tr('td')[4]
        eq_(str(actions('a')[0]['class']), 'icon edit overlay')
        eq_(str(actions('a')[1]['class']), 'icon delete overlay')

    def test_article(self):
        """controllers.admin.Controller.article is working properly"""
        languageid, tadm = self._fill_db()
        cat = Category(u'test_category', u'xx')
        DBSession.add(cat)
        article = Article(u'A Test Article!', cat, u'xx', tadm, u'random text')
        DBSession.add(article)
        DBSession.flush()
        categoryid = cat.id
        articleid = article.id
        transaction.commit()

        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/admin/article/', extra_environ=environ,
                                                                    status=200)

        tr = response.html.table.find('tr', articleid)
        # Date
        eq_(str(tr('td')[1]), '<td>test_category</td>')
        eq_(str(tr('td')[2]), '<td>%s</td>' % articleid)
        eq_(str(tr('td')[3]), '<td>A Test Article!</td>')
        eq_(str(tr('td')[4]), '<td></td>')
        eq_(str(tr('td')[5]), '<td>%s</td>' % languageid)
        # Status
        actions = tr('td')[7]
        eq_(str(actions('a')[0]['class']), 'icon edit')
        eq_(str(actions('a')[1]['class']), 'icon delete overlay')
        eq_(str(actions('a')[2]['class']), 'icon publish')

    def test_media(self):
        """controllers.admin.Controller.media is working properly"""
        languageid, tadm = self._fill_db()
        media = Media(u'image', u'test image', u'/test.png', tadm, u'xx',
                                                                u'random text')
        DBSession.add(media)
        DBSession.flush()
        mediaid = media.id
        transaction.commit()
        
        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/admin/media/', extra_environ=environ,
                                                                    status=200)

        tr = response.html.table('tr')[1]
        eq_(str(tr('td')[0]), '<td>%s</td>' % mediaid)
        eq_(str(tr('td')[1]), '<td>image</td>')
        eq_(str(tr('td')[2]), '<td>test image</td>')
        eq_(str(tr('td')[3]), '<td>/test.png</td>')
        eq_(str(tr('td')[4]), '<td></td>')
        eq_(str(tr('td')[5]), '<td>%s</td>' % languageid)
        actions = tr('td')[6]
        eq_(str(actions('a')[0]['class']), 'icon edit overlay')
        eq_(str(actions('a')[1]['class']), 'icon delete overlay')

    def test_link(self):
        """controllers.admin.Controller.link is working properly"""
        languageid, tadm = self._fill_db()
        link = Link(u'test link', u'http://example.com', tadm, u'xx',
                                                                u'random text')
        DBSession.add(link)
        DBSession.flush()
        linkid = link.id
        transaction.commit()
        
        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/admin/link/', extra_environ=environ,
                                                                    status=200)

        tr = response.html.table('tr')[1]
        eq_(str(tr('td')[0]), '<td>%s</td>' % linkid)
        eq_(str(tr('td')[1]), '<td>test link</td>')
        eq_(str(tr('td')[2]), '<td>http://example.com</td>')
        eq_(str(tr('td')[3]), '<td></td>')
        eq_(str(tr('td')[4]), '<td>%s</td>' % languageid)
        actions = tr('td')[5]
        eq_(str(actions('a')[0]['class']), 'icon edit overlay')
        eq_(str(actions('a')[1]['class']), 'icon delete overlay')


    def test_comment(self):
        """controllers.admin.Controller.comment is working properly"""
        languageid, tadm = self._fill_db()
        comment = Comment(u'anonymous', u'anonym@example.com', u'test comment')
        DBSession.add(comment)
        DBSession.flush()
        commentid = comment.id
        transaction.commit()
        
        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/admin/comment/', extra_environ=environ,
                                                                    status=200)

        tr = response.html.table('tr')[1]
        # Date
        eq_(str(tr('td')[1]), '<td>%s</td>' % commentid)
        eq_(str(tr('td')[2]), '<td></td>')
        eq_(str(tr('td')[3]), '<td>anonymous</td>')
        eq_(str(tr('td')[4]), '<td>anonym@example.com</td>')
        eq_(str(tr('td')[5]), '<td>test comment</td>')
        # Status
        actions = tr('td')[7]
        eq_(str(actions('a')[0]['class']), 'icon edit overlay')
        eq_(str(actions('a')[1]['class']), 'icon delete overlay')
        eq_(str(actions('a')[2]['class']), 'icon approve')
        eq_(str(actions('a')[3]['class']), 'icon spam')

    def test_banner(self):
        """controllers.admin.Controller.banner is working properly"""
        
        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.get('/admin/banner/', extra_environ=environ,
                                                                    status=200)

        eq_(response.html.form['action'], u'/admin/banner_set')
        eq_(response.html.form['method'], u'post')
        assert_true(response.html.find('select', {'name': 'mediaid'}),
                                        '"mediaid" select element not found')
        assert_true(response.html.find('select', {'name': 'linkid'}),
                                        '"linkid" select element not found')

    def test_banner_set(self):
        """controllers.admin.Controller.banner_set is working properly"""
        languageid, tadm = self._fill_db()
        media = Media(u'image', u'test image', u'/test.png', tadm, u'xx',
                                                                u'random text')
        DBSession.add(media)
        link = Link(u'test link', u'http://example.com', tadm, u'xx',
                                                                u'random text')
        DBSession.add(link)
        DBSession.flush()
        mediaid = media.id
        linkid = link.id
        transaction.commit()
        
        environ = {'REMOTE_USER': 'test_admin'}
        response = self.app.post('/admin/banner_set',
                                            dict(mediaid=mediaid,
                                                 linkid=linkid,
                                                ),
                                            extra_environ=environ, status=302)
        #redirected = response.follow(extra_environ=environ, status=200)

        bc = DBSession.query(BannerContent).first()
        eq_(bc.media_id, mediaid)
        eq_(bc.link_id, linkid)

