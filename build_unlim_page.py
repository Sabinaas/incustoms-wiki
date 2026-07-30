"""Собирает unlim.html из авторской презентации Unlim (standalone) для GitHub Pages.

Зачем скрипт, а не ручное копирование: презентацию пересобирают, и при каждом обновлении нужно
повторить ровно две правки — иначе они потеряются.

1. Первая кнопка «Подключить Unlim» ведёт в бот с параметром start=pay_unlim: бот по нему сразу
   открывает экран оплаты (Payme и Click). Напрямую на payme.uz/click.uz вести нельзя — платёж
   привязывается к заказу и Telegram ID, иначе после оплаты вебхуку некому включать подписку.
2. Внизу добавляется закреплённая кнопка оплаты: она видна на любом слайде, а не только на
   последнем, куда доскроллит не каждый.

Запуск: python build_unlim_page.py "<путь к InCustom-Helper-Unlim-standalone.html>"
"""

from __future__ import annotations

import pathlib
import sys

BOT = "https://t.me/incustom_helper_bot"
PAY = BOT + "?start=pay_unlim"
OUT = pathlib.Path(__file__).resolve().parent / "unlim.html"

PAY_BAR = """
<!-- Закреплённая кнопка оплаты: добавляется сборщиком (build_unlim_page.py), в самой
     презентации её нет. Ведёт в бот с start=pay_unlim → экран оплаты Payme/Click. -->
<style>
  #pay-bar{position:fixed;left:0;right:0;bottom:0;z-index:99999;display:flex;justify-content:center;
    padding:12px 14px calc(12px + env(safe-area-inset-bottom));
    background:linear-gradient(to top,rgba(15,58,42,.96),rgba(15,58,42,.72),transparent);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
  #pay-bar a{display:flex;align-items:center;gap:10px;max-width:520px;width:100%;
    justify-content:center;padding:16px 22px;border-radius:999px;background:#E4702B;
    color:#FFF8F0;text-decoration:none;font-weight:600;font-size:17px;
    box-shadow:0 10px 26px -12px rgba(0,0,0,.6)}
  #pay-bar small{display:block;text-align:center;font-weight:400;opacity:.85;font-size:13px}
</style>
<div id="pay-bar">
  <a href="__PAY__">💳 Подключить Unlim — 77 000 сум/мес
    <small>Payme или Click, в Telegram</small></a>
</div>
"""


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("укажите путь к InCustom-Helper-Unlim-standalone.html")
    src = pathlib.Path(sys.argv[1])
    s = src.read_text(encoding="utf-8")

    # Только ПЕРВАЯ ссылка — это кнопка «Подключить Unlim». Вторая («задать вопрос») и подпись
    # @incustom_helper_bot в подвале должны вести в обычный чат, а не на оплату.
    if s.count(BOT) < 1:
        raise SystemExit("в презентации не найдена ссылка на бота — проверьте сборку")
    s = s.replace(BOT, PAY, 1)

    if "</body>" not in s:
        raise SystemExit("нет </body> — не знаю, куда вставить кнопку оплаты")
    s = s.replace("</body>", PAY_BAR.replace("__PAY__", PAY) + "</body>", 1)

    OUT.write_text(s, encoding="utf-8")
    print(f"готово: {OUT.name}, {len(s)} знаков · кнопка оплаты → {PAY}")


if __name__ == "__main__":
    main()
