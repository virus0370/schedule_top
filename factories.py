from aiogram.filters.callback_data import CallbackData


class GroupsCallbackFactory(CallbackData, prefix="groups"):
    title: str


class PaginationCallbackFactory(CallbackData, prefix="pagination"):
    action: str
    date: str
    login: str
    password: str