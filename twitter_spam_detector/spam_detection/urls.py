from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/predict/', views.api_predict_spam, name='api_predict_spam'),
    path('api/evaluate/', views.api_evaluate_accuracy, name='api_evaluate_accuracy'),
    path('api/report/', views.api_report_spam, name='api_report_spam'),
]

