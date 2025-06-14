from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib.auth.decorators import login_required

from . models import ChatGroup
from .forms import ChatmessageCreateForm

@login_required
def chat_view(request):
    if request.user.role == "department_manager" or request.user.role =="manager":
        chat_group = get_object_or_404(ChatGroup, group_name= 'public-chat')
        chat_messages = chat_group.chat_messages.all()[:30]
        form = ChatmessageCreateForm()
        if request.htmx:
            form = ChatmessageCreateForm(request.POST)
            if form.is_valid:
                message = form.save(commit=False)
                message.author = request.user
                message.group = chat_group
                message.save()
                context = {'message':message, 'user':request.user,}
                return render(request, 'chat/chat_message_p.html', context)

        return render(request, 'chat/chat.html', {'chat_messages' : chat_messages, 'form':form, 'user_role':request.user.role})
    
    else:
        return HttpResponse('!دسترسی به این صفحه برای شما مجاز نیست')