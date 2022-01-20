from asyncore import loop
import time
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DELAY = 3600
tg_chat_id = -1001706482336
my_tg_id = 1913321923
API_TOKEN = "5021232324:AAHRoPJSJ1vWfNfYxqgqDF2urgPEGl5wcuk"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
account_data = {
    'login': 'bolvanchik',
    'password': 'testpassword443_'
}
forum_url = "https://forum.telegramhero.ru"
forum_login_url = "{}/login".format(forum_url)
forum_last_activity_url = "{}/whats-new/latest-activity".format(forum_url)

async def last_activity():
    try:
        mozilla_options = FirefoxOptions()
        mozilla_options.add_argument('--disable-dev-shm-usage')
        mozilla_options.add_argument('--no-sandbox')
        mozilla_options.add_argument("--headless")
        driver = webdriver.Firefox(options=mozilla_options)
        driver.get(forum_login_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'keywords')))
        login_input = driver.find_element(By.NAME, 'login')
        login_input.send_keys(account_data['login'])

        password_input = driver.find_element(By.NAME, 'password')
        password_input.send_keys(account_data['password'])
        password_input.send_keys(Keys.ENTER)

        driver.get(forum_last_activity_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'keywords')))
        time.sleep(0.5)
        title = driver.find_element(By.CLASS_NAME, 'contentRow-title')
        data = title.text
        driver.quit()
        return data
        

    except Exception as ex:
        print(ex)

@dp.message_handler(commands=['start'])
async def welcome_func(message: types.Message):
    await message.answer('Приветствую! При запуске бот оправляет последние изменения в форуме интервалом в 3.600 секунд.')

@dp.message_handler(text=['last'])
async def get_last_activity():
    answer_data = await last_activity()
    await bot.send_message(my_tg_id, answer_data, disable_notification=True)

def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(DELAY, repeat, coro, loop)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.call_later(DELAY, repeat, get_last_activity, loop)
    executor.start_polling(dp, skip_updates=True, loop=loop)
