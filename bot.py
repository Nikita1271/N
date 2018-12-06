# -*- coding: utf-8 -*-
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.apihelper import ApiException
from pymongo import MongoClient
import pyqiwi
import os

from random import randint, choice
from time import time, sleep
from datetime import datetime
import re
import math
import threading
from string import ascii_letters, digits

y=os.environ['qiwi']

# bot = telebot.TeleBot(os.environ['TELEGRAM_TOKEN'])
x=os.environ['shop']
my_username = bot.get_me().username
print('@'+my_username)
# client = os.environ['database'
z=os.environ['mongo']
db = MongoClient(client).DevelopingRoom_Bot

main_admin = 687806733
qiwi = '+380672038493'
percent_per_ref=1

start_ts = datetime(2018, 11, 3).timestamp()

generate_code = lambda: randint(100000, 999999)


def button(key):
    r = db.buttons.find_one({'key': key})   
    if r is not None:
        return r['text']
    print(f'''Not found {key} button''')
    d = {
        'buy': 'Купить бота',
        'earn': 'Заработать',
        'add_balance': 'Пополнить баланс',
        'add_balance_confirm': 'Я понял!',
        'main_menu': '🏡Главное меню',
        'cancel': '❌Отмена',
        'balance': '💳Баланс',
        'stats': '📊Статистика',
        'admin': '⚙️Админка',
        'admin_edit_user': 'Изменить пользователя',
        'admin_post': 'Сделать рассылку',
        'admin_watch_string': 'Посмотреть строки',
        'admin_edit_string': 'Изменить строки',
        'admin_watch_button': 'Посмотреть кнопки',
        'admin_edit_button': 'Изменить кнопки',
        'admin_watch_inline_button': 'Посмотреть инлайн-кнопки',
        'admin_edit_inline_button': 'Изменить инлайн-кнопки'
    }
    if key in d:
        return d[key]
    return key


def inline_button(key):
    r = db.inline_buttons.find_one({'key': key})
    if r is not None:
        return r['text']
    print(f'''Not found {key} inline button''')
    d = {
        'withdraw_balance': 'Вывести деньги {soon}',
        'add_balance': 'Пополнить баланс',
        'add_balance_confirm': 'Я понял!',
        'cancel': '❌Отмена',
        'order_bot': 'Заказать своего бота',
        'bots_list': 'Список ботов',
        'back_to_bots_list': 'Назад к списку',
        'buy': 'Купить'
    }
    if key in d:
        return d[key]
    return key


def string(key):
    r = db.strings.find_one({'key': key})
    if r is not None:
        return r['text']
    print(f'''Not found {key} string''')
    d = {
        'main_menu': 'текст главного меню',
        'balance': 'Баланс: {0} руб.',
        'qiwi': '''Отправь нужное кол-во денег (в рублях) на номер <code>{0}</code>
Обязательно напиши в комментарии <code>{1}</code> 
Как только мы получим твой платеж, тебе придет уведомление''',
        'not_enough': 'К сожалению, на балансе недостаточно средств: {0} из {1} руб.',
        'add_balance_confirmation': 'Пока что пополнение баланса доступно только через QIWI. Если тебя все устраивает, и ты точно хочешь пополнить баланс, нажми на кнопку',
        'write_off': 'С баланса списано {0} руб.\nОсталось {1} руб.',
        'replenishment': 'Ваш баланс пополнен на {0} руб.\nНа балансе {1} руб.',
        'ref_replenishment': 'Новое зачисление от <a href="tg://user?id={0}">{1}</a>, реферала {2} уровня!',
        'cancelled': 'Отменено!',
        'bot_not_found': 'Бот не найден :(',
        'stats': '''📊Статистика проекта:
🌐Всего пользователей: {0}
📺Всего ботов: {1}
🤖Проведено сделок: {2}
Время работы: {3} д.''',
        'unknown_input': 'Неизвестный ввод, попробуйте еще раз',
        'flood_text': 'Не так быстро, пожалуйста',
        'buy_text': 'приветственный текст ла ла ла',
        'bot_text': '''Бот @{0}
Описание: {1}
Язык: {2}
Цена: {3} руб.

Баланс: {4} руб.''',
        'order_bot': '''Здесь ты можешь заказать у нас бота для своих целей. Все условия обсуждаются отдельно.
Напиши сюда краткое описание своего бота, и с тобой свяжется @username''',
        'bot_order_success': '''Заказ успешно отправлен!''',
        'bot_purchase_success': '''Бот @{0} успешно куплен.
В ближайшем времени с вами свяжется @username и передаст файл''',
        'new_purchase': '''Новая покупка от <a href="tg://user?id={0}">{1}</a>
Сумма: {2} руб.
Бот: @{3}''',
        'new_order': '''Новый заказ от <a href="tg://user?id={0}">{1}</a>
Текст:
{2}''',
        'earn': '''Приглашайте друзей по своей ссылке и зарабатывайте!
Вы получите {0}% с каждой покупки своих рефералов, а также их рефералов (до 5 уровней!)

Отправьте им эту ссылку:''',
        'withdraw_balance_num': 'Введи номер телефона, на который нужно вывести деньги',
        'withdraw_balance_sum': '''Введи сумму, которую нужно вывести\nВаш баланс: {0} руб.''',
        'wrong_data': 'Неверные данные',
        'withdraw_comment': 'Перевод от @{0}'
    }
    if key in d:
        return d[key]
    return key

