import requests
from aiogram import Router
from aiogram.types import Message
from config import courses
import re
from aiogram import F




msg_router = Router()


# msg_handlers.py
import re

def clean_text(text):
    # Raqam emas belgilarini olib tashlash va kichik harflarga aylantirish
    cleaned_text = re.sub(r'[^0-9]+', '', text.lower())
    return cleaned_text

@msg_router.message()
async def convert_sum(message: Message):
    try:
        cleaned_text = clean_text(message.text)

        # Tekst ichida raqam bo'lsa
        if cleaned_text.isdigit():
            amount = int(cleaned_text)

            # Xabar "dollar" yoki "$" so'zini o'z ichiga olishi mumkin
            if any(keyword in message.text.lower() for keyword in ['dollar', '$']):
                converted_amount = {
                    'so`m': amount * 12334.09,
                    'evro': amount * 0.93,  # Konvertatsiya uchun ko'paytirishni ishlatamiz
                    'rubl': amount * 91.39   # Konvertatsiya uchun ko'paytirishni ishlatamiz
                }
                s = f"{amount} dollar:\n"
                for currency, value in converted_amount.items():
                    s += f"\t-{value: .2f} {currency}\n"
                await message.reply(s)
            else:
                await message.reply('Faqat dollar almashishini qo‘llang.')
        else:
            await message.reply(
                'Iltimos, faqat son va "dollar" yoki "$" so‘zini kiriting yoki /help buyrug‘ini bosing.')
    except Exception as e:
        print(e)
        await message.reply('Xatolik yuz berdi. Iltimos, qaytadan urinib ko‘ring.')
