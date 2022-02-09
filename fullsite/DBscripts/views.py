from django.shortcuts import render
from django.views import View
from .scripts import TestScript
from django.http import JsonResponse
#from django.core import serializers
import json

# Create your views here.

from .forms import ScriptsForm


class Scripts(View):
    #form_class = ScriptsForm
    template_name = 'DBscripts/dbs_form_script.html'

    def get(self, request):
        form = ScriptsForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        #form = self.form_class(request.POST)
        #form=ScriptsForm(request.POST)
        #if form.is_valid():
            #TestScript(form.cleaned_data)
            #return redirect('DBscripts:dbs_script')

        #return render(request, self.template_name, {'form': form})
        if self.request.is_ajax and self.request.method == "POST":

            form = ScriptsForm(request.POST)
            if form.is_valid():
                test=TestScript(form.cleaned_data)
                ser_instance = json.dumps(test)

                # send to client side.
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                return JsonResponse({"error": form.errors}, status=400)

        return JsonResponse({"error": ""}, status=400)