def main_menu_kb(admin):
    main_menu = [
        [button('buy')],
        [button('balance'), button('stats')],
        [button('earn')]
    ]
    return parse_kb(main_menu if not admin else main_menu+[[button('admin')]])


def is_main_admin(uid):
    return uid == main_admin


def parse_kb(b):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(len(b)):
        kb.add(*[types.KeyboardButton(j) for j in b[i]])
    return kb


def parse_inline_kb(b):
    kb = InlineKeyboardMarkup()
    for i in range(len(b)):
        kb.add(*[(
            InlineKeyboardButton(inline_button(j), callback_data=j) if type(j) == str
            else InlineKeyboardButton(j[0], callback_data=j[1])
        ) for j in b[i]])
    return kb


# def pagination_kb_cb(type, p, total_pages):
#     return f"page_{type}_{p}" if (0 < p <= total_pages) else 'none'
#
#
# def pagination_kb(type, page, total_pages):
#     kb = InlineKeyboardMarkup()
#     kb.add(
#         InlineKeyboardButton("‹", callback_data=pagination_kb_cb(type, page-1, total_pages)),
#         InlineKeyboardButton(f'{page}/{total_pages}', callback_data="none"),
#         InlineKeyboardButton("›", callback_data=pagination_kb_cb(type, page+1, total_pages)))
#     return kb


def admin_kb():
    return parse_kb([[button('admin_edit_user')],
                     [button('admin_edit_bot')],
                     [button('admin_post')],
                     [button('admin_watch_string'), button('admin_edit_string')],
                     [button('admin_watch_button'), button('admin_edit_button')],
                     [button('admin_watch_inline_button'), button('admin_edit_inline_button')],
                     [button('main_menu')]])


def admin_user_kb(u):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton('Изменить баланс', callback_data=f'''user_{u['id']}_edit_balance'''))
    kb.add(InlineKeyboardButton('Удалить пользователя', callback_data=f'''user_{u['id']}_delete'''))
    kb.add(InlineKeyboardButton('✅ Админ' if u['is_admin'] else '⛔ Не админ',
                                callback_data=f'''user_{u['id']}_admin_{0 if u['is_admin'] else 1}'''))
    return kb


def admin_bot_kb(u):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton('Удалить бота', callback_data=f'''admin_bot_"{u['username']}"_delete'''))
    kb.add(InlineKeyboardButton('Изменить описание',
                                callback_data=f'''admin_bot_"{u['username']}"_edit_desc'''))
    kb.add(InlineKeyboardButton('Изменить язык',
                                callback_data=f'''admin_bot_"{u['username']}"_edit_price'''))
    kb.add(InlineKeyboardButton('Изменить цену',
                                callback_data=f'''admin_bot_"{u['username']}"_edit_price'''))
    kb.add(InlineKeyboardButton('Изменить название',
                                callback_data=f'''admin_bot_"{u['username']}"_edit_title'''))
    return kb


def admin_user_text(u):
    text = u['name']
    if u['username']:
        text += f''' (@{u['username']})\n'''
    text += f'''Баланс: {u['balance']} руб.'''
    return text


def admin_bot_text(u):
    return f'''Бот {u['username']}
Описание: {u['desc']}
Язык: {u['lang']}
Цена: {u['price']} руб.
Название (кнопка в списке ботов) {u['title']}'''


