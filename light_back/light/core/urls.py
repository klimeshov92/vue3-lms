
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

# Имя приложения в адресах.
app_name = 'core'

# Роутер.
router = DefaultRouter()

router.register(r'content_types', ContentTypeViewSet)
router.register(r'accounts', AccountsViewSet)
router.register(r'clients', ClientsViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'categories', CategoriesViewSet)
router.register(r'account_groups', AccountsGroupViewSet)
router.register(r'accounts_group_object_permissions', AccountsGroupObjectPermissionViewSet)
router.register(r'account_object_permissions', AccountObjectPermissionViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'subdivisions', SubdivisionViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'placements', PlacementViewSet)
router.register(r'group_generators', GroupGeneratorViewSet)
router.register(r'home_page', HomePageViewSet)
router.register(r'legal_page', LegalPageViewSet)
router.register(r'policy_page', PolicyPageViewSet)

# Список маршрутов приложения.
urlpatterns = [
   # Подключаем все маршруты, которые создал роутер
   path('', include(router.urls)),
   path('check-token/', check_token, name='check_token'),
   path('user_permissions_version/<int:client_version>/', user_permissions_version, name='user_permissions_version'),
   path('user_permissions/', user_permissions, name='user_permissions'),
   path('users_permissions/', users_permissions, name='users_permissions'),
   path('cabinet/', cabinet, name='cabinet'),
   path('register/', register_view, name='register'),
   path('activate/<uidb64>/<token>/', activate_user_view, name='activate'),
   path('password_reset_request/', password_reset_request_view, name='password_reset_request'),
   path('provide_access_user/<int:id>/', provide_access_user_view, name='provide_access_user'),
   path('provide_access_group/<int:id>/', provide_access_group_view, name='provide_access_group'),
   path('password_reset_confirm/<uidb64>/<token>/', password_reset_confirm_view, name='password_reset_confirm_'),
   path('home_page_content/', home_page_content, name='home_page_content'),
   path('legal_page_content/', legal_page_content, name='legal_page_content'),
   path('policy_page_content/', policy_page_content, name='policy_page_content'),
]
