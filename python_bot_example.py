import datetime
import os
import json
from urllib.parse import quote

from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    WebAppInfo,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

SCHEDULES = (
    ("09:00", "13:00"),
    ("13:00", "17:00"),
    ("17:00", "21:00"),
)


def get_booking_props_encoded_uri():
    props = {
        "schedules": SCHEDULES,
        "gazebos": [
            ["0", "Альтанка 1", "відкрита, 6 чол", [False, False, True]],
            ["1", "Альтанка 2", "заскляна, 6 чол", [True, True, True]],
            ["2", "Альтанка 3", "відкрита, 6 чол", [True, False, True]],
            ["3", "Альтанка 4", "відкрита, 6 чол", [False, False, False]],
            ["4", "Альтанка 5", "відкрита, 6 чол", [True, True, False]],
            ["5", "Альтанка 6", "відкрита, 6 чол", [True, True, True]],
            ["6", "Альтанка 7", "відкрита, 6 чол", [True, False, False]],
            ["7", "Альтанка 8", "відкрита, 6 чол", [True, True, True]],
            ["8", "Альтанка 9", "відкрита, 6 чол", [False, False, True]],
            ["9", "Альтанка 10", "відкрита, 6 чол", [True, True, True]],
        ],
        "date": datetime.date.today().isoformat(),
    }
    jsonified = json.dumps(props, separators=(",", ":"))
    return quote(jsonified)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Бронювання",
        reply_markup=ReplyKeyboardMarkup.from_button(
            KeyboardButton(
                text="Забронювати",
                web_app=WebAppInfo(
                    url="https://seedofjoy.github.io/ft-book-demo?s={state}".format(
                        state=get_booking_props_encoded_uri(),
                    ),
                ),
            )
        ),
    )


async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = json.loads(update.effective_message.web_app_data.data)

    gazeboId = data["gazeboId"]
    date = data["date"]
    scheduleOptionIdx = data["scheduleOptionIdx"]

    fromTime, toTime = SCHEDULES[scheduleOptionIdx]

    await update.message.reply_html(
        text=f"Ви успішно забронювали <code>Альтанку {gazeboId}</code> на <b>{date}</b> з {fromTime} по {toTime}",
        reply_markup=ReplyKeyboardRemove(),
    )


def main():
    application = Application.builder().token(os.environ["BOT_TOKEN"]).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data)
    )

    application.run_polling()
