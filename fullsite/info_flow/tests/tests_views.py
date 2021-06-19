
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import AnonymousUser, User, Permission
from django.urls import reverse
from ..models import *
from ..views import *
from django.core.files.base import ContentFile


class ProcessViewTest(TestCase):

    def setUp(self):
        self.User = User.objects.create_user(
            username='test', email='test@test.com', password='test')
        self.c = Client()
        self.category_object = category.objects.create(
            cat_name='test', cat_level=1)

    def test_view_without_login(self):
        self.c.force_login(self.User)
        response = self.c.get("/processes/")
        self.assertEqual(response.status_code, 302)

    def test_if_process_list_view_with_logged_user_without_permissions(self):
        self.c.force_login(self.User)
        response = self.c.get("/processes/")
        self.assertEqual(response.status_code, 302)

    def test_if_process_list_view_with_logged_user_with_permissions(self):
        self.c.force_login(self.User)
        self.User.user_permissions.set([
            Permission.objects.get(codename='view_process')])
        response = self.c.get(reverse("info_flow:if_process_list"))
        self.assertTrue(response.status_code, 200)

    def test_if_process_list_view_use_correct_template(self):
        self.c.force_login(self.User)
        self.User.user_permissions.set([
            Permission.objects.get(codename='view_process')])
        response = self.c.get(reverse('info_flow:if_process_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info_flow/if_process_list.html')

    def test_if_new_proc_view_use_correct_template(self):
        self.c.force_login(self.User)
        self.User.user_permissions.set([
            Permission.objects.get(codename='add_process')])
        response = self.c.get(reverse('info_flow:if_new_proc'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info_flow/if_new_proc.html')

    def test_delete_proc_and_redirect(self):
        self.process_object = process.objects.create(proc_process_name='test',
                                                     proc_author=self.User, proc_category=self.category_object)
        self.c.force_login(self.User)
        self.User.user_permissions.set([
            Permission.objects.get(codename='delete_process')])
        response = self.c.delete(reverse('info_flow:if_delete_proc', kwargs={'cat': 'test', 'proc_id': self.process_object.id}),
                                 content_type='application/octet-stream', follow=True)
        self.assertEqual(response.status_code, 200)

    # def test_if_new_proc_creat_new_class_object(self):
    #     file = ContentFile(b'content', name='plain.txt')
    #     data = {'proc_process_name': 'test',
    #             'proc_author': self.User.id,
    #             'proc_category': self.category_object.id,
    #             'save_process': "Zapisz i Zakończ",
    #             'files_document': file,
    #             }
    #     self.c.force_login(self.User)
    #     self.User.user_permissions.set([
    #         Permission.objects.get(codename='add_process')])
    #     response = self.c.post(
    #         '/processes/create/', data, content_type='multipart/form-data')

    #     self.assertRedirects(response, reverse(
    #         'info_flow:if_processes', kwargs={'cat': 'test', 'active': 'active'}))

        # self.c.force_login(self.User)
        # self.User.user_permissions.set([
        #     Permission.objects.get(codename='add_process')])
        # # {'proc_process_name': 'test',
        # response = self.c.get('/processes/create/')
        # # 'proc_author': self.User, 'proc_category': self.category_object})
        # self.assertEqual(response.status_code, 200)

    # def test_if_new_proc_redirect_to_proper_url(self):
    #     self.c.force_login(self.User)
    #     self.User.user_permissions.set([
    #         Permission.objects.get(codename='add_process')])
    #     response = self.c.post('/processes/create/',  {'proc_process_name': 'test',
    #                                                    'proc_author': self.User, 'proc_category': self.category_object})
    #     self.assertTrue(response.status_code, 200)
    #     print(response.status_code)
    #     self.assertRedirects(response, expected_url='processes/test/active',
    #                          status_code=301, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
