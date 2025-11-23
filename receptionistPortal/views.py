from django.shortcuts import render


def report(request):
    text = 'Hello Every One'
    return render(request,'report.html',{'text' : text})