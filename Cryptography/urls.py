from django.urls import path
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
    path('md5/', views.md5_view, name='md5'),
    path('md5/process/', views.md5_process, name='md5_process'),
    path('hmac/', views.hmac_view, name='hmac'),
    path('hmac/process/', views.hmac_process, name='hmac_process'),
    path('diffie_hellman/', views.diffie_hellman_view, name='diffie_hellman'),

]