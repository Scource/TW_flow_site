"""
List of models for BMusers app
"""
from django.db import models
from django.conf import settings

# Create your models here.


def user_directory_path(self, filename):
    """Path to uploaded files"""
    return 'BMfiles/rb_documents/{0}'.format(filename)


class Element(models.Model):
    """	RB elements defining POB and SE"""
    POB=0
    SE=1
    CHOICES = (
    (POB, 'Podmiot odpowiedzialny za bilansowanie'),
    (SE, 'Sprzedawca energii')
    )

    code = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    dt_from = models.DateTimeField(null=True, blank=True)
    dt_to = models.DateTimeField(null=True, blank=True)
    cspr_id = models.IntegerField(null=True, blank=True)
    rher_id = models.IntegerField(null=True, blank=True)
    old_skome_id = models.IntegerField(null=True, blank=True)
    wire_id = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET('1'), related_name='ElementAuthor')
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET('1'), related_name='ElementModifier')
    element_type = models.IntegerField(choices=CHOICES)
    is_added = models.BooleanField(default=False)

    def __str__(self):
        return self.code


class Connection(models.Model):
    """	Defining connections between POB and SE"""
    POB = models.ForeignKey(
        Element, on_delete=models.CASCADE, related_name='POB', limit_choices_to={'element_type': 0})
    SE = models.ForeignKey(
        Element, on_delete=models.CASCADE, related_name='SE', limit_choices_to={'element_type':1})
    dt_from = models.DateTimeField(null=True, blank=True)
    dt_to = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET('1'), related_name='ConnectionAuthor')
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET('1'), related_name='ConnectionModifier')

    def __str__(self) -> str:
        return f'połączenie {self.POB} oraz {self.SE}' 

class Powerplant(models.Model):
    """	Defining power producing facilities """

    EC=0
    FW=1
    EW=2
    PV=3
    BIO=4
    CHOICES = (
        (EC, 'Elektrociepłownia'),
        (FW, 'Farma Wiatrowa'),
        (EW, 'Elektrownia Wodna'),
        (PV, 'Fotowoltaika'),
        (BIO, 'Biogazownia'),
        )
    name = models.CharField(max_length=130)
    PPE = models.CharField(max_length=40)
    cspr_id = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET('1'), related_name='PowerplantAuthor')
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET('1'), related_name='PowerplantModifier')
    is_added = models.BooleanField(default=False)
    element_type = models.IntegerField(choices=CHOICES)

    def __str__(self) -> str:
        return self.name

class PowerPlantConnection(models.Model):
    """	Defining power producing facilities connections to POB """
    POB = models.ForeignKey(
        Element, on_delete=models.CASCADE, related_name='PowerplantConnection', limit_choices_to={'element_type': 0})
    powerplant = models.ForeignKey(
        Powerplant, on_delete=models.CASCADE, related_name='Powerplant')
    dt_from = models.DateTimeField()
    dt_to = models.DateTimeField()

    def __str__(self) -> str:
        return f'połączenie {self.powerplant} oraz {self.POB}'


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
    files_connection = models.ForeignKey(
        Connection, on_delete=models.CASCADE, blank=True, null=True)
    files_powerplant = models.ForeignKey(
        Powerplant, on_delete=models.CASCADE, blank=True, null=True)
