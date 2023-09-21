from asyncio import run

from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import API
from prayer_requests import Pray_Request
from praytime import PrayTime


class MainBot:
    def __init__(self, token=API) -> None:
        self.__dp = Dispatcher()
        self.__bt = Bot(token=token)
        ls_btn = ["Toshkent",
                  "Namangan",
                  "Farg'ona",
                  "Andijon",
                  "Samarqand",
                  "Buxoro",
                  "Sirdaryo",
                  "Navoiy",
                  "Jizzax",
                  "Qashqadaryo",
                  "Xorazim",
                  "Surxandaryo",
                  "Qora qalpog'iston Respublikasi"]
        box = InlineKeyboardBuilder()
        for reg in ls_btn:
            box.add(InlineKeyboardButton(text=reg, callback_data="reg:" + reg))
        box.adjust(3)
        self.bx = box.as_markup()

    async def start_msg(self, msg: Message):
        await msg.answer(text="Assalomu aleykum viloyatingizni tanlang!", reply_markup=self.bx)

    async def region_callback(self, clb: CallbackQuery):
        data = clb.data.split(":")
        vil = data[1]
        pr = Pray_Request(vil)
        pr.request()
        pt = PrayTime(pr.Content)
        pt.scrapping()
        await clb.message.answer(f"Ayni paytdagi {vil} namoz vaqtlari: ",
                                 reply_markup=pt.get_keyboards())
        await clb.answer(text="ANSWER")

    def register(self):
        self.__dp.message.register(self.start_msg, Command("start"))
        self.__dp.callback_query.register(self.region_callback)

    async def start(self):
        try:
            self.register()
            await self.__dp.start_polling(self.__bt)
        except:
            await self.__bt.session.close()


if __name__ == '__main__':
    mn = MainBot()
    run(mn.start())
