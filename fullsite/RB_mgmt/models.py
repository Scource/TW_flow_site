"""
List of models for RB_mgmt app
"""
from django.db import models
from django.conf import settings

# Create your models here.


def user_directory_path(filename):
    """Path to iploaded files"""
    return 'user_files/rb_documents/{0}'.format(filename)


class Element(models.Model):
    """	RB elements defining POB and SE"""
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    dt_from = models.DateTimeField(null=True, blank=True)
    dt_to = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET('1'), related_name='ElementAuthor')
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET('1'), related_name='ElementModifier')
    element_type = models.IntegerField()
    is_added = models.BooleanField(default=False)

    def __str__(self):
        return self.code


class Connection(models.Model):
    """	Defining connections between POB and SE"""
    POB = models.ForeignKey(
        Element, on_delete=models.CASCADE, related_name='POB')
    SE = models.ForeignKey(
        Element, on_delete=models.CASCADE, related_name='SE')
    dt_from = models.DateTimeField(null=True, blank=True)
    dt_to = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET('1'), related_name='ConnectionAuthor')
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET('1'), related_name='ConnectionModifier')


class CsprElement(models.Model):
    """	Defining POB and SE elements in CSPR system"""
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=130)
    cspr_id = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET('1'), related_name='CsprElementAuthor')
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET('1'), related_name='CsprElementModifier')
    element_type = models.IntegerField()


class Powerplant(models.Model):
    """	Defining power producing facilities """
    name = models.CharField(max_length=130)
    PPE = models.CharField(max_length=40)
    POB = models.ForeignKey(
        Element, on_delete=models.CASCADE, related_name='PowerplantPOB')
    dt_from = models.DateTimeField(null=True, blank=True)
    dt_to = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET('1'), related_name='PowerplantAuthor')
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET('1'), related_name='PowerplantModifier')
    is_added = models.BooleanField(default=False)
    element_type = models.IntegerField()


class PowerPlantConnection(models.Model):
    POB = models.ForeignKey(
        Element, on_delete=models.SET_NULL, related_name='PowerplantElement', null=True)
    PowerPlantItem = models.ForeignKey(
        Powerplant, on_delete=models.CASCADE, related_name='PowerPlantItem')
    dt_from = models.DateTimeField(null=True, blank=True)
    dt_to = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(
        auto_now_add=True)
    modified = models.DateTimeField(
        auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET('1'), related_name='PowerplantConnecionAuthor')
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET('1'), related_name='PowerplantConnecionModifier')
    element_type = models.IntegerField()


class CsprPowerplant(models.Model):
    """	Defining power producing facilities in CSPR system """
    cspr_id = models.IntegerField()
    POB = models.ForeignKey(
        Element, on_delete=models.CASCADE, related_name='CsprPowerplantPOB')


class File(models.Model):
    """	Files connected with rest of RB-mgmt models """
    name = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    User = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET('1'))
    document = models.FileField(
        upload_to=user_directory_path, blank=True, null=True)
    files_element = models.ForeignKey(
        Element, on_delete=models.CASCADE, blank=True, null=True)
    files_element = models.ForeignKey(
        Connection, on_delete=models.CASCADE, blank=True, null=True)
    files_element = models.ForeignKey(
        Powerplant, on_delete=models.CASCADE, blank=True, null=True)