@bot.message_handler()
def message_handler(m):
    user = db.users.find_one({'id': m.from_user.id})
    if user is None:
        referrer_id = -1
        match = re.search(r'^/start ([a-zA-Z0-9]{7})$', m.text)
        if match:
            referrer = db.users.find_one({'invite_id': match.group(1)})
            if referrer:
                referrer_id = referrer['id']
        db.users.insert_one({
            'id': m.from_user.id,
            'name': m.from_user.first_name,
            'username': m.from_user.username,
            'is_admin': is_main_admin(m.from_user.id),
            'balance': 0,
            'last_message': -1,
            'mode': 'none',
            'mode_param': 'none',
            'invite_id': ''.join(choice(ascii_letters+digits) for _ in range(7)),
            'referrer': referrer_id
        })
        user = db.users.find_one({'id': m.from_user.id})
    if time() - user['last_message'] < 0.5:
        return bot.send_message(m.from_user.id, string('flood_text'))
    db.users.update_one({'id': m.from_user.id}, {'$set': {'name': m.from_user.first_name,
                                                          'username': m.from_user.username,
                                                          'last_message': time()}})
    user = db.users.find_one({'id': m.from_user.id})

    if m.text == button('cancel'):
        db.users.update_one({'id': user['id']}, {'$set': {'mode': 'none'}})
        bot.send_message(m.from_user.id, string('cancelled'), reply_markup=main_menu_kb(user['is_admin']))
    elif m.text == button('main_menu') or m.text.startswith('/start'):
        db.users.update_one({'id': user['id']}, {'$set': {'mode': 'none'}})
        bot.send_message(m.from_user.id, string('main_menu'), reply_markup=main_menu_kb(user['is_admin']))
    elif m.text == button('balance'):
        bot.send_message(
            m.from_user.id,
            string('balance').format(user['balance']),
            reply_markup=parse_inline_kb([['add_balance'],
                                          ['withdraw_balance']]))
    # elif m.text == button('add_balance'):
    #     bot.send_message(
    #         m.from_user.id,
    #         string('add_balance_confirmation'),
    #         reply_markup=parse_kb([[button('add_balance_confirm')], [button('main_menu')]]),
    #         parse_mode='HTML')
    # elif m.text == button('add_balance_confirm'):
    #     code = generate_code()
    #     db.payments.insert_one({
    #         'id': m.from_user.id,
    #         'code': code,
    #         'ts': time(),
    #         'completion_ts': None,
    #         'completed': False,
    #         'txn_id': -1
    #     })
    #     bot.send_message(m.from_user.id,
    #                      string('qiwi').format(qiwi, code),
    #                      reply_markup=parse_kb([[button('main_menu')]]),
    #                      parse_mode='HTML')
    # elif m.text == button('add'):
    #     db.users.update_one({'id': m.from_user.id}, {'$set': {'mode': 'adding'}})
    #     bot.send_message(m.from_user.id,
    #                      string('add').format(channel_add_cost, bot_add_cost, user['balance']),
    #                      reply_markup=parse_kb([[button('add_channel'), button('add_bot')],
    #                                             [button('cancel')]]))
    #     # if user['balance'] < add_cost:
    #     #     return bot.send_message(m.from_user.id,
    #     #                             string('not_enough').format(user['balance'], add_cost),
    #     #                             reply_markup=parse_kb([[button('add_balance')], [button('main_menu')]]))
    # elif m.text == button('channels'):
    #     c = [*db.channels.find({})]
    #     if len(c) == 0:
    #         return bot.send_message(m.from_user.id, string('no_channels'))
    #     items = c[0:items_per_page]
    #     bot.send_message(m.from_user.id,
    #                      '\n\n'.join(channel_text(channel) for channel in items),
    #                      reply_markup=pagination_kb('channels', 1, math.ceil(len(c)/items_per_page)))
    # elif m.text == button('bots'):
    #     b = [*db.bots.find({})]
    #     if len(b) == 0:
    #         return bot.send_message(m.from_user.id, string('no_bots'))
    #     items = b[0:items_per_page]
    #     bot.send_message(m.from_user.id,
    #                      '\n\n'.join(bot_text(bot) for bot in items),
    #                      reply_markup=pagination_kb('bots', 1, math.ceil(len(b)/items_per_page)))
    elif m.text == button('stats'):
        b = len([*db.bots.find()])
        u = len([*db.users.find()])
        t = len([*db.purchases.find()])
        bot.send_message(
            m.from_user.id,
            string('stats').format(u, b, t, math.ceil((time()-start_ts)/86400)))
    elif m.text == button('buy'):
        bot.send_message(m.from_user.id,
                         string('buy_text'),
                         reply_markup=parse_inline_kb([['order_bot'], ['bots_list']]))
    elif m.text == button('earn'):
        bot.send_message(
            m.from_user.id,
            string('earn').format(percent_per_ref))
        bot.send_message(m.from_user.id, f'''t.me/{my_username}?start={user['invite_id']}''')
    elif m.text == button('admin'):
        if not user['is_admin']:
            return
        bot.send_message(m.from_user.id,
                         button('admin'),
                         reply_markup=admin_kb())
    elif m.text == button('admin_edit_user'):
        if not user['is_admin']:
            return
        db.users.update_one({'id': m.from_user.id}, {'$set': {'mode': 'admin_choosing_user'}})
        bot.send_message(m.from_user.id,
                         'Введи id или юзернейм пользователя',
                         reply_markup=parse_kb([[button('cancel')]]))
    elif m.text == button('admin_edit_bot'):
        if not user['is_admin']:
            return
        db.users.update_one({'id': m.from_user.id}, {'$set': {'mode': 'admin_choosing_bot'}})
        bot.send_message(m.from_user.id,
                         'Введи юзернейм бота',
                         reply_markup=parse_kb([[button('cancel')]]))
    elif m.text == button('admin_post'):
        if not user['is_admin']:
            return
        db.users.update_one({'id': m.from_user.id}, {'$set': {'mode': 'admin_posting'}})
        bot.send_message(m.from_user.id,
                         'Введи сообщение для рассылки. Используется форматирование HTML.',
                         reply_markup=parse_kb([[button('cancel')]]))
    elif m.text == button('admin_edit_string'):
        if not user['is_admin']:
            return
        db.users.update_one({'id': m.from_user.id}, {'$set': {'mode': 'admin_edit_string_choosing'}})
        s = [*db.strings.find()]
        bot.send_message(m.from_user.id,
                         'Введи ключ строки или выбери из предложенных.',
                         reply_markup=parse_kb([[k['key']] for k in s]+[[button('cancel')]]))
    elif m.text == button('admin_edit_button'):
        if not user['is_admin']:
            return
        db.users.update_one({'id': m.from_user.id}, {'$set': {'mode': 'admin_edit_button_choosing'}})
        s = [*db.buttons.find()]
        bot.send_message(m.from_user.id,
                         'Введи ключ кнопки или выбери из предложенных.',
                         reply_markup=parse_kb([[k['key']] for k in s]+[[button('cancel')]]))
    elif m.text == button('admin_edit_inline_button'):
        if not user['is_admin']:
            return
        db.users.update_one({'id': m.from_user.id}, {'$set': {'mode': 'admin_edit_inline_button_choosing'}})
        s = [*db.inline_buttons.find()]
        bot.send_message(m.from_user.id,
                         'Введи ключ кнопки или выбери из предложенных.',
                         reply_markup=parse_kb([[k['key']] for k in s]+[[button('cancel')]]))
    elif m.text == button('admin_watch_string'):
        if not user['is_admin']:
            return
        db.users.update_one({'id': m.from_user.id}, {'$set': {'mode': 'admin_watching_string'}})
        s = [*db.strings.find()]
        bot.send_message(m.from_user.id,
                         'Введи ключ строки или выбери из предложенных.',
                         reply_markup=parse_kb([[k['key']] for k in s]+[[button('cancel')]]))
    elif m.text == button('admin_watch_button'):
        if not user['is_admin']:
            return
        db.users.update_one({'id': m.from_user.id}, {'$set': {'mode': 'admin_watching_button'}})
        s = [*db.inline_buttons.find()]
        bot.send_message(m.from_user.id,
                         'Введи ключ кнопки или выбери из предложенных.',
                         reply_markup=parse_kb([[k['key']] for k in s]+[[button('cancel')]]))
    elif m.text == button('admin_watch_inline_button'):
        if not user['is_admin']:
            return
        db.users.update_one({'id': m.from_user.id}, {'$set': {'mode': 'admin_watching_inline_button'}})
        s = [*db.inline_buttons.find()]
        bot.send_message(m.from_user.id,
                         'Введи ключ кнопки или выбери из предложенных.',
                         reply_markup=parse_kb([[k['key']] for k in s]+[[button('cancel')]]))
    elif re.search(r'/add (.+)\n(.+)\n(.+)\n(\d+)\n(.+)', m.text):
        if not user['is_admin']:
            return
        [title, desc, lang, price, username] = re.search(r'/add (.+)\n(.+)\n(.+)\n(\d+)\n(.+)', m.text).groups()
        db.bots.insert_one({
            'username': username,
            'title': title,
            'lang': lang,
            'price': int(price),
            'desc': desc
        })
        bot.send_message(m.from_user.id, f'''Бот успешно добавлен!''', reply_markup=parse_inline_kb([['bots_list']]))

    elif user['mode'] == 'withdraw_balance_waiting_num':
        num = re.sub(r'[\+\(\)\- ]', '', m.text)
        db.users.update_one({'id': user['id']}, {'$set': {'mode': 'withdraw_balance_waiting_sum',
                                                          'mode_param': num}})
        bot.send_message(m.from_user.id, string('withdraw_balance_sum').format(user['balance']), reply_markup=parse_kb([[button('cancel')]]))
    elif user['mode'] == 'withdraw_balance_waiting_sum':
        match = re.search(r'\d+\.?\d*', re.sub(r',', '.', m.text))
        if match is None:
            return bot.send_message(m.from_user.id, string('wrong_data'))
        sum = float(match.group(0))
        if sum > user['balance']:
            return bot.send_message(m.from_user.id, string('wrong_data'))
        print(wallet.send(pid="99", recipient='+79636424423', amount=1.11, comment='Привет!'))
        # print(wallet.send(99, recipient=user['mode_param'], amount=sum, comment=string('withdraw_comment').format(my_username)))
        db.users.update_one({'id': user['id']}, {'$set': {'mode': 'none'}})
    elif user['mode'] == 'ordering_bot':
        db.users.update_one({'id': m.from_user.id}, {'$set': {'mode': 'none'}})
        bot.send_message(m.from_user.id, string('bot_order_success'), reply_markup=main_menu_kb(user['is_admin']))
        bot.send_message(main_admin, string('new_order').format(m.from_user.id,
                                                                m.from_user.first_name,
                                                                m.text),
                         parse_mode='HTML')
    elif user['mode'] == 'admin_choosing_user':
        match1 = re.search(r'^\d+$', m.text)
        match2 = re.search(r'@([A-Za-z0-9_]{5,})', m.text)
        if match1 is None and match2 is None:
            return bot.send_message(m.from_user.id, string('wrong_data'))
        u = db.users.find_one({'id': int(match1.group(0))} if match1 is not None else {'username': match2.group(1)})
        if u is None:
            return bot.send_message(m.from_user.id, 'Пользователь не найден')
        bot.send_message(m.from_user.id, admin_user_text(u), reply_markup=admin_user_kb(u))
        print(u)
        pass
    elif user['mode'] == 'admin_choosing_bot':
        match = re.search(r'@([A-Za-z0-9_]{5,})', m.text)
        if match is None:
            return bot.send_message(m.from_user.id, string('wrong_data'))
        u = db.bots.find_one({'username': match.group(1)})
        if u is None:
            return bot.send_message(m.from_user.id, 'Бот не найден')
        bot.send_message(m.from_user.id, admin_bot_text(u), reply_markup=admin_bot_kb(u))
        print(u)
        pass
    elif user['mode'] == 'admin_editing_balance':
        match = re.search(r'^\d+$', m.text)
        if match is None:
            return bot.send_message(m.from_user.id, 'Неверный формат')
        amount = int(match[0])
        db.users.update_one({'id': user['mode_param']}, {'$set': {'balance': amount}})
        u = db.users.find_one({'id': user['mode_param']})
        bot.send_message(m.from_user.id, admin_user_text(u), reply_markup=admin_user_kb(u))
    elif user['mode'] == 'admin_posting':
        all_users = [*db.users.find()]
        n = 0
        db.users.update_one({'id': user['id']}, {'$set': {'mode': 'none'}})
        for u in all_users:
            print(u)
            try:
                bot.send_message(u['id'], m.text, parse_mode='HTML')
                n += 1
            except ApiException as e:
                print(e)
        db.posts.insert_one({'id': m.from_user.id, 'text': m.text, 'ts': time(), 'n_sent': n})
        bot.send_message(m.from_user.id,
                         f'Успешно отправлено {n} пользователям',
                         reply_markup=admin_kb())
    elif user['mode'] == 'admin_edit_string_choosing':
        key = m.text
        s = db.strings.find_one({'key': key})
        if s is None:
            return bot.send_message(m.from_user.id, 'Строка не найдена.')
        db.users.update_one({'id': m.from_user.id}, {'$set': {'mode': 'admin_edit_string_editing',
                                                              'mode_param': key}})
        bot.send_message(m.from_user.id,
                         f'''Введи новую строку. Текущее значение:\n\n{s['text']}''',
                         reply_markup=parse_kb([[button('cancel')]]),
                         parse_mode='HTML')
    elif user['mode'] == 'admin_edit_string_editing':
        val = m.text
        key = user['mode_param']
        s = db.strings.find_one({'key': key})
        if s is None:
            return bot.send_message(m.from_user.id, 'Строка не найдена.')
        db.users.update_one({'id': m.from_user.id}, {'$set': {'mode': 'none'}})
        db.strings.update_one({'key': key}, {'$set': {'text': val}})
        bot.send_message(m.from_user.id,
                         f'''Значение строки {key} успешно изменено''',
                         reply_markup=admin_kb())
    elif user['mode'] == 'admin_edit_button_choosing':
        key = m.text
        s = db.buttons.find_one({'key': key})
        if s is None:
            return bot.send_message(m.from_user.id, 'Кнопка не найдена.')
        db.users.update_one({'id': m.from_user.id}, {'$set': {'mode': 'admin_edit_button_editing',
                                                              'mode_param': key}})
        bot.send_message(m.from_user.id,
                         f'''Введи новую кнопку. Текущее значение:\n\n{s['text']}''',
                         reply_markup=parse_kb([[button('cancel')]]),
                         parse_mode='HTML')
    elif user['mode'] == 'admin_edit_button_editing':
        val = m.text
        key = user['mode_param']
        s = db.buttons.find_one({'key': key})
        if s is None:
            return bot.send_message(m.from_user.id, 'Кнопка не найдена.')
        db.users.update_one({'id': m.from_user.id}, {'$set': {'mode': 'none'}})
        db.buttons.update_one({'key': key}, {'$set': {'text': val}})
        bot.send_message(m.from_user.id,
                         f'''Значение кнопки {key} успешно изменено''',
                         reply_markup=admin_kb())
    elif user['mode'] == 'admin_edit_inline_button_choosing':
        key = m.text
        s = db.inline_buttons.find_one({'key': key})
        if s is None:
            return bot.send_message(m.from_user.id, 'Кнопка не найдена.')
        db.users.update_one({'id': m.from_user.id}, {'$set': {'mode': 'admin_edit_inline_button_editing',
                                                              'mode_param': key}})
        bot.send_message(m.from_user.id,
                         f'''Введи новую кнопку. Текущее значение:\n\n{s['text']}''',
                         reply_markup=parse_kb([[button('cancel')]]),
                         parse_mode='HTML')
    elif user['mode'] == 'admin_edit_inline_button_editing':
        val = m.text
        key = user['mode_param']
        s = db.inline_buttons.find_one({'key': key})
        if s is None:
            return bot.send_message(m.from_user.id, 'Кнопка не найдена.')
        db.users.update_one({'id': m.from_user.id}, {'$set': {'mode': 'none'}})
        db.inline_buttons.update_one({'key': key}, {'$set': {'text': val}})
        bot.send_message(m.from_user.id,
                         f'''Значение кнопки {key} успешно изменено''',
                         reply_markup=admin_kb())
    elif user['mode'] == 'admin_watching_string':
        key = m.text
        s = db.strings.find_one({'key': key})
        if s is None:
            return bot.send_message(m.from_user.id, 'Строка не найдена.')
        bot.send_message(m.from_user.id,
                         s['text'],
                         parse_mode='HTML')
    elif user['mode'] == 'admin_watching_button':
        key = m.text
        s = db.buttons.find_one({'key': key})
        if s is None:
            return bot.send_message(m.from_user.id, 'Кнопка не найдена.')
        bot.send_message(m.from_user.id,
                         s['text'],
                         parse_mode='HTML')
    elif user['mode'] == 'admin_watching_inline_button':
        key = m.text
        s = db.inline_buttons.find_one({'key': key})
        if s is None:
            return bot.send_message(m.from_user.id, 'Кнопка не найдена.')
        bot.send_message(m.from_user.id,
                         s['text'],
                         parse_mode='HTML')
    elif re.search(r'admin_bot_editing_(.+)', user['mode']):
        b = db.bots.find_one({'username': user['mode_param']})
        if b is None:
            return bot.send_message(m.from_user.id, string('bot_not_found'))
        [field] = re.search(r'admin_bot_editing_(.+)', user['mode']).groups()
        if field == 'price':
            try:
                val = int(m.text)
            except:
                return bot.send_message(m.from_user.id, string('wrong_data'))
        else:
            val = m.text
        db.bots.update_one({'username': user['mode_param']}, {'$set': {field: val}})
        bot.send_message(m.from_user.id, 'ok')
    else:
        db.users.update_one({'id': user['id']}, {'$set': {'mode': 'none'}})
        bot.send_message(m.from_user.id,
                         string('unknown_input'),
                         reply_markup=main_menu_kb(user['is_admin']))


