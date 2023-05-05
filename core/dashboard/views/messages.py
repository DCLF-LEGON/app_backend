from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from core.utils.constants import MediaType
from core.utils.decorators import AdminOnly, MustLogin
from dashboard.forms import MessageForm
from dashboard.models import Message, MessageCategory, Preacher


class MessagesListView(View):
    '''CBV for messsages list page'''

    template = 'dashboard/messages.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        message_objects = Message.objects.all().order_by('-created_at')
        context = {
            'message_objects': message_objects,
            'total_messages': message_objects.count(),
        }
        return render(request, self.template, context)


class CreateUpdateMessageView(View):
    '''CBV for create/update message'''

    template = 'dashboard/form-renderers/create_update_message.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        message_id = request.GET.get('message_id') or None
        message = Message.objects.filter(id=message_id).first()
        preachers = Preacher.objects.all().order_by('-created_at')
        categories = MessageCategory.objects.all().order_by('-created_at')
        media_types = [item.value for item in MediaType.__members__.values()]

        if message:
            head = "Update"
        else:
            head = "Create"
        context = {
            "head": head,
            'message': message,
            'preachers': preachers,
            'media_types': media_types,
            'categories': categories,
        }
        print(preachers)
        print(categories)
        print(media_types)
        return render(request, self.template, context)

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        message_id = request.POST.get('message_id') or None
        preacher_id = request.POST.get('preacher')
        category_id = request.POST.get('category')
        preacher = Preacher.objects.filter(id=preacher_id).first()
        category = MessageCategory.objects.filter(id=category_id).first()
        message = Message.objects.filter(id=message_id).first()
        form = MessageForm(request.POST, request.FILES or None, instance=message)  # noqa
        if form.is_valid():
            messsage = form.save(commit=False)
            messsage.preacher = preacher
            messsage.category = category
            messsage.save()
            if message_id:
                messages.info(request, 'Message updated successfully')
            else:
                messages.info(request, 'Message created successfully')
            return redirect('dashboard:messages')
        else:
            for k, v in form.errors.items():
                print(k, v)
                messages.info(request, f'{k}: {v}')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class MessageDetailsView(View):
    '''CBV for message details page'''

    template = 'dashboard/details/details_message.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        message_id = request.GET.get('message_id')
        message = Message.objects.filter(id=message_id).first()
        context = {
            'message': message,
        }
        return render(request, self.template, context)


class SearchMessageView(View):
    '''CBV for searching messages'''

    template = 'dashboard/messages.html'

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        message_objects = Message.objects.filter(
            Q(title__icontains=query) |
            Q(media_type__icontains=query) |
            Q(category__name__icontains=query) |
            Q(preacher__name__icontains=query)
        ).order_by('-created_at')
        context = {
            'message_objects': message_objects,
            'total_messages': message_objects.count(),
            'search': True,
        }
        return render(request, self.template, context)


class DeleteMessageView(View):
    '''CBV for deleting a message'''

    @method_decorator(MustLogin)
    def get(self, request, *args, **kwargs):
        '''redirect to messages list if request is get'''
        return redirect('dashboard:messages')

    @method_decorator(MustLogin)
    def post(self, request, *args, **kwargs):
        message_id = request.POST.get('message_id') or None
        if message_id:
            Message.objects.filter(id=message_id).delete()
            messages.success(request, 'Message deleted successfully')
        return redirect('dashboard:messages')
