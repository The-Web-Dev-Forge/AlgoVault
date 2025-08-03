
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('tools/', views.tools, name='tools'),
    path('about/', views.about, name='about'),
    path('help/', views.help_page, name='help'),
    path('caesar', views.caesar_cipher, name='caesar_cipher'),
    path('caesar/process', views.caesar_cipher, name='process_caesar'),
    # path('hill/', views.hill_cipher_page, name='hill_cipher_page'),
    # path('hill/process/', views.process_hill_cipher, name='process_hill_cipher'),
    path('vigenere/', views.vigenere_view, name='vigenere'),
    path('api/vigenere/process/', views.vigenere_process_api, name='vigenere_api'),
    path('des/', views.des_view, name='des'),
    path('api/des/process/', views.des_process_api, name='des_api'),
    path('sha512/', views.sha512_view, name='sha512'),
    # Handles SHA-512 processing requests from the frontend JavaScript
    path('api/sha512/process/', views.sha512_process_api, name='sha512_api'),
    path('hill/', views.hill_view, name='hill'),
    path('api/hill/process/', views.hill_process_api, name='hill_api'),
    path('aes/', views.aes_view, name='aes'),
    path('api/aes/process/', views.aes_process_api, name='aes_api'),
    path('md5/', views.md5_view, name='md5'),
    path('md5/process/', views.md5_process, name='md5_process'),
    path('hmac/', views.hmac_view, name='hmac'),
    path('hmac/process/', views.hmac_process, name='hmac_process'),
    path('diffie_hellman/', views.diffie_hellman_view, name='diffie_hellman'),

    # Dedicated error routes for profile/account dropdowns
    path('profile/', views.error_page, {'message': 'Sorry, Page not found.....'}, name='profile_error'),
    path('account-settings/', views.error_page, {'message': 'Sorry, Page not found.....'}, name='account_settings_error'),
    path('billing/', views.error_page, {'message': 'Sorry, Page not found.....'}, name='billing_error'),
    path('security/', views.error_page, {'message': 'Sorry, Page not found.....'}, name='security_error'),
    path('help-support/', views.error_page, {'message': 'Sorry, Page not found.....'}, name='help_support_error'),

    # Generic error page for unsupported/missing algorithm pages
    path('error/', views.error_page, name='error_page'),
    # Unsupported algorithms: Playfair and RC5
    path('playfair/', views.error_page, {'message': 'Playfair Cipher is not yet supported.'}, name='playfair_error'),
    path('rc5/', views.error_page, {'message': 'RC5 Cipher is not yet supported.'}, name='rc5_error'),

    # Catch-all for any undefined route in this app (should be last)
    re_path(r'^.*/$', views.error_page),

]