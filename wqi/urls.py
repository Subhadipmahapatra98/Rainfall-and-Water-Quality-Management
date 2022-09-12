from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('superadmin', views.superadmin, name="superadmin"),
    path('adminneworder', views.adminneworder, name="adminneworder"),
    path('adminconfirmed', views.adminconfirmed, name="adminconfirmed"),
    path('admindelivered', views.admindelivered, name="admindelivered"),
    path('admindeleted', views.admindeleted, name="admindeleted"),
    path('admindelete/<int:id>', views.admindelete, name="admindelete"),
    path('adminapproved/<int:id>', views.adminapproved, name="adminapproved"),
    path('admindelivering/<int:id>', views.admindelivering, name="admindelivering"),
    path('delivering', views.delivering, name="delivering"),
    path('adminnewproduct', views.adminnewproduct, name="adminnewproduct"),
    
    path('',views.home,name="home"),
    path('home',views.home,name="home"),
    path('main',views.main,name="main"),
    path('login/',views.login_call,name="login_call"),
    path('logout',views.logout_call,name="logout_call"),
    path('reg/',views.reg,name="reg"),
    path('rainfall',views.rainfall, name="rainfall"),
    path('wqi',views.wqi, name="wqi"),
    # path('waterquality',views.waterquality, name="waterquality"),
    path('rfvisualization',views.rfvisualization, name="rfvisualization"),
    path('wqivisualization',views.wqivisualization, name="wqivisualization"),
    path('userbuy',views.userbuy,name="userbuy"),
    path('order/<int:id>',views.order,name="order"),
    path('payment/',views.payment,name="payment"),
    path('orderdetails',views.orderdetails,name="orderdetails"),
    path('contact',views.contact, name="contact")
    # path('about',views.about, name="about")
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)