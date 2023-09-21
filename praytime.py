from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bs4 import BeautifulSoup


class CurPray:
    def __init__(self, tm: str, activ=False, qolgan=None) -> None:
        self.tm = tm
        self.active = activ
        self.rem = qolgan

    @property
    def isActive(self):
        return self.active

    @property
    def Time(self):
        return self.tm

    @property
    def Remind(self):
        return self.rem

    def __str__(self) -> str:
        return self.Time


class PrayTime:
    def __init__(self, con: str) -> None:
        self.__html = con
        self.__date = {
            "Tong": None,
            "Quyosh": None,
            "Peshin": None,
            "Asr": None,
            "Shom": None,
            "Xufton": None,
        }

    def scrapping(self):
        b = BeautifulSoup(self.__html, "html.parser")
        all_pr_times = b.find_all("div", class_="prayer-times")
        for el in all_pr_times:
            bul = el.text.strip().split('\n')
            # print(bul)
            if len(bul) == 3:
                nom = bul[-1]
                df = CurPray(bul[1], activ=True, qolgan=bul[0])
                self.__date[nom] = df
            else:
                nom = bul[0]
                df = CurPray(bul[1])
                self.__date[nom] = df

    def get_keyboards(self):
        kbs = InlineKeyboardBuilder()
        for el in self.__date:
            sn: CurPray = self.__date[el]
            ans = el
            if sn.isActive:
                ans += " ✅ " + sn.Time +" \n Until the " + ans + " " + sn.Remind
            else:
                ans += " ⚠️ " + sn.Time
            btn = InlineKeyboardButton(text=ans, callback_data="pr:" + el)
            kbs.add(btn)
        kbs.adjust(1)
        return kbs.as_markup()
