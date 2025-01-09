import ptbot
import os
from dotenv import load_dotenv
from pytimeparse import parse


def reply(chat_id, bot):
    end_time_message = "Время вышло"
    bot.send_message(chat_id, end_time_message)


def notify_progress(seconds_left, chat_id, message_id, total_time, bot):
    progress_bar = render_progress_bar(
        total_time,
        total_time - seconds_left,
        prefix='',
        suffix='',
        length=30
    )
    message = f"Осталось {seconds_left} секунд.\n{progress_bar}"
    bot.update_message(chat_id, message_id, message)


def timer(chat_id, question, bot):
    time = parse(question)
    message_id = bot.send_message(chat_id, f"Осталось {time} секунд.")
    bot.create_countdown(
        time,
        notify_progress,
        chat_id=chat_id,
        message_id=message_id,
        total_time=time,
        bot=bot
    )
    bot.create_timer(time, reply, chat_id=chat_id, bot=bot)


def render_progress_bar(
        total,
        iteration,
        prefix='',
        suffix='',
        length=30,
        fill='█',
        zfill='░'
        ):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return f"{prefix} |{pbar}| {percent}% {suffix}"


def main():
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    bot = ptbot.Bot(telegram_token)

    bot.reply_on_message(lambda chat_id, question: timer(chat_id,
                                                         question,
                                                         bot
                                                         ))
    bot.run_bot()


if __name__ == '__main__':
    main()
