from django.conf import settings
from django.shortcuts import render
from django.views import static

from kuma.core.sections import SECTION_USAGE
from kuma.core.cache import memcache
from kuma.demos.models import Submission
from kuma.feeder.models import Bundle
from kuma.search.models import FilterGroup
from kuma.search.serializers import GroupWithFiltersSerializer


def home(request):
    """Home page."""
    demos = Submission.objects.all_sorted(sort='recentfeatured', max=12)

    updates = []
    for s in SECTION_USAGE:
        updates += Bundle.objects.recent_entries(s.updates)[:5]

    community_stats = memcache.get('community_stats')

    if not community_stats:
        community_stats = {'contributors': 5453, 'locales': 36}

    groups = FilterGroup.objects.all()
    serializer = GroupWithFiltersSerializer(groups, many=True)

    context = {
        'demos': demos,
        'updates': updates,
        'stats': community_stats,
        'command_search_filters': serializer.data
    }
    return render(request, 'landing/homepage.html', context)


def contribute_json(request):
    return static.serve(request, 'contribute.json',
                        document_root=settings.ROOT)


def promote_buttons(request):
    """Bug 646192: MDN affiliate buttons"""
    return render(request, 'landing/promote_buttons.html')


def fellowship(request):
    return render(request, 'landing/fellowship.html')
