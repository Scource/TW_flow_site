
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import AnonymousUser, User, Permission
from django.urls import reverse
from ..models import *


# example tests for some of data models

class ProcessModelTest(TestCase):

    def setUp(self):
        self.User = User.objects.create_user(
            username='test', email='test@test.com', password='test')
        self.category_object = category.objects.create(
            cat_name='test', cat_level=1)
        self.process_object = process.objects.create(proc_process_name='test',
                                                     proc_author=self.User, proc_category=self.category_object)
        self.tasks_object = tasks.objects.create(
            tasks_name='test', tasks_proc=self.process_object, tasks_author=self.User)

    def test_get_absolute_url(self):
        proc = process.objects.get(id=1)
        self.assertEqual(proc.get_absolute_url(),
                         '/processes/show/1/')

    def test_task_count_property_in_process(self):
        self.assertEqual(self.process_object.task_count, '0/1')

    def test_str_is_equal_to_name(self):
        self.assertEqual(str(self.process_object),
                         self.process_object.proc_process_name)


class TaskModelTest(TestCase):

    def setUp(self):
        self.User = User.objects.create_user(
            username='test', email='test@test.com', password='test')
        self.category_object = category.objects.create(
            cat_name='test', cat_level=1)
        self.process_object = process.objects.create(proc_process_name='test',
                                                     proc_author=self.User, proc_category=self.category_object)
        self.tasks_object = tasks.objects.create(
            tasks_name='test', tasks_proc=self.process_object, tasks_author=self.User)

        self.point_object = tasks.objects.create(
            tasks_name='test', tasks_proc=self.process_object, tasks_author=self.User, tasks_tasks=self.tasks_object)

        for c in range(0, 5):
            comments.objects.create(
                com_author=self.User, com_proc=self.process_object, com_tasks=self.tasks_object)

    def test_get_absolute_url(self):
        self.assertEqual(self.tasks_object.get_absolute_url(),
                         '/processes/show/task_1/')

    def test_str_is_equal_to_name(self):
        self.assertEqual(str(self.tasks_object),
                         self.tasks_object.tasks_name)

    def test_points_count(self):
        self.assertEqual(self.tasks_object.points_count, '0/1')

    def test_task_comments_count(self):
        self.assertEqual(self.tasks_object.com_count, '5')

    def test_toggle_active_method(self):
        tasks.toggle_active(1)
        self.tasks_object = tasks.objects.get(id=1)
        self.assertFalse(self.tasks_object.tasks_is_active)

    def test_set_assignation_remove_point(self):
        tasks.set_assignation(1, self.User, False, 'point')
        self.tasks_object = tasks.objects.get(id=1)
        self.assertEqual(self.tasks_object.tasks_tasks_id, None)

    def test_set_assignation_remove_point(self):
        tasks.set_assignation(1, self.User, False, 'point')
        self.tasks_object = tasks.objects.get(id=1)
        self.assertEqual(self.tasks_object.tasks_tasks_id, None)


class PatternsModelTest(TestCase):
    def setUp(self):
        self.User = User.objects.create_user(
            username='test', email='test@test.com', password='test')
        self.category_object = category.objects.create(
            cat_name='test', cat_level=1)

        self.pattern_object = patterns.objects.create(
            pat_author=self.User, pat_category=self.category_object, pat_name='test')

        self.pat_element_object = patterns_elements.objects.create(
            pele_pattern=self.pattern_object, pele_order=1, pele_type=2)

    def test_patterns_str_name(self):
        self.assertEqual(str(self.pattern_object),
                         self.pattern_object.pat_name)

    def test_patterns_str_name(self):
        self.assertEqual(str(self.pat_element_object),
                         self.pat_element_object.pele_name)

    def test_assign_elements_to_pattern(self):
        self.assertEqual(
            self.pat_element_object.pele_pattern.id, self.pattern_object.id)

    def test_pattern_elements_name_max_length(self):
        self.assertEqual(self.pat_element_object._meta.get_field(
            'pele_name').max_length, 150)
