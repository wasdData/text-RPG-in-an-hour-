from main import Warrior, Mage, Archer, Goblin, Orc, Dragon,choose_enemy
import tkinter as tk
from tkinter import ttk, messagebox

class RPGApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RPG Game")
        self.root.geometry("500x400")
        self.root.configure(bg="#f0f0f0")

        # Стилизация
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12), padding=10, background="#4CAF50", foreground="white")
        self.style.configure("TLabel", font=("Arial", 14), background="#f0f0f0", foreground="#333")
        self.style.configure("Disabled.TButton", font=("Arial", 12), padding=10, background="#ccc", foreground="#666")

        # Окно выбора класса (модальное)
        self.choose_class_window = tk.Toplevel(root)
        self.choose_class_window.title("Выбери класс")
        self.choose_class_window.geometry("300x150")
        self.choose_class_window.configure(bg="#f0f0f0")
        self.choose_class_window.grab_set()  # Делаем окно модальным

        tk.Label(self.choose_class_window, text="Выбери класс персонажа:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)

        self.class_var = tk.StringVar(value="1")  # По умолчанию выбран Воин

        tk.Radiobutton(self.choose_class_window, text="Воин", variable=self.class_var, value="1", bg="#f0f0f0").pack()
        tk.Radiobutton(self.choose_class_window, text="Маг", variable=self.class_var, value="2", bg="#f0f0f0").pack()
        tk.Radiobutton(self.choose_class_window, text="Лучник", variable=self.class_var, value="3", bg="#f0f0f0").pack()

        tk.Button(self.choose_class_window, text="Начать игру", command=self.start_game, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=10)

    def start_game(self):
        # Создаем персонажа в зависимости от выбора
        class_choice = self.class_var.get()
        if class_choice == "1":
            self.hero = Warrior("Герой", health=100, basicAttack=20)
        elif class_choice == "2":
            self.hero = Mage("Герой", health=80, basicAttack=25)
        elif class_choice == "3":
            self.hero = Archer("Герой", health=90, basicAttack=22)

        self.choose_class_window.destroy()  # Закрываем окно выбора класса
        self.init_main_interface()  # Запускаем основное окно игры

    def init_main_interface(self):
        # Характеристики врага
        self.enemy = choose_enemy()

        # Создаём элементы интерфейса
        self.hero_label = ttk.Label(self.root, text=str(self.hero), style="TLabel")
        self.hero_label.pack(pady=10)

        self.enemy_label = ttk.Label(self.root, text=str(self.enemy), style="TLabel")
        self.enemy_label.pack(pady=10)

        self.log_text = tk.Text(self.root, height=10, width=50, state="disabled", font=("Arial", 12), bg="#fff", fg="#333")
        self.log_text.pack(pady=10)

        self.attack_button = ttk.Button(self.root, text="Атака", command=self.attack, style="TButton")
        self.attack_button.pack(side=tk.LEFT, padx=10)

        self.heal_button = ttk.Button(self.root, text="Лечение", command=self.heal, style="TButton")
        self.heal_button.pack(side=tk.LEFT, padx=10)

        self.special_button = ttk.Button(self.root, text="Мощная атака", command=self.special_attack, style="TButton")
        self.special_button.pack(side=tk.LEFT, padx=10)

        # Обновляем состояние кнопки мощной атаки
        self.update_special_button_state()

    def attack(self):
        message = self.hero.attack_target(self.enemy)
        self.update_log(message)
        self.update_labels()
        self.enemy_turn()

    def heal(self):
        message = self.hero.heal(10)
        self.update_log(message)
        self.update_labels()
        self.enemy_turn()

    def special_attack(self):
        message = self.hero.special_attack(self.enemy)
        self.update_log(message)
        self.update_labels()
        self.enemy_turn()

    def enemy_turn(self):
        if self.enemy.is_alive():
            if isinstance(self.enemy, Goblin):
                if self.enemy.special_cooldown == 0:
                    message = self.enemy.steal(self.hero)
                else:
                    message = self.enemy.attack_target(self.hero)
            elif isinstance(self.enemy, Orc):
                if self.enemy.special_cooldown == 0:
                    message = self.enemy.berserk()
                else:
                    message = self.enemy.attack_target(self.hero)
            elif isinstance(self.enemy, Dragon):
                if self.enemy.special_cooldown == 0:
                    message = self.enemy.fire_breath(self.hero)
                else:
                    message = self.enemy.attack_target(self.hero)
            self.enemy.update_cooldown()
            self.update_log(message)
            self.update_labels()

        self.check_game_over()

    def update_labels(self):
        self.hero_label.config(text=str(self.hero))
        self.enemy_label.config(text=str(self.enemy))
        self.update_special_button_state()

    def update_log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state="disabled")
        self.log_text.see(tk.END)  # Прокрутка лога вниз

    def update_special_button_state(self):
        if self.hero.special_cooldown > 0:
            self.special_button.config(state="disabled", style="Disabled.TButton")
        else:
            self.special_button.config(state="normal", style="TButton")

    def check_game_over(self):
        if not self.hero.is_alive():
            messagebox.showinfo("Конец игры", f"{self.enemy.name} побеждает!")
            self.root.quit()
        elif not self.enemy.is_alive():
            messagebox.showinfo("Конец игры", f"{self.hero.name} побеждает!")
            self.root.quit()


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = RPGApp(root)
    root.mainloop()