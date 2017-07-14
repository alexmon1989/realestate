from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django_tables2 import SingleTableView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse

from managers.models import Manager
from managers.tables import ManagerTable
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from decorators import group_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from managers.forms import ManagerForm


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

    @method_decorator(login_required)
    @method_decorator(group_required(('Users', 'Self')))
    def dispatch(self, *args, **kwargs):
        return super(ManagerList, self).dispatch(*args, **kwargs)


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

    @method_decorator(login_required)
    @method_decorator(group_required(('Users', 'Self')))
    def dispatch(self, *args, **kwargs):
        return super(ManagerCreate, self).dispatch(*args, **kwargs)

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

    @method_decorator(login_required)
    @method_decorator(group_required(('Users', 'Self')))
    def dispatch(self, *args, **kwargs):
        return super(ManagerEdit, self).dispatch(*args, **kwargs)


class ManagerDelete(DeleteView):
    """Displays page with delete confirm and deletes manager."""
    model = Manager
    success_url = reverse_lazy('managers:manager_list')

    def get_queryset(self):
        """User can delete only own managers."""
        qs = super(ManagerDelete, self).get_queryset()
        return qs.filter(user=self.request.user)

    @method_decorator(login_required)
    @method_decorator(group_required(('Users', 'Self')))
    def dispatch(self, *args, **kwargs):
        return super(ManagerDelete, self).dispatch(*args, **kwargs)


@require_POST
@csrf_exempt
@login_required
@group_required(('Users', 'Self'))
def add_manager_ajax(request):
    """Creates manager (by ajax request)."""
    form = ManagerForm(request.POST)
    if form.is_valid():
        form.instance.user = request.user
        manager = form.save()

        return JsonResponse({
            'success': 1,
            'pk': manager.pk,
            'name': manager.name
        })
    else:
        return JsonResponse({'success': 0, 'errors': form.errors}, status=422)
