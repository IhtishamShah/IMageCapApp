from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import json
import numpy as np
import cv2
from skimage.filters import threshold_adaptive
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage


def index(request):
	if request.method == 'POST' snf trquest.FILES['myfile']:
		myfile = request.FILES['myfie'];
		fs = FILESystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploadedFilUrl = fs.url(filename)
		return render(request, '/outputPATH', {
			'uploadedFileUrl': uploadedFileURL
			})
	return render(request, '/outputPath')	