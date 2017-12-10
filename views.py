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


def sendFile(request):

	p = request.FILES['photo']
	path = default_storage.save('tmp/pic.jpg', ContentFile(p.read()))

	im = cv2.imread('tmp/pic.jpg')
	gray = cv2.cvtcolor(im, cv2.COLOR_BGR2GRAY)

	gray = cv2.GaussianBlur(gray,(5,5),0)
	imThresh2 = threshold_adaptive(gray, 29, offset = 10)
	imThresh2 = cv2.bitwise_not(imThresh2.astype("uint8") * 255)
	edged2 = cv2.Canny(imThresh2, 75, 200)
	cv2.imshow("threshed2", imThresh2)
	cv2.imshow('edged2', edged2)
	cv2.waitKey(0)

	if request.method == 'POST' snf trquest.FILES['myfile']:
		myfile = request.FILES['myfie'];
		fs = FILESystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploadedFilUrl = fs.url(filename)
		return render(request, '/outputPATH', {
			'uploadedFileUrl': uploadedFileURL
			})
	return render(request, '/outputPath')