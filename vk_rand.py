import bs4, requests, telebot, random, time, sys, csv
from fake_useragent import UserAgent
from telebot import types as tp
from keyboa import keyboa_maker


# =============================================================================
# USER INPUT VARIABLES
# =============================================================================

bot = telebot.TeleBot(token='TOKEN HERE')


# =============================================================================
# PROGRAM
# =============================================================================


try:                                                #database check/creation
    csvfile_read = open('vk_exist.csv', 'r').close()
    
except FileNotFoundError:
    with open('vk_exist.csv','w',newline='') as f:
        csv_writer=csv.writer(f)
        csv_writer.writerow(['link', 'name'])

                                                    #reply_markups
main_menu = tp.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=1)
main_menu.add('📖 Random page')


db = [
  "Send to DB"
]

callback = keyboa_maker(items=db, copy_text_to_callback=True)
db_ok = [
  "THANKS"
]
callback_ok = keyboa_maker(items=db_ok, copy_text_to_callback=True)

                                                    #main_script
def rand_page(user_id):
    link = 'https://vk.com/id'
    url = str(random.randint(1, 1000000000))
    not_created = []
    
    only_content = bs4.SoupStrainer("div", id='content')
    r = requests.get(link+url, stream=True, headers={'User-Agent': UserAgent().chrome})
    soup = bs4.BeautifulSoup(r.text, "lxml", parse_only=only_content) 
    
    
    blocked = soup.find_all('h5', class_="profile_blocked")
    not_created = soup.find_all('div', class_='message_page page_block')
    if blocked != []:
        bot.send_message(user_id,  '*User is blocked :(*\n' + link+url, parse_mode='Markdown', reply_markup=main_menu)
        return
    if not_created != []:
        rand_page(user_id)   
        
    try: 
        name = soup.find('h1', class_='page_name').text
        bot.send_message(user_id, '*User alive!*\nName: ' +  str(name) + '\n' + link+url, parse_mode='Markdown', reply_markup=callback)
        print(str(user_id), 'Page found!')
        return
    except AttributeError:
        print('Error blyat')


@bot.message_handler(commands=['start', 'menu', 'help'])
def help_message(message):
    bot.send_message(message.from_user.id, '''👔 *VK Random Page Bot*.    
📞 *Usage*
Simply use button to get page: `Random page`, I know, you want some fun, Have fun
''', reply_markup=main_menu, parse_mode='Markdown')



@bot.message_handler(content_types=['text'])
def bot_input(message):
    text = message.text
    user_id = message.from_user.id
    
    if text == '📖 Random page':
        rand_page(user_id)



                                                    #inline database ask
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    text_array = str(call.message.text).split('\n')
    link = text_array[2]
    name = text_array[1]
    with open('vk_exist.csv','a',newline='') as f:
        vk_writer=csv.writer(f)
        vk_writer.writerow([link, name])
    bot.edit_message_text(call.message.text,call.from_user.id , call.message.message_id,  parse_mode='Markdown', reply_markup=callback_ok)
    print('Database Updated')


if __name__ == '__main__':
    
    while True:
        try:
            bot.infinity_polling(True)
        except KeyboardInterrupt:
            print('This is the end, folks')
            sys.exit(0)
        except ConnectionError:
            time.sleep(15)