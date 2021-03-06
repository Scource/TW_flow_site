# Generated by Django 3.0.8 on 2021-06-15 18:02

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import info_flow.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_is_balancing_unit', models.BooleanField(default=False)),
                ('user_is_b_mesuring_unit', models.BooleanField(default=False)),
                ('user_is_constracts_unit', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(max_length=20)),
                ('cat_level', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='patterns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pat_name', models.CharField(max_length=150)),
                ('pat_is_private', models.BooleanField(default=False)),
                ('pat_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pat_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info_flow.category')),
            ],
        ),
        migrations.CreateModel(
            name='process',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proc_process_name', models.CharField(max_length=150)),
                ('proc_description', models.TextField(null=True)),
                ('proc_created', models.DateTimeField(auto_now_add=True)),
                ('proc_modified', models.DateTimeField(auto_now=True)),
                ('proc_start_date', models.DateTimeField(blank=True, null=True)),
                ('proc_end_date', models.DateTimeField(blank=True, null=True)),
                ('proc_is_active', models.BooleanField(default=True)),
                ('proc_is_private', models.BooleanField(default=False)),
                ('proc_is_deleted', models.BooleanField(default=False)),
                ('proc_assigned', models.ForeignKey(blank=True, null=True, on_delete=models.SET('2'), related_name='assigned_user', to=settings.AUTH_USER_MODEL)),
                ('proc_author', models.ForeignKey(on_delete=models.SET('2'), related_name='proc_user', to=settings.AUTH_USER_MODEL)),
                ('proc_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info_flow.category')),
            ],
            options={
                'ordering': ['-proc_modified', '-proc_created', '-proc_is_active'],
                'permissions': (('connect_proc', 'Connect process'),),
            },
        ),
        migrations.CreateModel(
            name='user_status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('us_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tasks_name', models.CharField(max_length=150)),
                ('tasks_description', models.TextField(null=True)),
                ('tasks_created', models.DateTimeField(auto_now_add=True)),
                ('tasks_modified', models.DateTimeField(auto_now=True)),
                ('tasks_start_date', models.DateTimeField(blank=True, null=True)),
                ('tasks_end_date', models.DateTimeField(blank=True, null=True)),
                ('tasks_is_active', models.BooleanField(default=True)),
                ('tasks_is_deleted', models.BooleanField(default=False)),
                ('tasks_assigned', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('tasks_author', models.ForeignKey(on_delete=models.SET('2'), related_name='tasks_user', to=settings.AUTH_USER_MODEL)),
                ('tasks_proc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info_flow.process')),
                ('tasks_tasks', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='info_flow.tasks')),
            ],
            options={
                'permissions': (('connect_task', 'Connect task'), ('connect_point', 'Connect point')),
            },
        ),
        migrations.CreateModel(
            name='posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posts_title', models.CharField(max_length=150)),
                ('posts_created', models.DateTimeField(auto_now_add=True)),
                ('posts_modified', models.DateTimeField(auto_now=True)),
                ('posts_text', models.TextField()),
                ('posts_is_deleted', models.BooleanField(default=False)),
                ('post_level', models.IntegerField(default=0)),
                ('posts_author', models.ForeignKey(on_delete=models.SET('2'), to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='patterns_elements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pele_order', models.IntegerField()),
                ('pele_type', models.IntegerField()),
                ('pele_name', models.CharField(max_length=150)),
                ('pele_desc', models.TextField(null=True)),
                ('pele_proc', models.IntegerField(blank=True, null=True)),
                ('pele_task', models.IntegerField(blank=True, null=True)),
                ('pele_pattern', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info_flow.patterns')),
            ],
            options={
                'ordering': ['pele_order'],
            },
        ),
        migrations.CreateModel(
            name='messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mess_created', models.DateTimeField(auto_now_add=True)),
                ('mess_modified', models.DateTimeField(auto_now=True)),
                ('mess_text', models.TextField()),
                ('mess_is_deleted', models.BooleanField(default=False)),
                ('mess_author', models.ForeignKey(on_delete=models.SET('2'), to=settings.AUTH_USER_MODEL)),
                ('mess_posts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info_flow.posts')),
            ],
        ),
        migrations.CreateModel(
            name='files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('files_name', models.CharField(max_length=300)),
                ('files_added', models.DateTimeField(auto_now_add=True)),
                ('files_is_deleted', models.BooleanField(default=False)),
                ('files_document', models.FileField(blank=True, null=True, upload_to=info_flow.models.user_directory_path)),
                ('files_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('files_posts', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='info_flow.posts')),
                ('files_proc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='info_flow.process')),
                ('files_tasks', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='info_flow.tasks')),
            ],
        ),
        migrations.CreateModel(
            name='comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('com_body', models.TextField(null=True)),
                ('com_created', models.DateTimeField(auto_now_add=True)),
                ('com_modified', models.DateTimeField(auto_now=True)),
                ('com_is_deleted', models.BooleanField(default=False)),
                ('com_author', models.ForeignKey(on_delete=models.SET('2'), to=settings.AUTH_USER_MODEL)),
                ('com_proc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='info_flow.process')),
                ('com_tasks', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='info_flow.tasks')),
            ],
            options={
                'ordering': ['-com_created'],
            },
        ),
        migrations.CreateModel(
            name='archive_posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arch_posts_title', models.CharField(max_length=150)),
                ('arch_posts_created', models.DateTimeField(auto_now_add=True)),
                ('arch_posts_modified', models.DateTimeField(auto_now=True)),
                ('arch_posts_text', models.TextField()),
                ('arch_posts_is_deleted', models.BooleanField(default=False)),
                ('arch_posts_author', models.ForeignKey(on_delete=models.SET('2'), to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
