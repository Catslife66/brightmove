from django.urls import path

from . import views

app_name = 'property'

urlpatterns = [
    path('search/', views.search_by_location, name='search'),
    path('sort-by/', views.sort_by, name='sort-by'),
    path('filter-search/', views.filter_search, name='filter-search'),
    path('<int:pk>/map/', views.show_on_map, name='map'),
    path('<int:pk>/update/', views.update_property_detail_view, name='update-property'),
    path('<int:pk>/send-email/', views.email_owner, name='email'),
    path('<int:pk>/', views.property_detail_view, name='property-detail'),
    path('upload/', views.property_upload_view, name='upload'),
    path('<int:pk>/add-to-wishlist/', views.update_wishlist, name='add-to-wishlist'),
]