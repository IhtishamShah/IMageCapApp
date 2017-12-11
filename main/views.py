
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import requests
import os

def index(request):
	if request.method == 'POST' and request.FILES['myfile']:
		myfile = request.FILES['myfile']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)

		img = open(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\media\\" + myfile.name, "rb")

		r = requests.post(
		    "https://api.deepai.org/api/neuraltalk",
		    files={
		    
		    'image': img
		      
		    
		    },
		    headers={'api-key': '17b00d3b-69db-49f5-8931-1c4dc0945e25'}
		)

		print(r.json()['output'])
		
		return render(request, 'main/index.html', {
		    'uploaded_file_url': uploaded_file_url
		    })
	return render(request, 'main/index.html')