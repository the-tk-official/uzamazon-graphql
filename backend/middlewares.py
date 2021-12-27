from .permissions import resolve_paginated


class CustomPaginationMiddleware(object):
    """Custom middleware for finding query with pagination and add page"""

    def resolve(self, next, root, info, **kwargs):
        try:
            is_paginated = info.return_type.name[-9:]
            is_paginated = is_paginated == 'Paginated'
        except Exception:
            is_paginated = False

        if is_paginated:
            page = kwargs.pop('page', 1)
            return resolve_paginated(query_data=next(root, info, **kwargs).value, info=info, page_info=page)

        return next(root, info, **kwargs)