@bot.callback_query_handler(lambda call: call.data == 'none')
def none_callback(call):
    bot.answer_callback_query(call.id, "")


# @bot.callback_query_handler(func=lambda call: re.search(r'page_(.+?)_(\d+)', call.data))
# def page_callback(call):
#     [type, page] = re.search(r'page_(.+?)_(\d+)', call.data).groups()
#     page = int(page)
#     if type == 'channels':
#         c = [*db.channels.find({})]
#         if len(c) == 0:
#             return bot.edit_message_text(string('no_channels'), call.from_user.id, call.message.message_id)
#         items = c[items_per_page*(page-1):items_per_page*page]
#         bot.edit_message_text('\n\n'.join(channel_text(channel) for channel in items),
#                               call.from_user.id,
#                               call.message.message_id,
#                               reply_markup=pagination_kb('channels', page, math.ceil(len(c)/items_per_page)))
#     elif type == 'bots':
#         b = [*db.bots.find({})]
#         if len(b) == 0:
#             return bot.edit_message_text(string('no_bots'), call.from_user.id, call.message.message_id)
#         items = b[items_per_page*(page-1):items_per_page*page]
#         bot.edit_message_text('\n\n'.join(bot_text(bot) for bot in items),
#                               call.from_user.id,
#                               call.message.message_id,
#                               reply_markup=pagination_kb('bots', page, math.ceil(len(b)/items_per_page)))
#     bot.answer_callback_query(call.id, "")


