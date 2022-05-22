from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, FileResponse
from django.urls import resolve, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.views.generic.edit import CreateView, DeleteView, FormMixin
from django.views.generic import ListView, UpdateView, DetailView

from .forms import *
from .models import *
from .filters import ElementFilter, ConnectionFilter, PowerplantFilter


#Files Views
class DeleteFileView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = File
    template_name = 'file_confirm_delete.html'
    permission_required = 'BalancingMarket.delete_file'

    def get_success_url(self):
        return reverse_lazy('BalancingMarket:element_detail', kwargs={'pk': self.object.files_element.id})

class DownloadFileView(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = 'BalancingMarket.view_file'
    
    def get(self, request, *args, **kwargs):
        obj = File.objects.get(pk=self.kwargs['pk'])
        filename = settings.BASE_DIR+obj.document.url
        response = FileResponse(open(filename, 'rb'))
        response['Content-Disposition'] = "attachment; filename=" + obj.name
        return response

#Elements Views
class ElementView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = 'BalancingMarket.view_element'
    model=Element
    template_name = 'element_list.html'
    paginate_by=30
    
    def filter_qs(self):
        url = resolve(self.request.path).url_name
        URB = 0 if url == 'element_list_POB' else 1
        qs = super().get_queryset()
        return qs.filter(element_type=URB)

    def get_queryset(self):   
        return ElementFilter(
            self.request.GET, queryset=self.filter_qs()).qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
        filter=ElementFilter(self.request.GET,
                             queryset=self.filter_qs()))
        return context

class ElementCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = ElementForm
    template_name = 'element_form.html'
    success_url = reverse_lazy('BalancingMarket:element_list_POB')
    permission_required = 'BalancingMarket.add_element'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)

class ElementUpdateView(ElementCreateView, PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Element
    template_name = 'element_form_update.html'
    permission_required = 'BalancingMarket.change_element'

    def get_success_url(self):
        return reverse_lazy('BalancingMarket:element_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class ElementDetailView(PermissionRequiredMixin, LoginRequiredMixin, FormMixin, DetailView):
    model = Element
    template_name = 'element_detail.html'
    form_class = ElementFileForm
    permission_required = 'BalancingMarket.view_element'

    def get_success_url(self):
        return reverse_lazy('BalancingMarket:element_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['added_files'] = File.objects.filter(
            files_element=self.kwargs['pk'])
        context['form'] = self.get_form()
        context['connections'] = Connection.objects.filter(
            Q(POB=self.object.id) | Q(SE=self.object.id))
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            for f in request.FILES.getlist('document'):
                newFile = File(document=f)
                newFile.files_element = Element.objects.get(id=self.kwargs['pk'])
                newFile.User = self.request.user
                newFile.name = f
                newFile.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)

class ElementDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Element
    template_name = 'element_confirm_delete.html'
    success_url = reverse_lazy('BalancingMarket:element_list_POB')
    permission_required = 'BalancingMarket.delete_element'


#Connections Views
class ConnList(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Connection
    template_name = 'connection_list.html'
    paginate_by = 30
    permission_required = 'BalancingMarket.view_connection'

    def get_queryset(self):
        qs = super().get_queryset()
        return ConnectionFilter(self.request.GET, queryset=qs).qs

    def get_context_data(self, **kwargs):
        qs = super().get_queryset()
        context = super().get_context_data(**kwargs)
        context.update(
            filter=ConnectionFilter(self.request.GET, queryset=qs))
        return context

class ConnCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = ConnectionForm
    template_name = 'connection_form.html'
    permission_required = 'BalancingMarket.add_connection'

    def get_success_url(self):
        return reverse_lazy('BalancingMarket:connection_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class ConnUpdateView(ConnCreateView, PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Connection
    template_name = 'connection_form_update.html'
    permission_required = 'BalancingMarket.change_connection'

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('BalancingMarket:connection_detail', kwargs={'pk': self.object.id})

class ConnDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    model = Connection
    template_name = 'connection_detail.html'
    permission_required = 'BalancingMarket.view_connection'

class ConnDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Connection
    template_name = 'connection_confirm_delete.html'
    permission_required = 'BalancingMarket.delete_connection'

    def get_success_url(self):
        return reverse_lazy('BalancingMarket:element_detail', kwargs={'pk': self.object.POB.id})


#PowerPlants Views
class PowerPlantList(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Powerplant
    template_name = 'powerplant_list.html'
    paginate_by = 30
    permission_required = 'BalancingMarket.view_powerplant'

    def get_queryset(self):
        qs = super().get_queryset()
        return PowerplantFilter(self.request.GET, queryset=qs).qs

    def get_context_data(self, **kwargs):
        qs = super().get_queryset()
        context = super().get_context_data(**kwargs)
        context.update(
            filter=PowerplantFilter(self.request.GET, queryset=qs))
        return context

class PowerPlantCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = PowerplantForm
    template_name = 'powerplant_form.html'
    success_url = reverse_lazy('BalancingMarket:powerplant_list')
    permission_required = 'BalancingMarket.add_powerplant'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)

class PowerPlantUpdateView(PowerPlantCreateView, PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Powerplant
    template_name = 'powerplant_form_update.html'
    permission_required = 'BalancingMarket.change_powerplant'

    def get_success_url(self):
        return reverse_lazy('BalancingMarket:powerplant_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class PowerPlantDetailView(PermissionRequiredMixin, LoginRequiredMixin, FormMixin, DetailView):
    model = Powerplant
    template_name = 'powerplant_detail.html'
    form_class = ElementFileForm
    permission_required = 'BalancingMarket.view_powerplant'

    def get_success_url(self):
        return reverse_lazy('BalancingMarket:powerplant_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['added_files'] = File.objects.filter(
            files_powerplant=self.kwargs['pk'])
        context['form'] = self.get_form()
        context['pp_connections'] = PowerPlantConnection.objects.filter(
            powerplant=self.object.id)
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            for f in request.FILES.getlist('document'):
                newFile = File(document=f)
                newFile.files_powerplant = Powerplant.objects.get(
                    id=self.kwargs['pk'])
                newFile.User = self.request.user
                newFile.name = f
                newFile.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)


class PowerPlantDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Powerplant
    template_name = 'powerplant_confirm_delete.html'
    success_url = reverse_lazy('BalancingMarket:powerplant_list')
    permission_required = 'BalancingMarket.delete_powerplant'


#PowerPlant Connection Views
class PowerPlantConnectionCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = PowerplantConnectionForm
    template_name = 'powerplantconn_form.html'
    permission_required = 'BalancingMarket.add_powerplant'

    def get_success_url(self):
        return reverse_lazy('BalancingMarket:powerplant_detail', kwargs={'pk': self.object.powerplant.id})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class PowerPlantConnectionUpdateView(PowerPlantConnectionCreateView, PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = PowerPlantConnection
    template_name = 'powerplantconn_form_update.html'
    permission_required = 'BalancingMarket.change_powerplant'

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class PowerPlantConnectionDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = PowerPlantConnection
    template_name = 'powerplantconn_confirm_delete.html'
    permission_required = 'BalancingMarket.delete_powerplant'

    def get_success_url(self):
        return reverse_lazy('BalancingMarket:powerplant_detail', kwargs={'pk': self.object.powerplant.id})
