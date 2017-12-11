from django.db import models

# Create your models here.


class image(models.Model):
	imageName = models.FileField(max_length=20)
	fileType = models.CharField(max_length=4)

	def __str__(self):
		return self.imageName


class result(models.Model):
	iamgeNmae = models.ForeignKey(image, on_delete=models.CASCADE)
	fileType = models.CharField(max_length=4)
	caption = models.CharField(max_length=2000)

	def __str__(self):
		return self.caption
