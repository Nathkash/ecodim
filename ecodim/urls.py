from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='dashboard', permanent=False)),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('moniteurs/', views.moniteurs_list, name='moniteurs_list'),
    path('moniteurs/ajouter/', views.moniteur_ajouter, name='moniteur_ajouter'),
    path('moniteurs/<int:pk>/', views.moniteur_detail, name='moniteur_detail'),

    path('enfants/', views.enfants_list, name='enfants_list'),
    path('enfants/ajouter/', views.enfant_ajouter, name='enfant_ajouter'),
    path('enfants/<int:pk>/', views.enfant_detail, name='enfant_detail'),
    path('enfants/<int:pk>/modifier/', views.enfant_modifier, name='enfant_modifier'),

    path('lecons/', views.lecons_list, name='lecons_list'),
    path('lecons/ajouter/', views.lecon_ajouter, name='lecon_ajouter'),
    path('lecons/<int:pk>/', views.lecon_detail, name='lecon_detail'),
    path('lecons/<int:pk>/modifier/', views.lecon_modifier, name='lecon_modifier'),

    path('presences/', views.presences_list, name='presences_list'),
    path('presences/seance/<int:pk>/', views.presence_seance, name='presence_seance'),
    path('presences/nouvelle/', views.nouvelle_seance, name='nouvelle_seance'),
]
