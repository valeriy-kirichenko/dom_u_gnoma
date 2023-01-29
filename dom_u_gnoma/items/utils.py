from googletrans import Translator


def image_directory_path(instance, filename):
    """Возвращает директорию для сохранения картинки изделия и переводит
    имя изделия на английский для использования в названии файла.

    Args:
        instance (Item): обьект изделия.
        filename (str): имя файла.

    Returns:
        str: путь для сохранения картинки.
    """

    image_extension = filename.split('.')[1]
    translator = Translator()
    translation = translator.translate(instance.name)
    translation = '_'.join(translation.text.split(' '))
    return (
        f'{instance.name.capitalize()}/{translation.lower()}'
        f'_main_image.{image_extension}'
        )


def get_and_update_session(request):
    """Добавляет в сессию текущий url.

    Args:
        request (HttpRequest): обьект запроса.

    Returns:
        SessionStore: обьект сессии.
    """

    session = request.session  # получаем обьект сессии.
    session['path'] = request.path  # сохраняем текущий url в сессии.
    session.modified = True
    return session
