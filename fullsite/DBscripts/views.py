from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import resolve
from django.views.generic.edit import CreateView, DeleteView, FormMixin
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import FileResponse
from django.http import HttpResponse

from .models import Report, ReportItem
from .scripts import choose_from
from .reports import create_report
from .filters import ReportFilter

import os
import zipfile
from io import BytesIO

from django.http import HttpResponse

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
            raport=create_report(user=request.user, url=url, **form.cleaned_data)
            return redirect('DBscripts:report_item_list', pk=raport)
        else:
            return redirect(f'DBscripts:{url}')


class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'report_list.html'
    paginate_by = 30

    def get_queryset(self):
        qs = super().get_queryset().order_by('-start')
        return ReportFilter(self.request.GET, queryset=qs).qs

    def get_context_data(self, **kwargs):
        qs = super().get_queryset().order_by('-start')
        context = super().get_context_data(**kwargs)
        context.update(
            filter=ReportFilter(self.request.GET, queryset=qs))
        return context

class ReportItemListView(LoginRequiredMixin, ListView):
    model = ReportItem
    template_name = 'DBscripts/report_item_list.html'
    paginate_by = 40

    def get_queryset(self):
        return ReportItem.objects.filter(report_id=self.kwargs['pk']).order_by('-start')


class ReportItemDownloadView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        obj = ReportItem.objects.get(pk=self.kwargs['pk_item'])
        filename = settings.BASE_DIR+obj.report_file.url
        response = FileResponse(open(filename, 'rb'))
        response['Content-Disposition'] = "attachment; filename=" + \
            obj.report_name
        return response


class ReportDownloadZipView(LoginRequiredMixin, View):

    def get(self, request, **kwargs):
        filenames = ReportItem.objects.filter(report=self.kwargs['pk'])
        files = [settings.BASE_DIR+ f.report_file.url for f in filenames]

        rep=Report.objects.get(id=kwargs.get('pk'))
        zip_subdir = f'{rep.report_type}_{rep.start.strftime("%Y-%m-%d-%H:%M")}'
        zip_filename = "%s.zip" % zip_subdir

        # Open StringIO to grab in-memory ZIP contents
        s = BytesIO()

        # The zip compressor
        zf = zipfile.ZipFile(s, "w")

        for fpath in files:
            # Calculate path for file in zip
            fdir, fname = os.path.split(fpath)
            zip_path = os.path.join(zip_subdir, fname)

            # Add file, at correct path
            zf.write(fpath, zip_path)

        # Must close zip for all contents to be written
        zf.close()

        # Grab ZIP file from in-memory, make response with correct content_type
        response=HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")

        response['Content-Disposition']="attachment; filename=" + zip_filename
        return response
