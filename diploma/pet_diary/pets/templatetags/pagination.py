from django import template


register = template.Library()


@register.inclusion_tag('pets/pagination.html', takes_context=True)
def render_pagination(context, page_obj, tab, per_page_param, page_param):
    request = context['request']
    query_params = request.GET.copy()
    query_params.pop(page_param, None)
    query_params.pop(per_page_param, None)
    return {
        'page_obj': page_obj,
        'tab': tab,
        'per_page_param': per_page_param,
        'page_param': page_param,
        'query_string': query_params.urlencode(),
    }