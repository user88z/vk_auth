import requests

from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import VKProvider

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

USER_FIELDS = ['first_name',
               'last_name',
               'nickname',
               'screen_name',
               'sex',
               'bdate',
               'city',
               'country',
               'timezone',
               'photo',
               'photo_medium',
               'photo_big',
               'photo_max_orig',
               'has_mobile',
               'contacts',
               'education',
               'online',
               'counters',
               'relation',
               'last_seen',
               'activity',
               'universities',
               'friends']

USER_FIELDS_2 = ['param_count',
                ]


class VKOAuth2Adapter(OAuth2Adapter):
    provider_id = VKProvider.id
    access_token_url = 'https://oauth.vk.com/access_token'
    authorize_url = 'https://oauth.vk.com/authorize'
    profile_url = 'https://api.vk.com/method/users.get'
    profile_url_2 = 'https://api.vk.com/method/friends.get'

    def complete_login(self, request, app, token, **kwargs):
        uid = kwargs['response'].get('user_id')
        params = {
            'v': '5.95',
            'access_token': token.token,
            'fields': ','.join(USER_FIELDS),
        }
        if uid:
            params['user_ids'] = uid
        resp = requests.get(self.profile_url,
                            params=params)
        params = {
            'v': '5.95',
            'access_token': token.token,
            'fields': ','.join(USER_FIELDS_2),
        }
        if uid:
            params['user_ids'] = uid
        resp_2 = requests.get(self.profile_url_2,
                            params=params)
        resp.raise_for_status()
        resp_2.raise_for_status()
        friends = resp_2.json()['response']['items'][0:5]
        extra_data = resp.json()['response'][0]
        extra_data['friends_data'] = friends
        email = kwargs['response'].get('email')
        if email:
            extra_data['email'] = email
        

        return self.get_provider().sociallogin_from_response(request,
                                                             extra_data)


oauth2_login = OAuth2LoginView.adapter_view(VKOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(VKOAuth2Adapter)
