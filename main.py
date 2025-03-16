from time import sleep
from random import randint

# Функция для рандомного урона
def damage(base_damage):
    return randint(base_damage - 5, base_damage + 5)

class Character:
    def __init__(self, name, health, basicAttack):
        self.name = name
        self.max_health = health  # Максимальное здоровье
        self.health = health
        self.basicAttack = basicAttack
        self.special_cooldown = 0
        self.experience = 0
        self.level = 1

    def attack_target(self, target):
        currentAttack = damage(self.basicAttack)
        target.health = max(target.health - currentAttack, 0)  # Здоровье не меньше 0
        return f"{self.name} атакует {target.name} и наносит {currentAttack} урона!"

    def heal(self, amount):
        self.health = min(self.health + amount, self.max_health)  # Здоровье не больше максимума
        return f"{self.name} восстанавливает {amount} здоровья!"

    def is_alive(self):
        return self.health > 0

    def update_cooldown(self):
        if self.special_cooldown > 0:
            self.special_cooldown -= 1

    def gain_experience(self, amount):
        self.experience += amount
        return f"{self.name} получает {amount} опыта!"
        if self.experience >= 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_health += 20  # Увеличиваем максимальное здоровье
        self.health = self.max_health  # Восстанавливаем здоровье до максимума
        self.basicAttack += 5
        self.experience = 0
        return f"{self.name} повысил уровень до {self.level}! Здоровье: {self.health}, Атака: {self.basicAttack}"

    def __str__(self):
        return f"{self.name} (Здоровье: {self.health}, Атака: {self.basicAttack})"


class Warrior(Character):
    def __init__(self, name, health, basicAttack):
        super().__init__(name, health, basicAttack)
        self.special_cooldown_max = 3

    def special_attack(self, target):
        if self.special_cooldown == 0:
            damage = self.basicAttack * 2
            target.health = max(target.health - damage, 0)
            self.special_cooldown = self.special_cooldown_max
            return f"{self.name} использует мощную атаку и наносит {damage} урона!"
        else:
            return f"{self.name} не может использовать мощную атаку! Осталось ходов до перезарядки: {self.special_cooldown}"


class Mage(Character):
    def __init__(self, name, health, basicAttack):
        super().__init__(name, health, basicAttack)
        self.special_cooldown_max = 4

    def special_attack(self, target):
        if self.special_cooldown == 0:
            damage = self.basicAttack + 10
            target.health = max(target.health - damage, 0)
            self.special_cooldown = self.special_cooldown_max
            return f"{self.name} запускает огненный шар и наносит {damage} урона!"
        else:
            return f"{self.name} не может использовать огненный шар! Осталось ходов до перезарядки: {self.special_cooldown}"


class Archer(Character):
    def __init__(self, name, health, basicAttack):
        super().__init__(name, health, basicAttack)
        self.special_cooldown_max = 2

    def special_attack(self, target):
        if self.special_cooldown == 0:
            damage = self.basicAttack + 5
            target.health = max(target.health - damage, 0)
            self.special_cooldown = self.special_cooldown_max
            return f"{self.name} делает точный выстрел и наносит {damage} урона!"
        else:
            return f"{self.name} не может использовать точный выстрел! Осталось ходов до перезарядки: {self.special_cooldown}"


class Enemy(Character):
    def __init__(self, name, health, basicAttack, reward_experience):
        super().__init__(name, health, basicAttack)
        self.reward_experience = reward_experience
        self.special_cooldown = 0

    def defeat_reward(self):
        return f"{self.name} повержен"


class Goblin(Enemy):
    def __init__(self):
        super().__init__(name="Гоблин", health=50, basicAttack=20, reward_experience=20)

    def steal(self, target):
        if self.special_cooldown == 0:
            stolen_health = 15
            target.health = max(target.health - stolen_health, 0)
            self.health += stolen_health
            self.special_cooldown = 3
            return f"{self.name} крадёт {stolen_health} здоровья у {target.name}!"
        else:
            return f"{self.name} не может украсть здоровье! Осталось ходов до перезарядки: {self.special_cooldown}"


class Orc(Enemy):
    def __init__(self):
        super().__init__(name="Огр", health=100, basicAttack=15, reward_experience=30)

    def berserk(self):
        if self.special_cooldown == 0:
            self.basicAttack += 10
            self.special_cooldown = 4
            return f"{self.name} впадает в ярость! Его атака увеличена до {self.basicAttack}."
        else:
            return f"{self.name} не может впасть в ярость! Осталось ходов до перезарядки: {self.special_cooldown}"


class Dragon(Enemy):
    def __init__(self):
        super().__init__(name="Дракон", health=150, basicAttack=13, reward_experience=50)

    def fire_breath(self, target):
        if self.special_cooldown == 0:
            damage = self.basicAttack + 5
            target.health = max(target.health - damage, 0)
            self.special_cooldown = 5
            return f"{self.name} использует огненное дыхание и наносит {damage} урона!"
        else:
            return f"{self.name} не может использовать огненное дыхание! Осталось ходов до перезарядки: {self.special_cooldown}"


def choose_enemy():
    import random
    enemies = [Goblin(), Orc(), Dragon()]
    return random.choice(enemies)