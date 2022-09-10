from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('contact/',views.contact,name='contact'),
    path('gallery/',views.gallery,name='gallery'),
    path('about/',views.about,name='about'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('doctor_profile/',views.doctor_profile,name='doctor_profile'),
    path('doctors/',views.doctors,name='doctors'),
    path('doctor_detail/<int:pk>/',views.doctor_detail,name='doctor_detail'),
    path('myappointment/',views.myappointment,name='myappointment'),
    path('book_appointment/<int:pk>/',views.book_appointment,name='book_appointment'),
    path('patient_cancel_appointment/<int:pk>/',views.patient_cancel_appointment,name='patient_cancel_appointment'),
    path('health_profile/',views.health_profile,name='health_profile'),
    path('my_appointment/',views.my_appointment,name='my_appointment'),
    path('doctor_index/',views.doctor_index,name='doctor_index'),
    path('doctor_approve_appointment/<int:pk>/',views.doctor_approve_appointment,name='doctor_approve_appointment'),
    path('doctor_complete_appointment/<int:pk>/',views.doctor_complete_appointment,name='doctor_complete_appointment'),
    path('doctor_cancel_appointment/<int:pk>/',views.doctor_cancel_appointment,name='doctor_cancel_appointment'),
    path('payment/',views.initiate_payment, name='payment'),
    path('callback/',views.callback, name='callback'),
    path('ajax/validate_email/',views.validate_email,name='validate_email'),
    path('ajax/validate_appointment/',views.validate_appointment,name='validate_appointment'),
    path('ajax/validate_appointment_time/',views.validate_appointment_time,name='validate_appointment_time'),
]