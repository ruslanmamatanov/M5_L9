import requests
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from config import courses
import re
from aiogram import F
from datetime import datetime


cmd_router = Router()

@cmd_router.message(CommandStart())
async def cmd_start(message: Message):
    s = "Assalomu alaykum!\nValyuta kurslari haqida ma'lumot beruvchi botimizga xush kelibsiz!\nYordam uchun /help buyrug'ini bosing!"
    await message.answer(s)

@cmd_router.message(Command('help'))
async def cmd_help(message: Message):
    s = ("Quyidagi komandalar yordamida botdan samarali foydalanishingiz mumkin:\n\n"
         "\t/kurslar - valyuta kursalrini bilish\n"
         "\t/dollar - dollar kursini bilish\n"
         "\t/yevro - yevro kursini bilish\n"
         "\t/rubl - rubl kursini bilish\n\n"
         "\nAgar biron summani jo'natsangiz, bot uni turli valyutalardagi qiymatini qaytaradi. (Masalan, 1000000) ")
    await message.reply(s)

@cmd_router.message(Command('kurslar'))
async def cmd_kurslar(message: Message):
    response = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/")
    s = "Bugungi valyuta kurslari:\n"
    print(response.json())
    for kurs in response.json():
        if kurs["Ccy"] in ['USD', 'EUR', 'RUB']:
            courses[kurs["Ccy"]] = float(kurs['Rate'])
            s += f"1 {kurs['CcyNm_UZ']} - {kurs['Rate']} so'm\n"

    await message.answer(s)

@cmd_router.message(Command('dollar'))
async def cmd_dollar(message: Message):
    s = f"1 AQSh dollari = {courses['USD']} so'm"
    await message.reply(s)

@cmd_router.message(Command('yevro'))
async def cmd_yevro(message: Message):
    s = f"1 EVRO = {courses['EUR']} so'm"
    await message.reply(s)

@cmd_router.message(Command('rubl'))
async def cmd_yevro(message: Message):
    s = f"1 Rossiya rubli = {courses['RUB']} so'm"
    await message.reply(s)



@cmd_router.message(Command('sana') & F.regex(r'\d{4}-\d{2}-\d{2}'))
async def cmd_date(message: Message):
    try:
        date_str = re.search(r'\d{4}-\d{2}-\d{2}', message.text).group()
        target_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

        response = requests.get(f"https://cbu.uz/uz/arkhiv-kursov-valyut/json/{date_str}/")
        s = f"Valyuta kurslari {target_date} sanasiga:\n"
        for kurs in response.json():
            if kurs["Ccy"] in ['USD', 'EUR', 'RUB']:
                s += f"1 {kurs['CcyNm_UZ']} - {kurs['Rate']} so'm\n"

        await message.answer(s)
    except Exception as e:
        print(e)
        await message.reply('Xatolik yuz berdi. Iltimos, qaytadan urinib ko‘ring.')


@cmd_router.message(Command('hafta'))
async def cmd_weekly_rates(message: Message):
    try:
        today = datetime.date.today()
        start_date = today - datetime.timedelta(days=today.weekday())
        end_date = start_date + datetime.timedelta(days=6)

        s = f"Bu haftaning valyuta kurslari:\n"
        for date in [start_date + datetime.timedelta(days=n) for n in range(7)]:
            response = requests.get(f"https://cbu.uz/uz/arkhiv-kursov-valyut/json/{date.strftime('%Y-%m-%d')}/")
            s += f"\n{date}:"
            for kurs in response.json():
                if kurs["Ccy"] in ['USD', 'EUR', 'RUB']:
                    s += f"\n\t1 {kurs['CcyNm_UZ']} - {kurs['Rate']} so'm"

        await message.answer(s)
    except Exception as e:
        print(e)
        await message.reply('Xatolik yuz berdi. Iltimos, qaytadan urinib ko‘ring.')



