from django.shortcuts import render


def index(request):
    """View-функция для отображения главной страницы.

    Args:
        request (HttpRequest): обьект запроса.

    Returns:
        HttpResponse: обьект ответа, главная страница.
    """

    return render(request, 'about/index.html', {'user': request.user})
