from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('item/<int:item_id>', views.item_view, name='item'),
    path('add/<int:item_id>', views.add_to_order, name='add_to_order'),
    path('config/', views.stripe_config),
    path('buy/', views.create_checkout_session),
    path('success/', views.success_view), # new
    path('cancelled/', views.cancelled_view), # new
]
