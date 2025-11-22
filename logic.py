import requests
import random
import time

class Pokemon:
    def __init__(self, name, image, attack_power, health, pokemon_class=None):
        self.name = name
        self.image = image
        self.attack_power = attack_power
        self.health = health
        self.max_health = health
        self.pokemon_class = pokemon_class
        self.last_feed_time = 0

    def can_feed(self):
        if self.pokemon_class == 'fighter':
            cooldown = 12 * 3600  # 12 часов в секундах
        else:
            cooldown = 24 * 3600  # 24 часа в секундах
        
        return time.time() - self.last_feed_time >= cooldown

    def feed(self):
        heal_amount = 20
        if self.pokemon_class == 'wizard':
            heal_amount *= 2
        self.health = min(self.health + heal_amount, self.max_health)
        self.last_feed_time = time.time()
        return heal_amount

    def attack(self, defender):
        # Базовая атака
        damage = self.attack_power
        
        # Проверка способностей атакующего (если fighter)
        counter_attack = False
        if self.pokemon_class == 'fighter' and random.random() < 0.33:
            counter_attack = True
        
        # Проверка способностей защищающегося (если wizard)
        shield_active = False
        if defender.pokemon_class == 'wizard' and random.random() < 0.25:
            shield_active = True
            damage = damage // 4  # Уменьшение урона в 4 раза
        
        # Применение урона
        defender.health -= damage
        
        # Контратака (если сработала способность fighter)
        counter_damage = 0
        if counter_attack and defender.health > 0:
            counter_damage = damage // 4  # 25% от нанесенного урона
            self.health -= counter_damage
        
        return {
            'damage': damage,
            'counter_attack': counter_attack,
            'counter_damage': counter_damage,
            'shield_active': shield_active
        }

class PokemonAPI:
    @staticmethod
    def get_random_pokemon():
        pokemon_id = random.randint(1, 151)  # Первое поколение покемонов
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}')
        if response.status_code == 200:
            data = response.json()
            return data
        return None

class PokemonFactory:
    @staticmethod
    def create_pokemon():
        data = PokemonAPI.get_random_pokemon()
        if data:
            name = data['name']
            image = data['sprites']['front_default']
            attack_power = random.randint(30, 65)
            health = random.randint(70, 100)
            
            pokemon_class = None
            if random.random() < 0.15:
                pokemon_class = random.choice(['fighter', 'wizard'])
            
            return Pokemon(name, image, attack_power, health, pokemon_class)
        return None

class Battle:
    @staticmethod
    def fight(pokemon1, pokemon2):
        battle_log = []
        
        # Случайный выбор первого атакующего
        if random.random() < 0.5:
            attacker, defender = pokemon1, pokemon2
            battle_log.append(f"🎲 Первым атакует {attacker.name}!")
        else:
            attacker, defender = pokemon2, pokemon1
            battle_log.append(f"🎲 Первым атакует {attacker.name}!")
        
        # Первая атака
        battle_log.append(f"⚔️ {attacker.name} атакует {defender.name}!")
        result1 = attacker.attack(defender)
        
        class_info_attacker = f" ({attacker.pokemon_class})" if attacker.pokemon_class else ""
        class_info_defender = f" ({defender.pokemon_class})" if defender.pokemon_class else ""
        
        battle_log.append(f"💥 {attacker.name}{class_info_attacker} наносит {result1['damage']} урона!")
        
        if result1['shield_active']:
            battle_log.append(f"🛡️ {defender.name} использует Щит! Урон уменьшен в 4 раза!")
        
        if result1['counter_attack']:
            battle_log.append(f"🔄 {defender.name} контратакует и наносит {result1['counter_damage']} урона!")
        
        battle_log.append(f"❤️ Здоровье {attacker.name}: {max(0, attacker.health)}")
        battle_log.append(f"❤️ Здоровье {defender.name}: {max(0, defender.health)}")
        
        # Проверка на победу после первой атаки
        if defender.health <= 0:
            battle_log.append(f"🎉 Победитель: {attacker.name}!")
            return battle_log
        
        if attacker.health <= 0:
            battle_log.append(f"🎉 Победитель: {defender.name}!")
            return battle_log
        
        # Вторая атака (меняем роли)
        attacker, defender = defender, attacker
        battle_log.append(f"⚔️ {attacker.name} атакует {defender.name}!")
        result2 = attacker.attack(defender)
        
        battle_log.append(f"💥 {attacker.name}{class_info_attacker} наносит {result2['damage']} урона!")
        
        if result2['shield_active']:
            battle_log.append(f"🛡️ {defender.name} использует Щит! Урон уменьшен в 4 раза!")
        
        if result2['counter_attack']:
            battle_log.append(f"🔄 {defender.name} контратакует и наносит {result2['counter_damage']} урона!")
        
        battle_log.append(f"❤️ Здоровье {attacker.name}: {max(0, attacker.health)}")
        battle_log.append(f"❤️ Здоровье {defender.name}: {max(0, defender.health)}")
        
        # Определение победителя
        if attacker.health <= 0 and defender.health <= 0:
            battle_log.append("🤝 Ничья! Оба покемона побеждены!")
        elif attacker.health <= 0:
            battle_log.append(f"🎉 Победитель: {defender.name}!")
        elif defender.health <= 0:
            battle_log.append(f"🎉 Победитель: {attacker.name}!")
        else:
            battle_log.append("🏁 Бой завершен!")
        
        return battle_log



