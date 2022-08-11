"""reserves_files_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from reserves_files_app import views

urlpatterns = [
    ## main url -----------------------------------------------------
    path( 'resources/<course_code>/<file_name>/', views.file_manager, name='resource_manager_url' ),
    path( 'add/', views.adder, name='adder_url' ),
    ## other  -------------------------------------------------------
    path( '', views.root, name='root_url' ),
    path( 'error_check/', views.error_check, name='error_check_url' ),
    path( 'info/', views.info, name='info_url' ),
    path( 'version/', views.version, name='version_url' ),
    path('admin/', admin.site.urls),
]