@bot.callback_query_handler(func=lambda call: re.search(r'user_(\d+?)_(.+)', call.data))
def user_callback(call):
    [uid, data] = re.search(r'user_(\d+?)_(.+)', call.data).groups()
    uid = int(uid)
    u = db.users.find_one({'id': uid})
    if u is None:
        return bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    if data == 'delete':
        db.users.delete_one({'id': uid})
        bot.edit_message_text('Пользователь {0} удален.'.format(u['name']),
                              call.from_user.id,
                              call.message.message_id)
    elif data == 'edit_balance':
        db.users.update_one({'id': call.from_user.id}, {'$set': {'mode': 'admin_editing_balance', 'mode_param': uid}})
        bot.edit_message_text(admin_user_text(u)+'\n\n Введи новый баланс:',
                              call.from_user.id,
                              call.message.message_id)
    elif re.search(r'admin_\d', data):
        val = re.search(r'admin_(\d)', data).group(1)
        db.users.update_one({'id': uid}, {'$set': {'is_admin': bool(int(val))}})
        u = db.users.find_one({'id': uid})
        bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=admin_user_kb(u))
    bot.answer_callback_query(call.id, "")


@bot.callback_query_handler(func=lambda call: re.search(r'^admin_bot_"(.+?)"_(.+)$', call.data))
def user_callback(call):
    [username, action] = re.search(r'admin_bot_"(.+?)"_(.+)', call.data).groups()
    print(username)
    user = db.users.find_one({'id': call.from_user.id})
    b = db.bots.find_one({'username': username})
    if b is None:
        return bot.answer_callback_query(call.id, string('bot_not_found'))
    bot.answer_callback_query(call.id, "")
    if action == 'delete':
        db.bots.delete_one({'username': username})
        return bot.edit_message_text('deleted',call.from_user.id, call.message.message_id)
    field = re.search(r'edit_(.+)', action).group(1)
    db.users.update_one({'id': call.from_user.id}, {'$set': {'mode': 'admin_bot_editing_'+field,
                                                             'mode_param': username}})
    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    bot.send_message(call.from_user.id, 'Введи новое значение')


