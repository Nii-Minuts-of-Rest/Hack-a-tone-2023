"""
URL configuration for web_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from question import views as question_views


urlpatterns = [
    path('', question_views.start_app),
    path('admin/', admin.site.urls),
    path('question/add', question_views.upload_file),
    path('question/show', question_views.questions),
    path('question/delete', question_views.delete_question),
    path('question/analise_go', question_views.start_analisis),
    path('question/edit_answer', question_views.edit_answer),
    path('question/add_e', question_views.add_question),
    path('question/answer', question_views.answer_function),
    path('question/report', question_views.showReport),
    #path('pdf/', GeneratePdf.as_view()), 
    #path('question/')
    #path('panel/index', question_views.index),
    #path('panel/contact', question_views.contact),
    #path('panel/about', question_views.about),

]
