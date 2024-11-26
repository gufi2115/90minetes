import os
from dotenv import load_dotenv

load_dotenv()


def init_django():
    import django
    from django.conf import settings

    if settings.configured:
        return

    settings.configure(
        INSTALLED_APPS=[
            'db',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.getenv('NAME'),
                'USER': os.getenv('USER'),
                'PASSWORD': os.getenv('PASSWORD'),
                'HOST': os.getenv('HOST'),
                'PORT': os.getenv('PORT')
            }
        }
    )
    django.setup()


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    init_django()
    execute_from_command_line()