@bot.callback_query_handler(func=lambda call: re.search(r'^bot_(.+)$', call.data))
def user_callback(call):
    [username] = re.search(r'bot_(.+)', call.data).groups()
    user = db.users.find_one({'id': call.from_user.id})
    b = db.bots.find_one({'username': username})
    if b is None:
        return bot.answer_callback_query(call.id, string('bot_not_found'))
    bot.answer_callback_query(call.id, "")
    bot.edit_message_text(string('bot_text').format(b['username'], b['desc'], b['lang'], b['price'], user['balance']),
                          call.from_user.id, call.message.message_id,
                          reply_markup=parse_inline_kb([
                              [(string('buy'), f'buy_{username}') if (user['balance'] >= b['price']) else (inline_button('not_enough_money'), 'none')],
                              ['back_to_bots_list']]),
                          parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: re.search(r'^buy_(.+)$', call.data))
def user_callback(call):
    [username] = re.search(r'buy_(.+)', call.data).groups()
    user = db.users.find_one({'id': call.from_user.id})
    b = db.bots.find_one({'username': username})
    if b is None:
        return bot.answer_callback_query(call.id, string('bot_not_found'))
    bot.answer_callback_query(call.id, "")
    if user['balance'] < b['price']:
        return bot.edit_message_text(string('not_enough_money'),
                                     call.from_user.id, call.message.message_id)
    db.users.update_one({'id': call.from_user.id}, {'$inc': {'balance': -b['price']}})
    db.purchases.insert_one({
        'ts': time(),
        'username': b['username'],
        'price': b['price'],
        'id': call.from_user.id
    })
    user = db.users.find_one({'id': call.from_user.id})
    bot.send_message(call.from_user.id,
                     string('write_off').format(b['price'], user['balance']),
                     reply_markup=main_menu_kb(user['is_admin']))
    bot.edit_message_text(string('bot_purchase_success').format(b['username']),
                          call.from_user.id, call.message.message_id)
    bot.send_message(main_admin, string('new_purchase').format(call.from_user.id,
                                                               call.from_user.first_name,
                                                               b['price'],
                                                               b['username']),
                     parse_mode='HTML')

    r_id = user['referrer']
    sum = b['price']*percent_per_ref/100
    for i in range(5):
        referrer = db.users.find_one({'id': r_id})
        if referrer is None:
            return
        db.users.update_one({'id': r_id}, {'$inc': {'balance': sum}})
        referrer = db.users.find_one({'id': r_id})

        bot.send_message(r_id,
                         string('ref_replenishment').format(user['id'], user['name'], i+1),
                         parse_mode='HTML')
        bot.send_message(r_id,
                         string('replenishment').format(sum, referrer['balance']),
                         reply_markup=main_menu_kb(user['is_admin']))
        db.ref_replenishments.insert_one({
            'ts': time(),
            'level': i+1,
            'id': referrer['id']
        })
        r_id = referrer['referrer']


