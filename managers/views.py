from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django_tables2 import SingleTableView
from django.contrib.messages.views import SuccessMessageMixin

from managers.models import Manager
from managers.tables import ManagerTable


class ManagerList(SingleTableView):
    """Displays page with manager's table."""
    model = Manager
    table_class = ManagerTable

    def get_queryset(self):
        return Manager.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ManagerList, self).get_context_data(**kwargs)
        context['total'] = len(self.get_table_data())
        return context


class ManagerCreate(SuccessMessageMixin, CreateView):
    """Displays page with manager's create form."""
    model = Manager
    fields = [
        'name',
        'agency',
        'phone_numbers',
        'email',
        'rate',
        'city'
    ]
    template_name_suffix = '_create_form'
    success_message = 'Manager has been successfully created.'
    success_url = reverse_lazy('managers:manager_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(ManagerCreate, self).form_valid(form)

    #def get_success_url(self):
    #    return reverse('managers:manager_edit', args=(self.object.id,))


class ManagerEdit(SuccessMessageMixin, UpdateView):
    """Displays page with manager's edit form."""
    model = Manager
    fields = [
        'name',
        'agency',
        'phone_numbers',
        'email',
        'rate',
        'city'
    ]
    template_name_suffix = '_update_form'
    success_message = 'Manager has been data successfully saved.'
    success_url = reverse_lazy('managers:manager_list')

    def get_queryset(self):
        """User can edit only own managers."""
        qs = super(ManagerEdit, self).get_queryset()
        return qs.filter(user=self.request.user)


class ManagerDelete(DeleteView):
    """Displays page with delete confirm and deletes manager."""
    model = Manager
    success_url = reverse_lazy('managers:manager_list')

    def get_queryset(self):
        """User can delete only own managers."""
        qs = super(ManagerDelete, self).get_queryset()
        return qs.filter(user=self.request.user)
