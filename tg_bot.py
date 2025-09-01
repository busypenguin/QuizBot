import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import CallbackContext, ConversationHandler, RegexHandler
from config import TELEGRAM_BOT_TOKEN
from quiz_loader import quiz
from redis_manager import r


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    custom_keyboard = [['Новый вопрос', 'Сдаться'],
                       ['Мой счёт']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_markdown_v2(
        fr'Здравствуйте, {user.mention_markdown_v2()}\! Я бот для викторин\!',
        reply_markup=reply_markup,
    )
    return CHOOSING


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def handle_new_question_request(update: Update, context: CallbackContext):
    """Send a new questions"""
    question = random.choice(list(quiz))
    chat_id = update.effective_chat.id
    update.message.reply_text(question)
    r.set(chat_id, question)
    # anrwer = (quiz[question])
    # print(anrwer)
    return ANSWER


def handle_solution_attempt(update: Update, context: CallbackContext):
    """       """
    if update.message.text == (quiz[r.get(update.effective_chat.id)]):
        update.message.reply_text('Правильно! Поздравляю! Для следующего '
                                  'вопроса нажми «Новый вопрос»')
        return CHOOSING
    elif update.message.text == 'Сдаться':
        return ANSWER
    else:
        update.message.reply_text('Неправильно… Попробуешь ещё раз?')
        return ANSWER


def stop(update: Update, context: CallbackContext):
    return ConversationHandler.END


def give_up(update: Update, context: CallbackContext):
    answer = quiz[r.get(update.effective_chat.id)]
    update.message.reply_text(f'Правильнный ответ: {answer}.\n'
                              'Для следующего вопроса нажми «Новый вопрос»')
    handle_new_question_request(update, context)

    return ANSWER


CHOOSING, ANSWER, PASS = range(3)


def main() -> None:
    """Start the bot."""
    tg_token = TELEGRAM_BOT_TOKEN
    updater = Updater(tg_token)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                RegexHandler('^Новый вопрос$',
                             handle_new_question_request,
                             pass_user_data=True)
                ],
                # RegexHandler('^Мой счёт$',
                #              new_foo)],
            ANSWER: [
                RegexHandler('^Сдаться$',
                             give_up,
                             pass_user_data=True),
                MessageHandler(Filters.text,
                               handle_solution_attempt,
                               pass_user_data=True)
                ]
            },
        fallbacks=[CommandHandler('stop', stop)]
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