@bot.callback_query_handler(func=lambda x:x)
def callback_query_callback(call):
    user = db.users.find_one({'id': call.from_user.id})
    data = call.data
    if data == 'cancel':
        db.users.update_one({'id': user['id']}, {'$set': {'mode': 'none'}})
        bot.edit_message_text(string('cancelled'), call.from_user.id, call.message.message_id)
    elif data == 'bots_list' or data == 'back_to_bots_list':
        bots = [*db.bots.find()]
        kb = []
        arr = []
        for b in bots:
            arr.append((b['title'], 'bot_'+b['username']))
            if len(arr) == 1:
                kb += [arr]
                arr = []
        kb += [arr]
        print(kb)
        bot.edit_message_text(string('buy_text'), call.from_user.id, call.message.message_id,
                              reply_markup=parse_inline_kb(kb))
    elif data == 'add_balance':
        bot.edit_message_text(
            string('add_balance_confirmation'),
            call.from_user.id, call.message.message_id,
            reply_markup=parse_inline_kb([['add_balance_confirm'], ['cancel']]),
            parse_mode='HTML')
    elif data == 'add_balance_confirm':
        code = generate_code()
        db.payments.insert_one({
            'id': call.from_user.id,
            'code': code,
            'ts': time(),
            'completion_ts': None,
            'completed': False,
            'txn_id': -1
        })
        bot.edit_message_text(
            string('qiwi').format(qiwi, code),
            call.from_user.id, call.message.message_id,
            parse_mode='HTML')
        # bot.send_message(call.from_user.id, string('main_menu'), reply_markup=main_menu_kb(user['is_admin']))
    elif data == 'order_bot':
        db.users.update_one({'id': call.from_user.id}, {'$set': {'mode': 'ordering_bot'}})
        bot.edit_message_text(
            string('order_bot'),
            call.from_user.id, call.message.message_id,
            reply_markup=parse_inline_kb([['cancel']]),
            parse_mode='HTML')
    elif data == 'withdraw_balance':
        db.users.update_one({'id': user['id']}, {'$set': {'mode': 'withdraw_balance_waiting_num'}})
        bot.edit_message_text(
            string('withdraw_balance_num'),
            call.from_user.id, call.message.message_id,
            reply_markup=parse_inline_kb([['cancel']]))

    bot.answer_callback_query(call.id, "")


