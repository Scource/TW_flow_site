from django.shortcuts import render, HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import resolve
from django.http import JsonResponse
import json

from io import BytesIO
import pandas as pd

from .scripts import choose_from




@method_decorator(login_required, name='dispatch')
class ScriptsView(View):
    template_name = 'DBscripts/dbs_form_script.html'
    def get(self, request):
        url = resolve(request.path).url_name
        form = choose_from(url, 1)()
        info = choose_from(url, 3)
        return render(request, self.template_name, {'info': info, 'form': form})

    def post(self, request):
        url = resolve(request.path).url_name
        form = choose_from(url, 1)(request.POST)
        if form.is_valid():
            with BytesIO() as b:                
                function = choose_from(url, 2)
                data = function(form.cleaned_data)
                with pd.ExcelWriter(b) as writer:
                    data.to_excel(writer, sheet_name="Zestawienie")
                if form.cleaned_data['date_to']:
                    filename = f"Raport_{form.cleaned_data['date_from']}_{form.cleaned_data['date_to']}.xlsx"
                else:
                    filename = f"Raport_{form.cleaned_data['date_from']}.xlsx"
                print(filename)
                res = HttpResponse(b.getvalue(),
                    content_type='application/vnd.ms-excel')
                res['Content-Disposition'] = f'attachment; filename={filename}'
                return res


