import asyncio
import json
import logging

from aiogram import *
from aiogram.enums import *
from aiogram.filters import *
from aiogram.filters import callback_data
from aiogram.types import *
from aiogram.types import message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import *
from aiogram.types.input_media_photo import *
from aiogram.types import input_media_photo

from config import *
from resources.TEXT_MESSAGES import *
from send_logs import *
from kb_builder import *
from send_data import *
from StatesGroup import *

@dp.message(CommandStart())
async def main_menu(message: Message) -> None:
    try:
        global user_id, message_id
        user_id = str(message.from_user.id)
        chat_id = message.chat.id
        member = await bot.get_chat_member(chat_id, user_id)
        username = member.user.username

        image_path = 'resources/TechSupport.png'
        
        photo = FSInputFile(image_path)
        await message.answer_photo(photo, caption=HELLO_MESSAGE, reply_markup=await main_kb())
        
        logger.debug(f"{user_id} - main menu")

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()

@dp.callback_query(F.data == "SuggestIdea")
async def GetUserIdea(callback: types.CallbackQuery, state: FSMContext):
    try:
        await state.set_state(GetIdea.wait_for_message)

        logger.debug(f"{user_id} - idea suggest")

        if callback.message.text:
            await callback.message.edit_text(IDEA_TEXT)
        else:
            await callback.message.answer(IDEA_TEXT)

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()

@dp.callback_query(F.data == "BugReport")
async def GetUserIdea(callback: types.CallbackQuery, state: FSMContext):
    try:
        await state.set_state(GetBug.wait_for_message)
        
        logger.debug(f"{user_id} - bug report")

        if callback.message.text:
            await callback.message.edit_text(BUG_TEXT)
        else:
            await callback.message.answer(BUG_TEXT)

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()


@dp.message(GetIdea.wait_for_message)
async def IdeaUserMessage(message: Message, state: FSMContext):
    try:
        username = message.from_user.username
        logger.debug(f"Idea suggest from {username}: {message.text}")

        try:
            await send_messages(message, username, "🍀 IDEA 🍀")
        except Exception as e:
            logging.error(f"Error forwarding message from {username} to {CHANNEL}: {e}")

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()


@dp.message(GetBug.wait_for_message)
async def BugUserMessage(message: types.Message, state: FSMContext):
    try:
        username = message.from_user.username
        logger.debug(f"Bug report from {username}: {message.text}")

        try:
            await send_messages(message, username, "❌ BUG ❌")
        except Exception as e:
            logging.error(f"Error forwarding message from {username} to {CHANNEL}: {e}")

    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()

@dp.callback_query(F.data == "Back")
async def BackToStartMenu(callback: types.CallbackQuery):
    try:
        await main_menu(callback.message)
    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()

@dp.callback_query(F.data == "Contacts")
async def Contacts(callback: types.CallbackQuery):
    try:
        logger.debug(f"{user_id} - contacts")

        await callback.message.answer(DEVS_TEXT, reply_markup=await back_btn(), disable_web_page_preview=True)
    except Exception as err:
        logger.error(f"{err}")
        await send_log_to_dev()
