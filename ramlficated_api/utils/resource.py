# -*- coding: utf-8 -*-


def resource_restructure(api, replacer=None):
    _resources = {}
    for resource in api.resources:
        # fix ramls url param pattern syntax for ids in raml {} to
        # flask [('{', '<'), ('}', '>')] or
        # tornado [('{', '(?P<'), ('}', '>[^\/]+)')]
        if replacer:
            resource_path = resource.path
            for x, y in replacer:
                resource_path = resource_path.replace(x, y)
        _resources_pr = _resources.get(resource_path, {})
        _resources_pr.update({resource.method.upper(): resource})
        _resources[resource_path] = _resources_pr
    return _resources
