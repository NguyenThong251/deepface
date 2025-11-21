from typing import Any, Dict, Optional


def is_user_admin(module_info: Optional[Dict[str, Any]]) -> bool:
    if not module_info:
        return False

    permission = module_info.get('permission', {})

    return all([
        permission.get('listViewable', False),
        permission.get('detailView', False),
        permission.get('updateable', False),
        permission.get('createable', False),
        permission.get('deleteable', False),
    ])
