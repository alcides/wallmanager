from django.core import mail

from appman.models import *
from appman.signals import *

from base import *

class CategoryTest(BaseTest):
    
    def test_authorized_list_cat(self):
        """ Test category list page. """
        login = self.do_admin_login()
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TestCat</td>")
        self.assertContains(response, "<tr>", Category.objects.count()+1) # 2 cat, plus header
    
    def test_authorized_add_category(self):
        """ Test category insersion page. """
        c = Category.objects.count()
        login = self.do_admin_login()
        post_data = {
            'name': 'Action'
        }
        response = self.client.post('/categories/add/', post_data)
        self.assertRedirects(response, '/categories/')
        self.assertEqual(c+1, Category.objects.count())

    def test_unauthorized_add_category(self):
        """ Tests permition to add category. """
        c = Category.objects.count()
        login = self.do_login()
        post_data = {
            'name': 'Action'
        }
        response = self.client.post('/categories/add/', post_data)
        self.assertRedirects(response, '/accounts/login/?next=/categories/add/')
        self.assertEqual(c, Category.objects.count())

    def test_edit_cat(self):
        """ Test category edition. """
        login = self.do_admin_login()
        #change educational to Work
        post_data = {
            'name': 'Work'
        }
        response = self.client.post('/categories/%s/edit/'%self.gps.category.id, post_data)
        #see if it changed
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Work</td>")
        self.assertContains(response, "<tr>", Category.objects.count()+1) # 2 cat, plus header
        #confirm that the application category changed to work
        response = self.client.get('/applications/%s/' % self.gps.id )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Work")

    def test_remove_unused_cat(self):
        """ Test removal of empty category. """
        login = self.do_admin_login()
        c = Category.objects.count()
        response = self.client.post('/categories/%s/remove/'%self.TestCat.id)
        self.assertRedirects(response, '/categories/')
        self.assertEqual(c-1, Category.objects.count())

    def test_remove_used_cat(self):
        """ Test removal of non-empty category. """
        login = self.do_admin_login()
        c = Category.objects.count()
        response = self.client.post('/categories/%s/remove/'%self.gps.category.id)
        self.assertRedirects(response, '/categories/')
        #confirm that category unknow appeared
        response = self.client.get('/categories/')
        self.assertContains(response, DEFAULT_CATEGORY)        

        #confirm that the application category changed
        response = self.client.get('/applications/%s/'%self.gps.id)
        self.assertContains(response, DEFAULT_CATEGORY)                

    def test_default_category(self):
        """ Test existence of default category. """
        self.assertEqual(Category.objects.filter(name=DEFAULT_CATEGORY).count(), 1)
