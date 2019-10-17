from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

def main(request):
    # print(request.user)
    # print(request.user.first_name)
    # print(request.user.last_name)
    # print(dir(User))
    
    if not request.user.is_authenticated:
        return render(request, 'main_page/base.html')
    else:
        uid_user = str(request.user)[2:]
        user_acc = SocialAccount.objects.get(uid = uid_user)
        friends = user_acc.extra_data['friends_data']
        friend_list = []
        i = 1
        for friend in friends:
            string = str(i) + ') ' + 'id:' + str(friend['id']) + ' ' + friend['first_name'] + friend['last_name']
            i += 1
            friend_list.append(string)
        return render(request, 'main_page/profile.html', context = {
                                                            'firstname': request.user.first_name, 
                                                            'lastname': request.user.last_name,
                                                            'friend_list': friend_list,

                                                            })

