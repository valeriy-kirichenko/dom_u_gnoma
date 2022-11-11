from googletrans import Translator


def image_directory_path(instance, filename):
    image_extension = filename.split('.')[1]
    translator = Translator()
    translation = translator.translate(instance.name)
    translation = '_'.join(translation.text.split(' '))
    return (
        f'{instance.name.capitalize()}/{translation.lower()}'
        f'_main_image.{image_extension}'
        )
