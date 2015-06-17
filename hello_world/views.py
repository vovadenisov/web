from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def index(request):
    if request.method == 'GET':
        report = 'Hello World! ' + request.method
        for i in request.GET:
            report += '<br>' + i + " = " + request.GET[i]
    elif request.method == 'POST':
	    report = 'Hello World! ' + request.method
	    for i in request.POST:
	        report += '<br>' + i + " = " + request.POST[i]
    return HttpResponse(report)


