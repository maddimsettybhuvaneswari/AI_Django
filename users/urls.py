from django.urls import path
from .views import login, register, userdata, emailExistorNot, updatepassword, add_doctors, getDoctorsdata, book_appointments, getAppointments, chat, get_chatting, get_previouschatting

urlpatterns = [
    path('login/', login),
    path('register/', register),
    path('userdata/', userdata),
    path('emailExistorNot/', emailExistorNot),
    path('updatepassword/', updatepassword),
    path('add_doctors/', add_doctors),
    path('getDoctorsdata/', getDoctorsdata),
    path('book_appointments/', book_appointments),
    path('getAppointments/', getAppointments),
    path("chat/", chat),
    path("get_chatting/", get_chatting),
    path("get_previouschatting/", get_previouschatting)

]