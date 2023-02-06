from sqladmin import ModelView

from app.config import settings as s
from app.module.models.user import User

permission = s.IS_LOCAL


class BaseView(ModelView):
    can_create = permission
    can_delete = permission
    # can_edit = permission


class UserView(BaseView, model=User):
    column_list = [User.id, User.name]
    form_columns = [User.name]
    column_details_list = [User.name]
    column_searchable_list = [User.name]
    column_sortable_list = [User.id, User.name]
    name_plural = "Пользователи"


VIEWS = [
    UserView,
]
