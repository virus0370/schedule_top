import calendar
from datetime import datetime

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
import factories
import database


def create_command_start_keyboards() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    groups = database.fetch_all_group_tokens_and_names()

    if groups:
        for group in groups:
            title = group[0]

            builder.add(InlineKeyboardButton(text=title,
                                             callback_data=factories.GroupsCallbackFactory(title=title).pack()))
    builder.add(InlineKeyboardButton(text="Добавить группу",
                                     callback_data="add_group"))

    builder.adjust(1)
    return builder.as_markup()


def calendar_keyboard(current_month: int = None, current_year: int = None) -> InlineKeyboardMarkup:
    month_names = [
        "Январь", "Февраль", "Март", "Апрель",
        "Май", "Июнь", "Июль", "Август",
        "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
    ]
    weekday_names = [
        "Пн", "Вт", "Ср",
        "Чт", "Пт", "Сб",
        "Вс"
    ]
    if current_month is None and current_year is None:
        current_date = datetime.utcnow()
        current_month = current_date.month
        current_year = current_date.year

    prev_year = current_year - 1 if current_month == 1 else current_year
    next_year = current_year + 1 if current_month == 12 else current_year
    prev_month = current_month - 1 if current_month != 1 else 12.
    next_month = current_month + 1 if current_month != 12 else 1
    calendar_data = calendar.monthcalendar(current_year, current_month)

    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='◀️', callback_data=factories.Pagination(action='prev', number_month=prev_month,
                                                                           number_year=prev_year).pack()),
        InlineKeyboardButton(text=f'{month_names[current_month - 1]}', callback_data='abc'),
        InlineKeyboardButton(text=f'{current_year}', callback_data='abc'),
        InlineKeyboardButton(text='◀️', callback_data=factories.Pagination(action='next', number_month=next_month,
                                                                           number_year=next_year).pack())
        )

    for week in weekday_names:
        builder.add(InlineKeyboardButton(text=week, callback_data='abc'))

    for week in calendar_data:
        for day in week:
            _text = str(day) if day != 0 else ' '
            builder.add(InlineKeyboardButton(text=_text, callback_data='abc'))

    builder.adjust(4, 7)
    return builder.as_markup()


def pagination_keyboards(current_date: str, login: str, password: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='◀️',
                                     callback_data=factories.PaginationCallbackFactory(action='back',
                                                                                       date=current_date,
                                                                                       login=login,
                                                                                       password=password).pack()))
    builder.add(InlineKeyboardButton(text=current_date, callback_data=current_date))
    builder.add(InlineKeyboardButton(text='▶️',
                                     callback_data=factories.PaginationCallbackFactory(action='next',
                                                                                       date=current_date,
                                                                                       login=login,
                                                                                       password=password).pack()))
    builder.adjust(3)
    return builder.as_markup()
