from django.urls import path
from .views import *


urlpatterns = [
    path("cart-items/", GetItemsView.as_view()),
    # path('get/<userID>/', GetCartView.as_view()),
    path("add-item/", AddItemView.as_view()),
    path("get-total/", GetTotalView.as_view()),
    path("clear/", ClearCartView.as_view()),
    path("remove-item/", RemoveItemView.as_view()),
    # path('add-course-item', AddCourseItemView.as_view()),
    # path('get-item-total', GetItemTotalView.as_view()),
    # path('update-item/', UpdateItemView.as_view()),
    # path('remove-course-item', RemoveCourseItemView.as_view()),
    # path('empty-cart', EmptyCartView.as_view()),
    path("synch/", SynchCartItemsView.as_view()),
    # path('create', CartCreateView.as_view()),
]
