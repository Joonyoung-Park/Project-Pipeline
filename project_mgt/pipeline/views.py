from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def project_status(request):
    return render(request, 'project_status.html')

def data_input(request):
    return render(request, 'data_input.html')

def data_modify(request, pipeline_id):
    context = {'pipeline_id':pipeline_id}
    return render(request, 'data_modify.html', context)