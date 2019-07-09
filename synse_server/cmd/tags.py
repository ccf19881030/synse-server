
from synse_server import cache
from synse_server.i18n import _
from synse_server.log import logger


async def tags(*namespaces, with_id_tags=False):
    """Generate the tags response data.

    Args:
        namespaces (str): The namespace(s) of the tags to filter by.
        with_id_tags (bool): Flag to toggle the inclusion/exclusion of ID tags.

    Returns:
        list[str]: A list of all tags currently associated with devices.
    """
    logger.debug(
        _('issuing command'), command='TAGS',
        namespaces=namespaces, with_id=with_id_tags,
    )

    cached_tags = cache.get_cached_device_tags()

    def matches_ns(t):
        if '/' in t:
            ns = t.split('/')[0]
        else:
            ns = 'default'
        return ns in namespaces

    if not with_id_tags:
        cached_tags = filter(lambda t: not t.startswith('system/id:'), cached_tags)

    if namespaces:
        cached_tags = filter(lambda t: matches_ns(t), cached_tags)

    return sorted(cached_tags)