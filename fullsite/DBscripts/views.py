from django.shortcuts import render, HttpResponse
from django.views import View
from .scripts import GetPeakValues
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
#from django.core import serializers
import json
from io import BytesIO
import pandas as pd
# Create your views here.

from .forms import ScriptsForm


@method_decorator(login_required, name='dispatch')
class Scripts(View):
    #form_class = ScriptsForm
    template_name = 'DBscripts/dbs_form_script.html'

    def get(self, request):
        form = ScriptsForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form=ScriptsForm(request.POST)
        if form.is_valid():
            with BytesIO() as b:
                data = GetPeakValues(form.cleaned_data)
                with pd.ExcelWriter(b) as writer:
                    data.to_excel(writer, sheet_name="Data", index=False)

                filename = f"zawyzone_dane_{form.cleaned_data['date_from']}.xlsx"
                print(filename)
                res = HttpResponse(
                    b.getvalue(),
                    content_type='application/vnd.ms-excel'
                )
                res['Content-Disposition'] = f'attachment; filename={filename}'
                return res

        # if self.request.is_ajax and self.request.method == "POST":

        #     form = ScriptsForm(request.POST)
        #     if form.is_valid():
        #         test=TestScript(form.cleaned_data)
        #         ser_instance = json.dumps(test)

        #         # send to client side.
        #         return JsonResponse({"instance": ser_instance}, status=200)
        #     else:
        #         return JsonResponse({"error": form.errors}, status=400)

        # return JsonResponse({"error": ""}, status=400)