def check_qiwi():
    while True:
        print(wallet.balance())
        history = wallet.history(20, 'IN')
        for t in history['transactions']:
            if t.status != 'SUCCESS':
                continue
            if t.comment is None:
                continue
            if t.sum.currency != 643:
                continue
            if db.payments.find_one({'txn_id': t.txn_id}):
                continue

            code = re.search(r'\d+', t.comment)
            if code is None:
                continue
            code = int(code[0])

            payment = db.payments.find_one({'code': code, 'completed': False})
            if not payment:
                continue
            db.payments.update(
                {
                    'code': code,
                    'completed': False
                },
                {'$set': {
                    'completed': True,
                    'completion_ts': time(),
                    'txn_id': t.txn_id
                }})
            amount = t.sum.amount
            db.users.update_one({'id': payment['id']}, {'$inc': {'balance': amount}})
            user = db.users.find_one({'id': payment['id']})
            bot.send_message(payment['id'],
                             string('replenishment').format(amount, user['balance']),
                             reply_markup=main_menu_kb(user['is_admin']))
        sleep(300)

if True:
    print('bot is working')
    t2 = threading.Thread(target=lambda: bot.polling(none_stop=True, timeout=600))
    t2.start()
    t1 = threading.Thread(target=check_qiwi())
    t1.start()


