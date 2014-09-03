from django.shortcuts import render
from eumkd.forms import EumkdSearchForm


def search(request):
    resources = []
    if request.GET:
        form = EumkdSearchForm(request.GET)
        if form.is_valid():
            resources = form.find_resources()
    else:
        form = EumkdSearchForm()

    return render(request, 'search.html', {'form': form, 'resources': resources})