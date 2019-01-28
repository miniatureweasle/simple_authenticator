"""
The `urlpatterns` list routes URLs to views.
"""
import views

urlpatterns = [
    ('POST', '/signup', views.signup),
    ('POST', '/login', views.login),
    ('GET', '/verify', views.verify),
]
