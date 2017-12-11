
from django.http import HttpResponse


def index(request):
	return HttpResponse("<h1>upload your file here</h1>")