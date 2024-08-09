from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Хранилище данных для задач
users_tasks = {}

def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    if user_id not in users_tasks:
        users_tasks[user_id] = []
        update.message.reply_text('Привет! Вы зарегистрированы. Начните добавлять задачи командой /add <название задачи>.\n\n'
                                  'используйте комаанду: /help помошник.')
    else:
        update.message.reply_text('Вы уже зарегистрированы. Можете продолжать работу с задачами.')

def add_task(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    task_name = ' '.join(context.args)
    if task_name:
        users_tasks[user_id].append(task_name)
        update.message.reply_text(f'Задача "{task_name}" добавлена.')
    else:
        update.message.reply_text('Пожалуйста, укажите название задачи после команды /add.')

def list_tasks(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    tasks = users_tasks.get(user_id, [])
    if tasks:
        task_list = '\n'.join([f'{i+1}. {task}' for i, task in enumerate(tasks)])
        update.message.reply_text(f'Ваши задачи:\n{task_list}')
    else:
        update.message.reply_text('У вас нет задач.')

def delete_task(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    try:
        task_index = int(context.args[0]) - 1
        task = users_tasks[user_id].pop(task_index)
        update.message.reply_text(f'Задача "{task}" удалена.')
    except (IndexError, ValueError):
        update.message.reply_text('Пожалуйста, укажите корректный номер задачи после команды /delete.')

def edit_task(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    try:
        task_index = int(context.args[0]) - 1
        new_task_name = ' '.join(context.args[1:])
        users_tasks[user_id][task_index] = new_task_name
        update.message.reply_text(f'Задача изменена на "{new_task_name}".')
    except (IndexError, ValueError):
        update.message.reply_text('Пожалуйста, укажите корректный номер задачи и новое название после команды /edit.')

def help_command(update: Update, context: CallbackContext) -> None:
    help_text = (
        "/start - Зарегистрироваться и начать\n"
        "/add <название задачи> - Добавить новую задачу\n"
        "/list - Просмотреть список задач\n"
        "/delete <номер задачи> - Удалить задачу по номеру\n"
        "/edit <номер задачи> <новое название> - Изменить задачу\n"
        "/help - Показать это сообщение"
    )
    update.message.reply_text(help_text)

def main() -> None:
    # Вставьте сюда токен вашего Telegram бота
    updater = Updater("7098958950:AAFV_U95LtwK56kMeWh0m370jxS7qgHTvN8")

    dispatcher = updater.dispatcher

    # Регистрация обработчиков команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("add", add_task))
    dispatcher.add_handler(CommandHandler("list", list_tasks))
    dispatcher.add_handler(CommandHandler("delete", delete_task))
    dispatcher.add_handler(CommandHandler("edit", edit_task))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()