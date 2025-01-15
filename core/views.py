from django.shortcuts import render


# Create your views here.


def main(request):
    return render(request, "core/main.html")

def misdatos(request):
    return render(request, 'archivos/misdatos.html')