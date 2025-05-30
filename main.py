import tkinter as tk
import customtkinter as ctk
from datetime import datetime, timedelta
import bcrypt

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# Хэширование паролей
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(hashed, password):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Шаблоны планов тренировок
workout_templates = {
    "default": {
        "beginner": "Начальный уровень: разминка, ходьба 30 мин, базовая растяжка.",
        "intermediate": "Средний уровень: кардио + силовые упражнения, растяжка.",
        "advanced": "Продвинутый уровень: HIIT, силовые блоки."
    },
    "health_issues": {
        "сердце": "Тренировка с низкой нагрузкой: плавное кардио, дыхательные упражнения.",
        "спина": "Упражнения на укрепление мышц спины, щадящая растяжка.",
        "суставы": "Без прыжков, акцент на плавность движений и укрепление связок."
    }
}

# Исходные данные
users = {
    "admin": {"password": hash_password("admin"), "role": "admin"},
    "vlad": {"password": hash_password("vlad"), "role": "coach", "name": "Влад Поляшов"},
    "bogdan": {"password": hash_password("bogdan"), "role": "coach", "name": "Богдан Скрипин"},
    "alex": {"password": hash_password("alex"), "role": "coach", "name": "Александр Кузнецов"}
}
clients = []
passes = [
    {"type": "неделя", "duration_days": 7, "price_per_day": 142},
    {"type": "месяц", "duration_days": 30, "price_per_day": 100},
    {"type": "год", "duration_days": 365, "price_per_day": 82},
    {"type": "пользовательский", "duration_days": None, "price_per_day": 100}
]
groups = {
    "Квадробика": "Влад Поляшов",
    "Фуррисплеинг": "Влад Поляшов",
    "Бокс": "Богдан Скрипин",
    "Йога": "Александр Кузнецов"
}
trainers = [
    {"name": "Влад Поляшов", "qualification": "Мастер спорта по КВД и Фурри", "groups": ["Квадробика", "Фуррисплеинг"]},
    {"name": "Богдан Скрипин", "qualification": "Тренер высшей категории", "groups": ["Бокс"]},
    {"name": "Александр Кузнецов", "qualification": "Личный тренер", "groups": ["Йога"]}
]

class GymApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Фитнес-приложение")
        self.geometry("900x650")
        self.resizable(False, False)
        self.current_frame = None
        self.user_role = None
        self.username = None
        self.show_login()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ctk.CTkFrame(self)
        self.current_frame.pack(padx=20, pady=20, fill="both", expand=True)

    def show_login(self):
        self.clear_frame()
        ctk.CTkLabel(self.current_frame, text="Вход", font=("Arial", 24, "bold")).pack(pady=20)
        self.login_entry = ctk.CTkEntry(self.current_frame, placeholder_text="Логин", width=300)
        self.login_entry.pack(pady=10)
        self.pass_entry = ctk.CTkEntry(self.current_frame, placeholder_text="Пароль", show="*", width=300)
        self.pass_entry.pack(pady=10)
        ctk.CTkButton(self.current_frame, text="Войти", command=self.login, width=200, fg_color="#3A7C59").pack(pady=20)

    def login(self):
        login = self.login_entry.get().strip()
        password = self.pass_entry.get().strip()
        user = users.get(login)
        if user and check_password(user["password"], password):
            self.user_role = user["role"]
            self.username = login
            if self.user_role == "admin":
                self.show_admin_panel()
            elif self.user_role == "coach":
                self.show_coach_panel()
        else:
            ctk.CTkLabel(self.current_frame, text="Неверный логин или пароль", text_color="red").pack()

    def validate_name(self, value):
        return value == "" or value.replace(" ", "").isalpha()

    def validate_phone(self, value):
        if len(value) > 12:
            return False
        return value == "" or value.isdigit() or (value.startswith('+') and value[1:].isdigit())

    def register_client(self):
        self.clear_frame()
        ctk.CTkLabel(self.current_frame, text="Регистрация клиента", font=("Arial", 18, "bold")).pack(pady=10)
        self.name = ctk.CTkEntry(self.current_frame, placeholder_text="Имя")
        self.name.pack(pady=5)
        self.name.bind("<FocusOut>", lambda e: self.validate_field(self.name, self.validate_name))
        self.surname = ctk.CTkEntry(self.current_frame, placeholder_text="Фамилия")
        self.surname.pack(pady=5)
        self.surname.bind("<FocusOut>", lambda e: self.validate_field(self.surname, self.validate_name))
        self.patronymic = ctk.CTkEntry(self.current_frame, placeholder_text="Отчество")
        self.patronymic.pack(pady=5)
        self.patronymic.bind("<FocusOut>", lambda e: self.validate_field(self.patronymic, self.validate_name))
        self.phone = ctk.CTkEntry(self.current_frame, placeholder_text="Номер телефона")
        self.phone.pack(pady=5)
        vcmd = (self.register(self.validate_phone), '%P')
        self.phone.configure(validate="key", validatecommand=vcmd)
        ctk.CTkLabel(self.current_frame, text="Проблемы со здоровьем?").pack(pady=5)
        self.health_issue_var = tk.StringVar(value="Нет")
        self.health_menu = ctk.CTkOptionMenu(
            self.current_frame,
            values=["Нет", "Да"],
            variable=self.health_issue_var,
            command=self.toggle_health_desc
        )
        self.health_menu.pack(pady=5)
        self.health_desc_frame = ctk.CTkFrame(self.current_frame)
        self.health_desc = ctk.CTkEntry(self.health_desc_frame, placeholder_text="Описание проблем")
        self.health_desc.pack(pady=5)
        self.health_desc_frame.pack_forget()
        ctk.CTkButton(self.current_frame, text="Далее → Выбор абонемента", command=self.select_pass).pack(pady=10)

    def toggle_health_desc(self, value):
        if value == "Да":
            self.health_desc_frame.pack(pady=5, fill="x")
        else:
            self.health_desc_frame.pack_forget()

    def validate_field(self, widget, validator):
        value = widget.get()
        if not validator(value):
            widget.configure(border_color="red")
        else:
            widget.configure(border_color="gray")

    def select_pass(self):
        name = self.name.get().strip()
        surname = self.surname.get().strip()
        patronymic = self.patronymic.get().strip()
        phone = self.phone.get().strip()
        if not all([name, surname, phone]):
            ctk.CTkLabel(self.current_frame, text="Заполните обязательные поля", text_color="red").pack()
            return
        self.client_data = {
            "name": name,
            "surname": surname,
            "patronymic": patronymic,
            "phone": phone,
            "health_issues": f"{self.health_issue_var.get()}: {self.health_desc.get()}",
            "attendance": [],
            "pass_start": datetime.now().strftime("%Y-%m-%d")
        }
        self.clear_frame()
        ctk.CTkLabel(self.current_frame, text="Выбор абонемента", font=("Arial", 18, "bold")).pack(pady=10)
        self.pass_var = tk.StringVar(value="неделя")
        for p in passes:
            ctk.CTkRadioButton(
                self.current_frame,
                text=f"{p['type']} ({p.get('duration_days', 'custom')} дней, {p.get('price_per_day', '?')} руб/день)",
                value=p['type'],
                variable=self.pass_var
            ).pack(anchor='w')

        # Добавляем выбор статуса оплаты
        ctk.CTkLabel(self.current_frame, text="Статус оплаты").pack(pady=5)
        self.payment_var = tk.StringVar(value="Оплачено")
        ctk.CTkOptionMenu(
            self.current_frame,
            values=["Оплачено", "Не оплачено"],
            variable=self.payment_var
        ).pack(pady=5)

        self.custom_days_entry = None
        self.price_label = None

        def update_custom_days(*args):
            if self.pass_var.get() == "пользовательский":
                if not self.custom_days_entry:
                    self.custom_days_entry = ctk.CTkEntry(self.current_frame, placeholder_text="Введите количество дней")
                    self.custom_days_entry.pack(pady=5)
                    self.price_label = ctk.CTkLabel(self.current_frame, text="")
                    self.price_label.pack(pady=5)
                    self.custom_days_entry.bind("<KeyRelease>", lambda e: update_price())
            else:
                if self.custom_days_entry:
                    self.custom_days_entry.destroy()
                    self.custom_days_entry = None
                if self.price_label:
                    self.price_label.destroy()
                    self.price_label = None

        def update_price(*args):
            try:
                days = int(self.custom_days_entry.get())
                price_per_day = next(p for p in passes if p['type'] == 'пользовательский')['price_per_day']
                total = days * price_per_day
                self.price_label.configure(text=f"Общая стоимость: {total} руб. (по {price_per_day} руб./день)")
            except ValueError:
                self.price_label.configure(text="")

        self.pass_var.trace_add("write", update_custom_days)
        ctk.CTkButton(self.current_frame, text="Далее → Выбор группы", command=self.select_group).pack(pady=10)
        ctk.CTkButton(self.current_frame, text="Назад", command=self.show_admin_panel).pack(pady=5)

    def select_group(self):
        pass_type = self.pass_var.get()
        selected_pass = next((p for p in passes if p["type"] == pass_type), None)
        duration_days = selected_pass["duration_days"]

        if pass_type == "пользовательский":
            try:
                duration_days = int(self.custom_days_entry.get())
                if duration_days <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                ctk.CTkLabel(self.current_frame, text="Введите корректное положительное число дней", text_color="red").pack()
                return

        start_date = datetime.now()
        end_date = (start_date + timedelta(days=duration_days)).strftime("%Y-%m-%d") if duration_days else "Не указан"

        level = "beginner"
        plan = workout_templates["default"][level]
        health_issue = self.client_data.get("health_issues", "").lower()
        if "сердце" in health_issue:
            plan = workout_templates["health_issues"]["сердце"]
        elif "спина" in health_issue:
            plan = workout_templates["health_issues"]["спина"]
        elif "сустав" in health_issue:
            plan = workout_templates["health_issues"]["суставы"]

        self.client_data.update({
            "pass_type": pass_type,
            "pass_start": start_date.strftime("%Y-%m-%d"),
            "pass_end": end_date,
            "payment_status": self.payment_var.get(),
            "workout_plan": plan
        })

        self.clear_frame()
        ctk.CTkLabel(self.current_frame, text="Выбор группы", font=("Arial", 18, "bold")).pack(pady=10)
        self.group_var = tk.StringVar()
        for group, coach in groups.items():
            ctk.CTkRadioButton(
                self.current_frame,
                text=f"{group} — {coach}",
                value=group,
                variable=self.group_var
            ).pack(anchor='w')

        def confirm_group():
            selected_group = self.group_var.get()
            if selected_group:
                coach = groups[selected_group]
                self.client_data.update({"group": selected_group, "assigned_coach": coach})
                clients.append(self.client_data)
                ctk.CTkLabel(self.current_frame, text="Клиент зарегистрирован!", text_color="green").pack(pady=10)
                def go_back():
                    self.show_admin_panel()
                ctk.CTkButton(self.current_frame, text="Назад в меню", command=go_back).pack(pady=5)
                ctk.CTkButton(self.current_frame, text="Зарегистрировать ещё одного клиента", command=self.register_client).pack(pady=5)
            else:
                ctk.CTkLabel(self.current_frame, text="Выберите группу", text_color="red").pack()

        ctk.CTkButton(self.current_frame, text="Подтвердить", command=confirm_group).pack(pady=10)
        ctk.CTkButton(self.current_frame, text="Назад", command=self.select_pass).pack(pady=5)

    def list_clients(self, group_filter="Все"):
        self.clear_frame()
        ctk.CTkLabel(self.current_frame, text="Список клиентов", font=("Arial", 18, "bold")).pack(pady=10)
        filter_frame = ctk.CTkFrame(self.current_frame)
        filter_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(filter_frame, text="Фильтр по группе:").pack(side="left")
        group_var = tk.StringVar(value=group_filter)
        group_options = ["Все"] + list(groups.keys())
        group_menu = ctk.CTkOptionMenu(filter_frame, values=group_options, variable=group_var)
        group_menu.pack(side="left", padx=5)
        def apply_filter():
            self.clear_frame()
            self.list_clients(group_filter=group_var.get())
        ctk.CTkButton(filter_frame, text="Применить", command=apply_filter).pack(side="left", padx=5)

        client_list_frame = ctk.CTkScrollableFrame(self.current_frame)
        client_list_frame.pack(fill="both", expand=True)

        for idx, client in enumerate(clients):
            if group_filter != "Все" and client.get("group") != group_filter:
                continue
            client_payment = client.get("payment_status", "Не оплачено")
            bg_color = "#ccffcc" if client_payment == "Оплачено" else "#ffcccc"
            frame = ctk.CTkFrame(client_list_frame, fg_color=bg_color)
            frame.pack(fill="x", pady=5, padx=10)

            info = f"{client.get('surname', '-')} {client.get('name', '-')} | Тел: {client.get('phone', '-')}" \
                   f" | Группа: {client.get('group', '-')} | Абонемент до: {client.get('pass_end', '-')}"
            ctk.CTkLabel(frame, text=info, justify="left").pack(padx=10, anchor='w')
            ctk.CTkLabel(frame, text=f"Оплата: {client_payment}", text_color="black").pack(padx=10, anchor='w')

            btn_frame = ctk.CTkFrame(frame)
            btn_frame.pack(fill="x", pady=5)
            ctk.CTkButton(btn_frame, text="Редактировать", width=100,
                          command=lambda i=idx: self.edit_client(i)).pack(side="left", padx=5)
            ctk.CTkButton(btn_frame, text="Удалить", width=100, fg_color="#a94442", hover_color="#8b2e2c",
                          command=lambda i=idx: self.delete_client(i)).pack(side="left", padx=5)
            ctk.CTkButton(btn_frame, text="План тренировок", width=100,
                          command=lambda i=idx: self.edit_workout_plan(i)).pack(side="left", padx=5)
            ctk.CTkButton(btn_frame, text="Оплата", width=100,
                          command=lambda i=idx: self.edit_payment(i)).pack(side="left", padx=5)

        ctk.CTkButton(self.current_frame, text="Назад", command=self.show_admin_panel).pack(pady=10)

    def edit_workout_plan(self, index):
        self.clear_frame()
        client = clients[index]
        ctk.CTkLabel(self.current_frame, text="Редактирование плана тренировок", font=("Arial", 18, "bold")).pack(pady=10)
        plan_text = ctk.CTkTextbox(self.current_frame, height=250, width=600, wrap="word")
        plan_text.insert("1.0", client.get("workout_plan", ""))
        plan_text.pack(pady=10, padx=10, fill="both", expand=True)

        def save_plan():
            clients[index]["workout_plan"] = plan_text.get("1.0", "end").strip()
            ctk.CTkLabel(self.current_frame, text="✅ План тренировок сохранён", text_color="green").pack(pady=10)
            self.after(1500, lambda: self.return_based_on_role())

        ctk.CTkButton(self.current_frame, text="Сохранить изменения", command=save_plan, fg_color="#2E8B57").pack(pady=10)
        ctk.CTkButton(self.current_frame, text="⬅ Назад", command=lambda: self.return_based_on_role(), width=150).pack(pady=5)

    def edit_payment(self, index):
        self.clear_frame()
        client = clients[index]
        ctk.CTkLabel(self.current_frame, text="Редактирование оплаты", font=("Arial", 18, "bold")).pack(pady=10)
        payment_var = tk.StringVar(value=client.get("payment_status", "Оплачено"))
        ctk.CTkOptionMenu(self.current_frame, values=["Оплачено", "Не оплачено"], variable=payment_var).pack(pady=5)

        start_entry = ctk.CTkEntry(self.current_frame)
        start_entry.insert(0, client.get("pass_start", ""))
        start_entry.pack(pady=5)

        end_entry = ctk.CTkEntry(self.current_frame)
        end_entry.insert(0, client.get("pass_end", ""))
        end_entry.pack(pady=5)

        def save_payment():
            clients[index].update({
                "payment_status": payment_var.get(),
                "pass_start": start_entry.get().strip(),
                "pass_end": end_entry.get().strip()
            })
            ctk.CTkLabel(self.current_frame, text="✅ Статус оплаты обновлён", text_color="green").pack(pady=10)
            self.after(1500, lambda: self.return_based_on_role())

        ctk.CTkButton(self.current_frame, text="Сохранить изменения", command=save_payment).pack(pady=10)
        ctk.CTkButton(self.current_frame, text="⬅ Назад", command=lambda: self.return_based_on_role(), width=150).pack(pady=5)

    def return_based_on_role(self):
        if self.user_role == "coach":
            self.view_my_group()
        else:
            self.list_clients()

    def edit_client(self, index):
        self.clear_frame()
        ctk.CTkLabel(self.current_frame, text="Редактирование клиента", font=("Arial", 18, "bold")).pack(pady=10)
        client = clients[index]
        self.name = ctk.CTkEntry(self.current_frame, placeholder_text="Имя")
        self.name.insert(0, client["name"])
        self.name.pack(pady=5)
        self.surname = ctk.CTkEntry(self.current_frame, placeholder_text="Фамилия")
        self.surname.insert(0, client["surname"])
        self.surname.pack(pady=5)
        self.patronymic = ctk.CTkEntry(self.current_frame, placeholder_text="Отчество")
        self.patronymic.insert(0, client["patronymic"])
        self.patronymic.pack(pady=5)
        self.phone = ctk.CTkEntry(self.current_frame, placeholder_text="Номер телефона")
        self.phone.insert(0, client["phone"])
        self.phone.pack(pady=5)
        ctk.CTkLabel(self.current_frame, text="Проблемы со здоровье?").pack(pady=5)
        self.health_issue_var = tk.StringVar(value=client["health_issues"].split(":")[0] if ":" in client["health_issues"] else "Нет")
        self.health_menu = ctk.CTkOptionMenu(
            self.current_frame,
            values=["Нет", "Да"],
            variable=self.health_issue_var,
            command=self.toggle_health_desc_edit
        )
        self.health_menu.pack(pady=5)
        self.health_desc_frame = ctk.CTkFrame(self.current_frame)
        self.health_desc = ctk.CTkEntry(self.health_desc_frame, placeholder_text="Описание проблем")
        health_desc_value = client["health_issues"].split(":", 1)[1].strip() if ":" in client["health_issues"] else ""
        self.health_desc.insert(0, health_desc_value)
        self.health_desc.pack(pady=5)
        if self.health_issue_var.get() == "Да":
            self.health_desc_frame.pack(pady=5, fill="x")

        def save_changes():
            clients[index].update({
                "name": self.name.get().strip(),
                "surname": self.surname.get().strip(),
                "patronymic": self.patronymic.get().strip(),
                "phone": self.phone.get().strip(),
                "health_issues": f"{self.health_issue_var.get()}: {self.health_desc.get().strip()}"
            })
            ctk.CTkLabel(self.current_frame, text="Данные успешно обновлены!", text_color="green").pack(pady=10)
            self.after(1500, lambda: self.return_based_on_role())

        ctk.CTkButton(self.current_frame, text="Сохранить изменения", command=save_changes).pack(pady=10)
        ctk.CTkButton(self.current_frame, text="Отмена", command=lambda: self.return_based_on_role()).pack(pady=5)

    def toggle_health_desc_edit(self, value):
        if value == "Да":
            self.health_desc_frame.pack(pady=5, fill="x")
        else:
            self.health_desc_frame.pack_forget()

    def delete_client(self, index):
        confirm_window = ctk.CTkToplevel(self)
        confirm_window.title("Подтверждение удаления")
        confirm_window.geometry("400x150")
        confirm_window.resizable(False, False)
        ctk.CTkLabel(confirm_window, text="Вы уверены, что хотите удалить этого клиента?", font=("Arial", 16)).pack(pady=20)
        btn_frame = ctk.CTkFrame(confirm_window)
        btn_frame.pack()
        def do_delete():
            del clients[index]
            confirm_window.destroy()
            self.list_clients()
        ctk.CTkButton(btn_frame, text="Да", width=100, command=do_delete).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Нет", width=100, command=confirm_window.destroy).pack(side="left", padx=10)

    def list_trainers(self):
        self.clear_frame()
        ctk.CTkLabel(self.current_frame, text="Список персонала", font=("Arial", 18, "bold")).pack(pady=10)
        for t in trainers:
            frame = ctk.CTkFrame(self.current_frame)
            frame.pack(fill="x", pady=5)
            ctk.CTkLabel(frame, text=f"{t['name']} | {t['qualification']} | Группы: {', '.join(t['groups'])}").pack(padx=10, anchor='w')
        ctk.CTkButton(self.current_frame, text="Назад", command=self.show_admin_panel).pack(pady=10)

    def show_admin_panel(self):
        self.clear_frame()
        ctk.CTkLabel(self.current_frame, text="Панель администратора", font=("Arial", 20, "bold")).pack(pady=10)
        ctk.CTkButton(self.current_frame, text="Регистрация клиента", command=self.register_client, width=300).pack(pady=10)
        ctk.CTkButton(self.current_frame, text="Список клиентов", command=self.list_clients, width=300).pack(pady=10)
        ctk.CTkButton(self.current_frame, text="Список персонала", command=self.list_trainers, width=300).pack(pady=10)
        ctk.CTkButton(self.current_frame, text="Назад", command=self.show_login, width=300).pack(pady=10)

    def show_coach_panel(self):
        self.clear_frame()
        ctk.CTkLabel(self.current_frame, text="Панель тренера", font=("Arial", 20, "bold")).pack(pady=10)
        ctk.CTkButton(self.current_frame, text="Посмотреть мою группу", command=self.view_my_group, width=300).pack(pady=10)
        ctk.CTkButton(self.current_frame, text="Статистика посещений", command=self.view_attendance_stats, width=300).pack(pady=10)
        ctk.CTkButton(self.current_frame, text="Назад", command=self.show_login, width=300).pack(pady=10)

    def view_my_group(self):
        self.clear_frame()
        ctk.CTkLabel(self.current_frame, text="Моя группа", font=("Arial", 18, "bold")).pack(pady=10)
        my_name = users[self.username]["name"]

        def mark_attendance(client_idx):
            clients[client_idx]["attendance"].append(datetime.now().strftime("%Y-%m-%d"))
            self.view_my_group()

        def unmark_attendance(client_idx):
            if clients[client_idx]["attendance"]:
                clients[client_idx]["attendance"].pop()
                self.view_my_group()

        found = False
        client_list_frame = ctk.CTkScrollableFrame(self.current_frame)
        client_list_frame.pack(fill="both", expand=True)

        for idx, client in enumerate(clients):
            if client.get("assigned_coach") == my_name:
                found = True
                frame = ctk.CTkFrame(client_list_frame)
                frame.pack(fill="x", pady=5, padx=10)

                today = datetime.now().date()
                pass_end = datetime.strptime(client["pass_end"], "%Y-%m-%d").date() if client["pass_end"] != "Не указан" else None
                color = "#ccffcc" if client.get("payment_status", "") == "Оплачено" else "#ffcccc"
                frame.configure(fg_color=color)

                info = f"{client.get('surname', '-')} {client.get('name', '-')} | Здоровье: {client.get('health_issues', '-')}" \
                       f" | Посещений: {len(client.get('attendance', []))}"
                ctk.CTkLabel(frame, text=info, justify="left").pack(padx=10, anchor='w')

                btn_frame = ctk.CTkFrame(frame)
                btn_frame.pack(fill="x", pady=2)
                ctk.CTkButton(btn_frame, text="Редактировать план", width=120,
                              command=lambda i=idx: self.edit_workout_plan(i)).pack(side="left", padx=5)
                ctk.CTkButton(btn_frame, text="Отметить посещение", width=120,
                              command=lambda i=idx: mark_attendance(i)).pack(side="left", padx=5)

        if not found:
            ctk.CTkLabel(self.current_frame, text="Вы не назначены ни одной группе", text_color="red").pack(pady=10)
        ctk.CTkButton(self.current_frame, text="Назад", command=self.show_coach_panel).pack(pady=10)

    def view_attendance_stats(self):
        self.clear_frame()
        ctk.CTkLabel(self.current_frame, text="Статистика посещений", font=("Arial", 18, "bold")).pack(pady=10)
        my_name = users[self.username]["name"]
        total_visits = 0
        client_list_frame = ctk.CTkScrollableFrame(self.current_frame)
        client_list_frame.pack(fill="both", expand=True)
        for client in clients:
            if client.get("assigned_coach") == my_name:
                visits = len(client.get("attendance", []))
                total_visits += visits
                frame = ctk.CTkFrame(client_list_frame)
                frame.pack(fill="x", pady=5, padx=10)
                info = f"{client.get('surname', '-')} {client.get('name', '-')} — {visits} посещений"
                ctk.CTkLabel(frame, text=info).pack(padx=10, anchor='w')
        ctk.CTkLabel(self.current_frame, text=f"\nОбщее количество посещений: {total_visits}", font=("Arial", 14)).pack()
        ctk.CTkButton(self.current_frame, text="Назад", command=self.show_coach_panel).pack(pady=10)

if __name__ == "__main__":
    app = GymApp()
    app.mainloop()