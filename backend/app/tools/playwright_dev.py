from playwright.sync_api import sync_playwright
import requests
from tools.extensions import random_user_agent, random_mail


class PlaywrightManager:
    def __init__(self):
        self.headless = True  # not visible Ui interface
        self.proxy = {"server": "socks5://tor:9050"}
        self.user_agent = random_user_agent.random  # Получение рандомный User-Agent
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def check_my_ip(self):
        response = requests.get('https://api.ipify.org', proxies=self.proxy)
        print(f'My public IP address is: {response.text}\n')

    def open_browser(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            proxy=self.proxy
        )
        self.context = self.browser.new_context(user_agent=self.user_agent)
        print("<--------------------------- start browser --------------------->")
        self.check_my_ip()

    def open_page(self, url):
        page = self.context.new_page()
        page.goto(url)

        # Ожидаем загрузки страницы
        page.wait_for_load_state("networkidle")

        print(f"[+] Page opened -> {url}")

        return page

    def wait_for_navigation(self, timeout=40000):
        if self.page:
            self.page.wait_for_navigation(timeout=timeout)
        else:
            print("[-] Регистрация прервана")

    @staticmethod
    def js_code_to_modify_select(selector_name: str, select_value: str) -> str:
        return """
            document.querySelectorAll('select[name=%s] option').forEach(option => {
                if (option.value == %s) {
                    option.setAttribute('selected', '1');
                } else {
                    option.removeAttribute('selected');
                }
            });
            """ % (selector_name, str(select_value))

    @staticmethod
    def js_code_to_modify_radio(select_value: str) -> str:
        return """
            (form) => {
                let maleOption = form.querySelector('input[name="sex"][value="%s"]');
                if (maleOption) {
                    maleOption.checked = true;
                }
            }
            """ % select_value

    @staticmethod
    def js_code_to_modify_hidden_input(select_value: str) -> str:
        return """
            var hiddenInput = document.querySelector('input[name="reg_email_confirmation__"]');
            if (hiddenInput) {
                hiddenInput.style.display = 'block';
                hiddenInput.value = '%s';
            }
            """ % select_value

    @staticmethod
    def check_selected_option(list_selector: list, std_name: str):
        # Вывод выбраного значенийя <option> элемента
        for option in list_selector:
            selected = option.get_attribute('selected')
            if selected:
                value_day = option.get_attribute('value')
                print(f'[+] {std_name}:', value_day)

    def register_facebook_user(self, page, user_data):
        # Найти форму по XPath
        form = page.locator('xpath=//*[@id="reg"]')
        print(form)

        # Найти все элементы input внутри формы
        xpath_firstname = 'xpath=//*[@name="firstname"]'
        form.locator(xpath_firstname).fill(user_data.get("first_name"))
        print('[+] Имя:', form.locator(xpath_firstname).input_value())

        xpath_lastname = 'xpath=//*[@name="lastname"]'
        form.locator(xpath_lastname).fill(user_data.get("last_name"))
        print('[+] Фамилия:', form.locator(xpath_lastname).input_value())

        xpath_email = 'xpath=//*[@name="reg_email__"]'
        form.locator(xpath_email).fill(user_data.get("email"))
        print('[+] email:', form.locator(xpath_email).input_value())

        xpath_password = 'xpath=//*[@name="reg_passwd__"]'
        form.locator(xpath_password).fill(user_data.get("password"))
        print('[+] password:', form.locator(xpath_password).input_value())

        # Найти скрытый элемент по селектору и установить значение через JavaScript
        xpath_email_confirm = 'xpath=//*[@name="reg_email_confirmation__"]'
        page.evaluate(
            self.js_code_to_modify_hidden_input(user_data.get("email"))
        )
        print('[+] email_2:', form.locator(xpath_email_confirm).input_value())

        # --------------- birthday_month -------------
        xpath_birthday_month = 'xpath=//*[@name="birthday_month"]'
        # Выбор нужного <option> элемента и добавление атрибута selected
        form.locator(xpath_birthday_month).evaluate(
            self.js_code_to_modify_select(
                selector_name="birthday_month", select_value=user_data.get("month")
            )
        )
        # Вывод выбраного значения <option> в <select>
        self.check_selected_option(form.locator(xpath_birthday_month).locator('option').all(), 'Месяц')

        # --------------- birthday_day -------------
        xpath_birthday_day = 'xpath=//*[@name="birthday_day"]'
        # Выбор нужного <option> элемента и добавление атрибута selected
        form.locator(xpath_birthday_day).evaluate(
            self.js_code_to_modify_select(
                selector_name="birthday_day", select_value=str(user_data.get("day"))
            )
        )
        # Вывод выбраного значения <option> в <select>
        self.check_selected_option(form.locator(xpath_birthday_day).locator('option').all(), 'День')

        # --------------- birthday_year -------------
        xpath_birthday_year = 'xpath=//*[@name="birthday_year"]'
        # Выбор нужного <option> элемента и добавление атрибута selected
        form.locator(xpath_birthday_year).evaluate(
            self.js_code_to_modify_select(
                selector_name="birthday_year", select_value=str(user_data.get("year"))
            )
        )
        # Вывод выбраного значения <option> в <select>
        self.check_selected_option(form.locator(xpath_birthday_year).locator('option').all(), 'Год')

        # ----------------- radio select ----------------------------------->
        gender_id = None
        if user_data.get("gender") == 'female':
            gender_id = 1
        if user_data.get("gender") == 'male':
            gender_id = 2
        print("gender_id", gender_id)
        form.evaluate(
            self.js_code_to_modify_radio(str(gender_id))
        )

        for radio in form.locator('xpath=//*[@name="sex"]').all():
            if radio.is_checked():
                radio_sex = int(radio.input_value())
                if radio_sex == 1:
                    print('[+] Пол:', 'Женщина')
                if radio_sex == 2:
                    print('[+] Пол:', 'Мужчина')

        # Нажимаем на кнопку регистрации и ждем навигации
        with page.expect_navigation():
            form.evaluate(
                """
                document.querySelector('xpath=//*[@name="websubmit"]').click();
                """
            )

        # -----------------------------------------------------------------------------------------------

        # переходим на станицу подтверждения регистрации
        new_url = page.url
        print(f"New URL after navigation: {new_url}")

        # # Кнопка продолжить
        # page.evaluate(
        #     """
        #     var elements = document.querySelectorAll('[role="button"]');
        #     elements.forEach(function(element) {
        #         if (element) {
        #             element.click();
        #         }
        #     });
        #     """
        # )
        #
        # # Кнопка решить задачу
        # form_task = page.locator('xpath=//*[@id="root"]')
        # form_task.evaluate(
        #     """
        #     var elements = document.querySelector('[role="button"]');
        #     if (element) {
        #         element.click();
        #     };
        #     """
        # )
        #
        #
        #
        #
        # code_fb = random_mail.get_code_by_facebook(user_data.get("inboxId"))
        # print("code_fb:", code_fb)

        # page.get_by_label("FB-").click()
        # page.get_by_label("FB-").fill("20763")
        # page.get_by_role("button", name="Продолжить").click()
        # page.get_by_role("button", name="ОК").click()
        #
        # # ---------------------
        # self.context.close()
        # self.browser.close()
        #

# test_data = {
#     'day': 11, 'month': 8, 'year': 1979, 'full_date': '1979-8-11', 'gender': 'female', 'first_name': 'Leslie',
#     'last_name': 'Walker', 'email': 'd4732209-0b63-4c7c-88da-4d6718133231@mailslurp.net',
#     'inboxId': 'd4732209-0b63-4c7c-88da-4d6718133231', 'password': '$nL~ASFX'
# }
