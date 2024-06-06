import datetime
from aiogram import Router, F, Bot
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import database
import keyboards
import factories
import states
import parsing

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    answer_message = (f"Привет, <b>{message.from_user.first_name}</b>!"
                      f"\nВыбери группу, чтобы посмотреть расписание")

    answer_reply_markup = keyboards.create_command_start_keyboards()
    await message.answer(text=answer_message, parse_mode='html', reply_markup=answer_reply_markup)


@router.callback_query(factories.PaginationCallbackFactory.filter())
async def pagination_callback_handler(callback: CallbackQuery, callback_data: factories.PaginationCallbackFactory):
    current_date = datetime.datetime.strptime(callback_data.date, '%Y-%m-%d')

    if callback_data.action == 'next':
        current_date += datetime.timedelta(days=1)
        current_date = current_date.strftime('%Y-%m-%d')
    elif callback_data.action == 'back':
        current_date -= datetime.timedelta(days=1)
        current_date = current_date.strftime('%Y-%m-%d')

    # Потом думать
    login = callback_data.password
    password = callback_data.login

    data = get_message_and_markup(login, password, current_date)

    answer_message = data[0]
    answer_reply_markup = data[1]

    await callback.message.edit_text(text=answer_message, reply_markup=answer_reply_markup, parse_mode='html')


def generate_answer_message(schedules, current_date):
    answer_message = ''
    for schedule in schedules:
        date = schedule.get('date')
        if date == current_date:
            answer_message += f'\n\n<b>{schedule.get("subject_name")}</b>'
            answer_message += f'\n\n{" " * 20}{schedule.get("started_at")} - {schedule.get("finished_at")}'
            answer_message += f' ауд {schedule.get("room_name")}'
            answer_message += f'\n\n{" " * 20}{schedule.get("teacher_name")}'
    return answer_message if len(answer_message) > 0 else 'На этот день расписания нет!'


def get_message_and_markup(login, password, current_date=None):
    is_successful = parsing.get_token(login, password)

    if is_successful:
        token = is_successful[1]
        if current_date is None:
            current_date = str(datetime.datetime.utcnow().date())
        schedules = parsing.get_schedule(token, current_date)

        answer_message = generate_answer_message(schedules, current_date)
        answer_reply_markup = keyboards.pagination_keyboards(current_date, password, login)

        return answer_message, answer_reply_markup


@router.callback_query(factories.GroupsCallbackFactory.filter())
async def courses_callback_handler(callback: CallbackQuery, callback_data: factories.GroupsCallbackFactory):
    group_name = callback_data.title
    data = database.get_login_and_password(group_name)
    for account in data:
        login = account[0]
        password = account[1]

        data = get_message_and_markup(login, password)
        answer_message = data[0]
        answer_reply_markup = data[1]

        await callback.message.answer(text=answer_message, parse_mode='html', reply_markup=answer_reply_markup)


@router.callback_query(F.data == "add_group")
async def add_group_handler(callback: CallbackQuery, state: FSMContext, bot: Bot):
    answer_message = f'Пожалуйста, введите логин от аккаунта для добавления группы.'
    answer_chat_id = callback.from_user.id
    answer_message_id = callback.message.message_id
    await bot.edit_message_text(text=answer_message, chat_id=answer_chat_id, message_id=answer_message_id)
    await state.set_state(states.Authentication.login)
    await state.update_data(message_id=answer_message_id)


@router.message(states.Authentication.login)
async def login_handler(message: Message, state: FSMContext, bot: Bot):
    answer_message = f'Пожалуйста, введите пароль от аккаунта для добавления группы.'
    answer_chat_id = message.from_user.id
    answer_message_id = (await state.get_data())["message_id"]
    await message.delete()
    await bot.edit_message_text(text=answer_message, chat_id=answer_chat_id, message_id=answer_message_id)
    await state.set_state(states.Authentication.password)
    await state.update_data(login=message.text)


@router.message(states.Authentication.password)
async def password_handler(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    answer_chat_id = message.from_user.id
    answer_message_id = data["message_id"]

    login = data["login"]
    password = message.text

    is_successful = parsing.get_token(login, password)

    if is_successful:
        token = is_successful[1]
        info = parsing.get_user_info(token)
        group_name = info["group_name"]
        database.add_or_update_user(message.from_user.id, login, password, group_name)
        database.add_group(group_name)

        answer_message = f'Группа успешно добавлена!'
    else:
        answer_message = f'Не удалось добавить группу!'

    await message.delete()
    await bot.edit_message_text(text=answer_message, chat_id=answer_chat_id, message_id=answer_message_id)
    await cmd_start(message)
    await state.clear()
