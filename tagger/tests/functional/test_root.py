# -*- coding: utf-8 -*-
"""
Functional test suite for the root controller.

This is an example of how functional tests can be written for controllers.

As opposed to a unit-test, which test a small unit of functionality,
functional tests exercise the whole application and its WSGI stack.

Please read http://pythonpaste.org/webtest/ for more information.

"""
from nose.tools import assert_true, eq_

from tagger.tests import TestController
from tagger.model import DBSession, User, Language, Category, Article
import transaction


class TestRootController(TestController):
    """Tests for the method in the root controller."""

    def _fill_db(self):
        tadm = DBSession.query(User).filter_by(user_name=u'test_admin').one()
        language = Language(u'xx', u'test_langugage')
        DBSession.add(language)
        cat = Category(u'test_category', u'xx')
        DBSession.add(cat)
        article = Article(u'A Test Article!', cat, u'xx', tadm, u'random text')
        DBSession.add(article)
        DBSession.flush()
        categoryid = cat.id
        articleid = article.id
        languageid = language.id
        transaction.commit()
        return languageid, categoryid, articleid

    def test_index(self):
        """The front page is working properly"""
        response = self.app.get('/')
        msg = 'index'
        # You can look for specific strings:
        assert_true(msg in response)

    # TODO: check for url "/category"
    def test_default(self):
        """articles can be retrived with url: /category/articleid"""
        languageid, categoryid, articleid = self._fill_db()

        response = self.app.get('/test_category/a-test-article')

        assert_true(str(response.html.find(id='content_with_side')),
                                'content should have class "content_with_side"')
        title = response.html.find('div', 'article_title')
        eq_(str(title.h1), '<h1>A Test Article!</h1>')
        eq_(str(title.find('span', 'user')),
                                        '<span class="user">test_admin</span>')


