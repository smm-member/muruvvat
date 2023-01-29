from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_delete
from django.utils.safestring import mark_safe
# Create your models here.

class Surai(models.Model):
	number=models.CharField(max_length=50, null=True)
	name_ar = models.CharField(max_length=50)
	name_en = models.CharField(max_length=50)
	slug = models.SlugField(unique=True, null=True)
	translation_en = models.CharField(max_length=50)
	number_of_Ayah = models.CharField(max_length=50)
	audio = models.CharField(max_length=200)
	desc = RichTextField()

	class Meta:
		verbose_name = 'Surai'
		verbose_name_plural = 'Surai'

	def __str__(self):
		return f"Surai - {self.name_en}"
	
	def get_surai(self):
		return reverse('main:surai_detail', kwargs={'surai_slug':self.slug})

class Ayah(models.Model):
	experiences = models.ForeignKey(Surai, on_delete=models.CASCADE)
	text_ar = RichTextField()
	text_uz = RichTextField()
	audio = models.CharField(max_length=200, null=True)
	chapter = models.CharField(max_length=50, null=True)
	verse = models.CharField(max_length=50, null=True)
	verse_ar = models.CharField(max_length=50, null=True)
	

	class Meta:
		verbose_name = 'Ayah'
		verbose_name_plural = 'Ayah'

def user_directory_path(instance, filename):
    return 'posters/{0}/{1}'.format(instance.phone, filename)

class Profile(models.Model):
   

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField("Name",max_length=200,null=True)
    phone = models.CharField("Phone",max_length=100)
    poster = models.ImageField("Poster",upload_to=user_directory_path, default="posters/default.png")
    code = models.IntegerField(default=0)
    password = models.CharField(max_length=200)
    adress = models.CharField(max_length=200)
    utype = models.BooleanField(default=0)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    def photo(self):
        return mark_safe('<img src="{}" width="30" height="30" />'.format(self.poster.url))
    photo.short_description = 'Image'
    photo.allow_tags = True

    def __str__(self): return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)


@receiver(post_delete, sender=Profile)
def post_delete_user(sender, instance, *args, **kwargs):
    if instance.user: 
        instance.user.delete()
	
class Contact(models.Model):
	name= models.CharField(max_length=100)
	email= models.CharField(max_length=100)
	theme= models.CharField(max_length=255)
	message= models.TextField()
	is_seen = models.BooleanField(default=False)
	def __str__(self):
		return self.theme

def application_certificates(instance, filename):
    return 'health_certificates/{0}/{1}'.format(instance.id_card_number, filename)

class Application(models.Model):
	id_card_number = models.CharField(max_length=10)
	id_card_personal_number = models.IntegerField()
	health_certificate = models.ImageField(upload_to=application_certificates)
	needed_cash = models.IntegerField()
	payed = models.IntegerField(default=0)
	ca_sh = models.IntegerField(default=0)
	deadline = models.DateField()
	card_number = models.IntegerField()
	desc = RichTextField()
	is_done = models.BooleanField(default=False)
	is_it_for_print = models.BooleanField(default=False)
	profile = models.ForeignKey(Profile,null=True, on_delete=models.CASCADE)

	def __str__(self):
		return self.id_card_number

def jami(instance, filename):
    return 'jamgarma/{0}/{1}'.format(instance.name, filename)

class Jamgarma(models.Model):
	name = models.CharField(max_length=255)
	info = RichTextField()
	needed_cash = models.IntegerField()
	payed = models.IntegerField()
	remain = models.IntegerField()
	date = models.DateField()
	img = models.ImageField(upload_to=jami)

	def __str__(self):
		return self.name

