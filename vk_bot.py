import random
import vk_api as VK
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from config import VK_TOKEN
from quiz_loader import quiz
from redis_manager import r


def start_quiz(event, vk_api):
    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Мой счёт', color=VkKeyboardColor.SECONDARY)

    if event.text == 'Новый вопрос':
        question = random.choice(list(quiz))
        vk_api.messages.send(
            peer_id=event.user_id,
            message=question,
            keyboard=keyboard.get_keyboard(),
            random_id=random.randint(1, 1000)
        )
        r.set(event.user_id, question)
        # anrwer = (quiz[question])
        # print(anrwer)
    elif event.text == 'Сдаться':
        answer = quiz[r.get(event.user_id)]
        vk_api.messages.send(
            peer_id=event.user_id,
            keyboard=keyboard.get_keyboard(),
            message=(f'Правильнный ответ: {answer}. Для следующего вопроса нажми «Новый вопрос»'),
            random_id=random.randint(1, 1000)
        )
    elif event.text == (quiz[r.get(event.user_id)]):
        vk_api.messages.send(
            peer_id=event.user_id,
            keyboard=keyboard.get_keyboard(),
            message='Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»',
            random_id=random.randint(1, 1000)
        )
    else:
        vk_api.messages.send(
            peer_id=event.user_id,
            keyboard=keyboard.get_keyboard(),
            message='Неправильно… Попробуешь ещё раз?',
            random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":
    vk_session = VK.VkApi(token=VK_TOKEN)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            start_quiz(event, vk_api)
