from main import damage

class SpecialAttacks:
    @staticmethod
    def powerful_attack(attacker, target):
        """
        Мощная атака: наносит двойной урон.
        """
        currentAttack = damage(attacker.basicAttack * 2)
        target.health -= currentAttack
        print(f"{attacker.name} использует мощную атаку и наносит {currentAttack} урона!")

    @staticmethod
    def fireball(attacker, target):
        """
        Огненный шар: наносит урон + 10%.
        """
        currentAttack = damage(attacker.basicAttack + (attacker.basicAttack / 100) * 10)
        target.health -= currentAttack
        print(f"{attacker.name} запускает огненный шар и наносит {currentAttack} урона!")

    @staticmethod
    def precise_shot(attacker, target):
        """
        Точный выстрел: наносит урон + 7%.
        """
        currentAttack = damage(attacker.basicAttack + (attacker.basicAttack / 100) * 7)
        target.health -= currentAttack
        print(f"{attacker.name} делает точный выстрел и наносит {currentAttack} урона!")