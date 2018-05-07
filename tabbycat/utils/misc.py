import logging

from django.core.exceptions import SuspiciousFileOperation
from django.urls import reverse
from django.utils import formats, timezone, translation
from django.shortcuts import redirect

from ipware.ip import get_real_ip
from whitenoise.storage import CompressedManifestStaticFilesStorage

logger = logging.getLogger(__name__)


def get_ip_address(request):
    ip = get_real_ip(request)
    if ip is None:
        return "0.0.0.0"
    return ip


def redirect_tournament(to, tournament, *args, **kwargs):
    return redirect(to, tournament_slug=tournament.slug, *args, **kwargs)


def reverse_tournament(to, tournament, *args, **kwargs):
    kwargs.setdefault('kwargs', {})
    kwargs['kwargs']['tournament_slug'] = tournament.slug
    return reverse(to, *args, **kwargs)


def redirect_round(to, round, *args, **kwargs):
    return redirect(to, tournament_slug=round.tournament.slug,
                    round_seq=round.seq, *args, **kwargs)


def reverse_round(to, round, *args, **kwargs):
    kwargs.setdefault('kwargs', {})
    kwargs['kwargs']['tournament_slug'] = round.tournament.slug
    kwargs['kwargs']['round_seq'] = round.seq
    return reverse(to, *args, **kwargs)


class SquashedWhitenoiseStorage(CompressedManifestStaticFilesStorage):
    """ Hack to get around dependencies throwing collectstatic errors """

    def url(self, name, **kwargs):
        try:
            return super(SquashedWhitenoiseStorage, self).url(name, **kwargs)
        except SuspiciousFileOperation:
            # Triggers within jet CSS files link to images outside path
            return name
        except ValueError:
            # Seems to happen as a byproduct of other errors when using daphne
            # So to prevent doubling up of the error; supress it
            pass


def badge_datetime_format(timestamp):
    lang = translation.get_language()
    for module in formats.get_format_modules(lang):
        fmt = getattr(module, "BADGE_DATETIME_FORMAT", None)
        if fmt is not None:
            break
    else:
        logger.error("No BADGE_DATETIME_FORMAT found for language: %s", lang)
        fmt = "d/m H:i"   # 18/02 16:33, as fallback in case nothing is defined

    localized_time = timezone.localtime(timestamp)
    return formats.date_format(localized_time, format=fmt)
