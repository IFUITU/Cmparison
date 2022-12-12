from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files import File
from .helpers import upload_file_name

class Company(models.Model):
    name = models.CharField(max_length=256, null=True)
    ceo = models.ForeignKey('client.User', on_delete=models.SET_NULL, null=True, related_name='company_ceo')
    staffs = models.ManyToManyField('client.User', related_name="company")


class Service(models.Model):
    name = models.CharField(max_length=256, null=True)
    desc = models.TextField(max_length=500, blank=True, null=True)
    icon = models.ImageField(upload_to=upload_file_name, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self,**kwargs):                         # to compress the img files!!
        if not self.icon.closed:                      #if img exists
            img = Image.open(self.icon)               #open img via Pillow
            img.thumbnail((100,100),Image.ANTIALIAS) #compress px till 100 to 100 saves proporsion donot worry!
            tmp = BytesIO()                          #Buffer massive!
            img.save(tmp,"PNG")                      #save img to massive that created before! & and change type of file to png
            #tmp.seek(0)

            self.img = File(tmp,'t.png') #telling django upload to img new file tmp-file <<t>> does not metter because we have uploaded_file_name

        return super().save(**kwargs)