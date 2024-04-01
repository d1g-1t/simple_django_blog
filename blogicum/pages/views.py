from django.shortcuts import render

from django.views.generic import TemplateView


class AboutPage(TemplateView):
    """
    Класс для отображения страницы "О проекте"
    """
    template_name = 'pages/about.html'


class RulesPage(TemplateView):
    """
    Класс для отображения страницы "Правила"
    """
    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    """
    Функция для отображения страницы 404
    """
    return render(request, "pages/404.html", status=404)


def server_error(request, reason=""):
    """
    Функция для отображения страницы 500
    """
    return render(request, "pages/500.html", status=500)


def csrf_failure(request, reason=""):
    """
    Функция для отображения страницы 403
    """
    return render(request, "pages/403csrf.html", status=403)
