import telebot
from logic import PokemonFactory, Battle
from config import token

bot = telebot.TeleBot(token)

#  Хранилище покемонов по chat_id
user_pokemons = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот покемонов. Используй /help для списка команд.")

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
Доступные команды:
/create1 - Создать первого покемона
/create2 - Создать второго покемона
/feed1 - Покормить первого покемона
/feed2 - Покормить второго покемона
/fight - Устроить бой между покемонами
    """
    bot.reply_to(message, help_text)

def create_pokemon_for_user(chat_id, slot):
    pokemon = PokemonFactory.create_pokemon()
    if not pokemon:
        return "Ошибка при создании покемона. Попробуйте снова."
    
    if chat_id not in user_pokemons:
        user_pokemons[chat_id] = {}
    
    user_pokemons[chat_id][slot] = pokemon
    
    class_info = ""
    if pokemon.pokemon_class:
        class_info = f"\nКласс: {pokemon.pokemon_class}"
    
    return (f"Покемон {slot} создан!\n"
            f"Имя: {pokemon.name}\n"
            f"Здоровье: {pokemon.health}\n"
            f"Сила удара: {pokemon.attack_power}"
            f"{class_info}")

@bot.message_handler(commands=['create1'])
def create_first_pokemon(message):
    chat_id = message.chat.id
    response = create_pokemon_for_user(chat_id, 1)
    if response.startswith("Покемон"):
        pokemon = user_pokemons[chat_id][1]
        if pokemon.image:
            bot.send_photo(chat_id, pokemon.image, caption=response)
        else:
            bot.reply_to(message, response)
    else:
        bot.reply_to(message, response)

@bot.message_handler(commands=['create2'])
def create_second_pokemon(message):
    chat_id = message.chat.id
    response = create_pokemon_for_user(chat_id, 2)
    if response.startswith("Покемон"):
        pokemon = user_pokemons[chat_id][2]
        if pokemon.image:
            bot.send_photo(chat_id, pokemon.image, caption=response)
        else:
            bot.reply_to(message, response)
    else:
        bot.reply_to(message, response)

def feed_pokemon(message, slot):
    chat_id = message.chat.id
    if chat_id not in user_pokemons or slot not in user_pokemons[chat_id]:
        return f"Сначала создайте покемона {slot} командой /create{slot}"
    
    pokemon = user_pokemons[chat_id][slot]
    
    if not pokemon.can_feed():
        return "Еще не прошло время кормления!"
    
    heal_amount = pokemon.feed()
    return (f"Покемон {pokemon.name} покормлен!\n"
            f"Восстановлено здоровья: {heal_amount}\n"
            f"Текущее здоровье: {pokemon.health}")

@bot.message_handler(commands=['feed1'])
def feed_first_pokemon(message):
    response = feed_pokemon(message, 1)
    bot.reply_to(message, response)

@bot.message_handler(commands=['feed2'])
def feed_second_pokemon(message):
    response = feed_pokemon(message, 2)
    bot.reply_to(message, response)

@bot.message_handler(commands=['fight'])
def fight_pokemons(message):
    chat_id = message.chat.id
    if chat_id not in user_pokemons:
        bot.reply_to(message, "Сначала создайте покемонов командами /create1 и /create2")
        return
    
    if 1 not in user_pokemons[chat_id] or 2 not in user_pokemons[chat_id]:
        bot.reply_to(message, "У вас нет двух покемонов для боя. Создайте их командами /create1 и /create2")
        return
    
    pokemon1 = user_pokemons[chat_id][1]
    pokemon2 = user_pokemons[chat_id][2]
    
    # Сохраняем исходное здоровье для восстановления после боя
    original_health1 = pokemon1.health
    original_health2 = pokemon2.health
    
    battle_log = Battle.fight(pokemon1, pokemon2)
    
    # Отправляем лог боя
    battle_text = "\n".join(battle_log)
    bot.reply_to(message, f"🏟️ НАЧАЛО БОЯ!\n\n{battle_text}")
    
    # Восстанавливаем здоровье покемонов после боя

if __name__ == '__main__':
    bot.polling()    

