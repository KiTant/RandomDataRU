import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import requests

# Установка внешнего вида программы
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Настройка основных свойств окна
        self.title("RandomDataRU")
        self.geometry("1000x500")
        self.minsize(1000, 350)
        self.maxsize(1250, 1000)

        self.last_data = ""

        # Инициализация компонентов интерфейса
        self._initialize_components()

    def _initialize_components(self):
        # Меню с опциями для выбора гендера
        self.gender_options = ctk.CTkOptionMenu(self, values=["Любой", "Мужчина", "Женщина"])
        self.gender_options.place(relx=0.025, rely=0.05, relwidth=0.15)

        # Кнопка для создания данных
        self.generate_data_btn = ctk.CTkButton(self, text="Сгенерировать данные", command=self.generate_data)
        self.generate_data_btn.place(relx=0.185, rely=0.05, relwidth=0.155)

        # Кнопка для копирования данных
        self.copy_generated_data_btn = ctk.CTkButton(self, text="Скопировать последние сгенерированные данные",
                                                     command=self.copy_data)
        self.copy_generated_data_btn.place(relx=0.35, rely=0.05, relwidth=0.325)

        # Кнопка для удаления данных из памяти
        self.clear_generated_data_btn = ctk.CTkButton(self, text="Очистить последние сгенерированные данные",
                                                      command=self.clear_data)
        self.clear_generated_data_btn.place(relx=0.685, rely=0.05, relwidth=0.305)

        # Текстбокс для отображения сгенерированных данных
        self.data_textbox = ctk.CTkTextbox(self, corner_radius=25)
        self.data_textbox.place(relx=0.025, rely=0.125, relwidth=0.95, relheight=0.85)

    def generate_data(self):
        req = requests.get(f'https://api.randomdatatools.ru/?'
                            f'source=rdt&'
                            f'gender={self.gender_options.get().replace("Мужчина", "man").replace("Женщина", "woman").replace("Любой", "unset")}'
                            f'&typeName=classic')
        if not req.ok:
            CTkMessagebox(title="Ошибка при генерировании данных",
                          message="API сервис не отвечает, попробуйте ещё раз",
                          icon="cancel", option_1="Ок", sound=True)
            return

        self.data_textbox.delete("0.0", "end")
        json = req.json()
        data = "Основная информация:\n"\
               f"ФИО: {json['LastName']} {json['FirstName']} {json['FatherName']}\n" \
               f"Номер телефона: {json['Phone']}\n" \
               f"Дата рождения: {json['DateOfBirth']} ({json['YearsOld']} лет)\n" \
               f"Адрес проживания: {json['Address']}\n" \
               f"Электронная почта: {json['Email']}\n" \
               f"\nО паспорте:\n" \
               f"Серия/Номер паспорта: {json['PasportNum']}\nКем выдан: {json['PasportOtd']}\n" \
               f"Дата выдачи: {json['PasportDate']}\nКод подразделения: {json['PasportCode']}\n" \
               f"Адрес регистрации: {json['AddressReg']}\n" \
               f"\nО автомобиле:\n" \
               f"Марка и модель: {json['CarBrand']} {json['CarModel']}\n" \
               f"Год выпуска и цвет: {json['CarYear']} {json['CarColor']}\n" \
               f"Гос.номер: {json['CarNumber']}\nVIN: {json['CarVIN']}\n" \
               f"Серия/Номер СТС и дата выдачи: {json['CarSTS']} {json['CarSTSDate']}\n" \
               f"Серия/Номер ПТС и дата выдачи: {json['CarPTS']} {json['CarPTSDate']}\n" \
               f"\nО образовании:\n" \
               f"Учебное заведение: {json['EduName']}\nСерия/Номер диплома: {json['EduDocNum']}\n" \
               f"Направление: {json['EduProgram']}\nСпециальность: {json['EduSpecialty']}\n" \
               f"Регистрационный номер: {json['EduRegNumber']}\nГод окончания обучения: {json['EduYear']}\n" \
               f"\nДокументы:\n" \
               f"ИНН ФЛ/ИП: {json['inn_fiz']}\nИНН ЮЛ: {json['inn_ur']}\n" \
               f"СНИЛС: {json['snils']}\nОМС: {json['oms']}\n" \
               f"ОГРН: {json['ogrn']}\nКПП: {json['kpp']}\n" \
               f"\nПлатёжная информация:\n" \
               f"БИК банка: {json['bankBIK']}\n" \
               f"Корреспондентский счёт: {json['bankCorr']}\n" \
               f"ИНН и КПП банка: {json['bankINN']}; {json['bankKPP']}\n" \
               f"Номер счёта: {json['bankNum']}\n" \
               f"Имя владельца карты: {json['bankClient']}\n" \
               f"Номер кредитной карты: {json['bankCard']}\n" \
               f"Срок действия карты: {json['bankDate']}\n" \
               f"CVC/CVV код: {json['bankCVC']}"
        self.last_data = data
        self.data_textbox.insert("0.0", data)

    def copy_data(self):
        data = self.last_data.strip()
        if not data:
            CTkMessagebox(title="Предупреждение о копировании данных",
                          message="Пожалуйста сгенерируйте данные чтобы их скопировать",
                          icon="warning", option_1="Ок", sound=True)
            return
        self.clipboard_clear()
        self.clipboard_append(self.last_data)
        CTkMessagebox(title="Копирование данных", message="Данные успешно скопированы",
                      icon="check", option_1="Ok", topmost=False)

    def clear_data(self):
        data = self.last_data.strip()
        if not data:
            CTkMessagebox(title="Предупреждение о копировании данных",
                          message="Пожалуйста  сгенерируйте данные чтобы их стереть из памяти",
                          icon="warning", option_1="Ок", sound=True)
            return
        self.data_textbox.delete("0.0", "end")
        self.last_data = ""

if __name__ == '__main__':
    app = App()
    app.mainloop()
