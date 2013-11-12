from django.contrib.admin import AdminSite


class CustomAdminSite(AdminSite):
    login_template = 'admin/custom_login.html'


site = CustomAdminSite()