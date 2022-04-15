from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.display_entry,name="display_entry"),
    path('random',views.display_random,name="random"),
    path('new-page',views.new_entry,name='new_entry'),
    path('wiki/<str:title>/edit',views.edit_entry,name='edit_entry'),
    path('edit/<str:title>',views.edit_entry,name='edit_entry')
]
