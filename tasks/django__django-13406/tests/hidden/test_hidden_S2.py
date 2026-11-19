import django
from django.conf import settings
from django.template import TemplateDoesNotExist
from django.test import RequestFactory, override_settings
from django.views.defaults import server_error


def test_server_error_propagates_missing_included_template():
    if not settings.configured:
        settings.configure(
            SECRET_KEY='error-page-test',
            INSTALLED_APPS=[],
            USE_I18N=False,
        )
    django.setup()

    missing_template = 'errors/support_details.html'
    templates = [{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': False,
        'OPTIONS': {
            'loaders': [
                ('django.template.loaders.locmem.Loader', {
                    '500.html': (
                        '<h1>Service unavailable</h1>'
                        "{% include 'errors/support_details.html' %}"
                    ),
                }),
            ],
        },
    }]

    caught = None
    with override_settings(DEBUG=False, TEMPLATES=templates):
        request = RequestFactory().get('/failed-operation/')
        try:
            server_error(request)
        except TemplateDoesNotExist as exc:
            caught = exc

    assert caught is not None, 'Rendering failures must not become a generic error page.'
    assert missing_template in str(caught)
