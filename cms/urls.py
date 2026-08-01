from django.urls import path
from . import views
app_name = "cms"
urlpatterns = [
    path("login/", views.admin_login, name="admin_login"),
    # 2. Dashboard Route
    path("dashboard/", views.dashboard, name="dashboard"),
    # 3. Logout Route
    path("logout/", views.admin_logout, name="admin_logout"),
        
 # BOOKINGS
    
    path("bookings/", views.booking_list, name="booking_list"),
    
    path("bookings/<int:id>/", views.booking_detail, name="booking_detail"),
        
    path(
        "bookings/<int:id>/edit/",
        views.booking_edit,
        name="booking_edit",
    ),
    
    path(
        "bookings/<int:id>/delete/",
        views.booking_delete,
        name="booking_delete",
    ),
        
    path(
        "customers/",
        views.customer_list,
        name="customer_list",
    ),
        
    path(
        "customers/<int:id>/",
        views.customer_detail,
        name="customer_detail",
    ),
        
        path(
        "customers/edit/<int:id>/",
        views.customer_edit,
        name="customer_edit",
        ),
        
    path(
        "customers/delete/<int:id>/",
        views.customer_delete,
        name="customer_delete",
    ),
        
    path("halls/", views.hall_list, name="hall_list"),
        
    path("halls/<int:id>/", views.hall_detail, name="cms_hall_detail"),
        
    path("halls/<int:id>/edit/", views.hall_edit, name="hall_edit"),
        
    path("halls/add/", views.hall_add, name="hall_add"),
        
        
    path(
        "hall-feature/add/<int:hall_id>/",
        views.hall_feature_add,
        name="hall_feature_add",
    ),
    
    path(
        "hall-feature/<int:id>/edit/",
        views.hall_feature_edit,
        name="hall_feature_edit",
    ),
        
    path(
        "hall-feature/<int:id>/delete/",
        views.hall_feature_delete,
        name="hall_feature_delete",
    ),
        
    path(
        "hall-feature/save/<int:hall_id>/",
         views.hall_feature_save,
        name="hall_feature_save",
    ),
        
    path(
        "hall-gallery/save/<int:hall_id>/",
        views.hall_gallery_save,
        name="hall_gallery_save",
    ),
    
    path(
        "hall-gallery/delete/<int:id>/",
        views.hall_gallery_delete,
        name="hall_gallery_delete",
    ),
        
        # Furniture
    path(
        "furniture/add/",
        views.furniture_add,
        name="furniture_add",
    ),
    
    path(
        "furniture/save/",
        views.furniture_save,
        name="furniture_save",
    ),
    
    path(
        "furniture/edit/<int:id>/",
        views.furniture_edit,
        name="furniture_edit",
    ),
    
    path(
         "furniture/delete/<int:id>/",
        views.furniture_delete,
        name="furniture_delete",
    ),
    
    path(
        "furniture/category/add/",
        views.furniture_category_add,
        name="furniture_category_add",
    ),
        
    path(
        "furniture/",
        views.furniture_list,
        name="furniture_list",
    ),
        
    path(
        "ajax/categories/<int:hall_id>/",
        views.load_furniture_categories,
        name="load_furniture_categories",
    ),
        
        # STAGE DESIGN ROUTES
    path("stage-design/", views.stage_design_list, name="stage_design_list"),
        
    path("stage-design/add/", views.stage_design_add, name="stage_design_add"),
        
    path("stage-design/edit/<int:id>/", views.stage_design_edit, name="stage_design_edit"),
        
    path("stage-design/delete/<int:id>/", views.stage_design_delete, name="stage_design_delete"),
        
    path("stage-category/add/", views.stage_category_add, name="stage_category_add"),
        
    path("stage-category/delete/<int:id>/", views.stage_category_delete, name="stage_category_delete"),
        
    path("service-category/add/", views.service_category_add, name="service_category_add"),
        
    path("service-category/delete/<int:id>/", views.service_category_delete, name="service_category_delete"),
        
    path("service/add/", views.service_add, name="service_add"),
        
    path("service/edit/<int:id>/", views.service_edit, name="service_edit"),
        
    path("service/delete/<int:id>/", views.service_delete, name="service_delete"),
        
    path("services/", views.service_list, name="service_list"),
        
    path('rooms/', views.room_list, name='room_list'),
        
    path('rooms/add/', views.room_add, name='room_add'),
        
    path('rooms/edit/<int:room_id>/', views.room_edit, name='room_edit'),
        
    path('rooms/delete/<int:room_id>/', views.room_delete, name='room_delete'),
    
    path('catering/', views.catering_dashboard, name='catering_list'), 
    
    path('catering/add/', views.catering_add, name='catering_add'),
    
    path('catering/edit/<int:package_id>/', views.catering_edit, name='catering_edit'),
    
    path('catering/delete/<int:package_id>/', views.catering_delete, name='catering_delete'),
    
    path(
        "caterings/<int:pk>/detail/",
        views.package_detail_view,
        name="package_detail",
    ),
    
    # 1. Main Website Gallery Page URL:
    path("gallery/", views.gallery_frontend_view, name="gallery_frontend"),
    # 2. CMS Admin Gallery Dashboard URL:
    path(
        "cms-gallery/", views.cms_gallery_view, name="gallery_dashboard"
    ),
    
    path('login/', views.admin_login, name='login'),
    path('logout/', views.cms_logout_view, name='logout'),
    path('', views.cms_dashboard, name='dashboard'),
    path('cms-gallery/', views.cms_gallery_view, name='gallery_dashboard'),
]

