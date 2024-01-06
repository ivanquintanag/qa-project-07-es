import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage: #rutas de página urbanrouters
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    taxi_button_xpath = "//button[@data-testid='taxi-button']" #nueva estructura
    comfort_button_xpath = "//div[@data-testid='comfort-button-container']//div[@class='button-wrapper']" #nueva estructura
    phone_button = (By.CLASS_NAME, 'np-button')
    phone_field = (By.ID, 'phone')
    next_button_xpath = "//form[@data-testid='login-form']//button[@data-testid='next-button']" #nueva estructura
    phone_code = (By.ID, 'code')
    confirm_button_xpath = "//form[@data-testid='confirmation-form']//button[@data-testid='confirm-button']" #nueva estructura
    payment_button = (By.CSS_SELECTOR, '.pp-button.filled')
    add_card_button = (By.CSS_SELECTOR, '.pp-row.disabled')
    number_card_field = (By.ID, 'number')
    code_card_field_xpath = "//form[@data-testid='code-card-form']//input[@data-testid='code-card-field']" #nueva estructura
    link_button_xpath = "//form[@data-testid='link-form']//button[@data-testid='link-button']" #nueva estructura
    close_window_button_xpath = "//button[@data-testid='close-window-button']" #nureva estructura
    comment_field = (By.ID, 'comment')
    slide_button = (By.CLASS_NAME, 'slider.round')
    ice_cream_xpath = "//div[@data-testid='ice-cream-container']//div[@data-testid='flavor-container']//div[@data-testid='chocolate-flavor']"#nueva estructura
    call_taxi_button = (By.CSS_SELECTOR, '.smart-button')
    modal_element = (By.CSS_SELECTOR, '.order-header-content')

    def __init__(self, driver):
        self.driver = driver

    #Ingresar dirección "From" (Desde)
    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    #Ingresar dirección "To" (Hasta)
    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def set_phone_number(self, phone):
        # Ingresar un número telefónico en el área correspondiente
        self.click_phone_button()  # Hacer clic para agregar un número telefónico
        self.enter_phone(phone)  # Ingresar el número telefónico
        self.click_next_button()  # Hacer clic en el botón siguiente

    def click_phone_button(self):
        # Acciones para hacer clic en el botón para agregar un número telefónico
        self.driver.find_element(*self.phone_button).click()

    def enter_phone(self, phone):
        # Acciones para ingresar el número telefónico
        self.driver.find_element(*self.phone_field).send_keys(phone)

    def click_next_button(self):
        # Acciones para hacer clic en el botón siguiente
        self.driver.find_element(*self.next_button).click()

    def set_confirmation_code(self): #Para ingresar SMS
        self.driver.find_element(*self.phone_code).send_keys(retrieve_phone_code(self.driver))#INGRESA CÓDIGO
        self.driver.find_element(*self.confirm_button).click() #botón para confirmar código

    def set_payment_method(self, card, code_card):
        self.open_payment_form()
        self.add_credit_card(card, code_card)
        self.confirm_payment()

    def set_payment_method(self, card, code_card):
        # Coordinar las acciones necesarias para establecer el método de pago
        self.open_payment_form()  # Abrir el formulario de pago
        self.add_credit_card(card, code_card)  # Ingresar los detalles de la tarjeta de crédito
        self.confirm_payment()  # Confirmar el método de pago

    def open_payment_form(self):
        # Acciones para abrir el formulario de pago
        self.driver.find_element(*self.payment_button).click()  # Click en el botón de pago
        self.driver.find_element(*self.add_card_button).click()  # Click en el botón para agregar una tarjeta de crédito

    def add_credit_card(self, card, code_card):
        # Acciones para ingresar los detalles de la tarjeta de crédito
        self.driver.find_element(*self.number_card_field).send_keys(card)  # Ingreso del número de la tarjeta
        self.driver.find_element(*self.code_card_field).send_keys(code_card)  # Ingreso del código de seguridad
        self.driver.find_element(*self.code_card_field).send_keys(Keys.TAB)  # Confirmar el código de seguridad

    def confirm_payment(self):
        # Acciones para confirmar el método de pago
        self.driver.find_element(*self.link_button).click()  # Click en el botón para continuar
        self.driver.find_element(*self.close_window_button).click()  # Cerrar la ventana de confirmación

    def get_manta_panuelos(self): #Se agrega una manta
        self.driver.find_element(*self.slide_button).click() #se clickea el botón para acceder a esa opción

    def get_ice_cream(self): #se piden dos helados en un click (X2)
        self.driver.find_element(*self.ice_cream).click()
        self.driver.find_element(*self.ice_cream).click()

    def click_order_taxi_button(self): #Botón con click para solicitar un taxi
        self.driver.find_element(*self.call_taxi_button).click()


    def wait_for_load_information(self): #espera a que aparezca información
        WebDriverWait(self.driver, 35).until(EC.presence_of_element_located(self.modal_element))

class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to

        # Establecer la dirección de origen y verificar
        routes_page.set_from(address_from)
        obtained_from = routes_page.get_from()
        assert obtained_from == address_from, f"Esperado '{address_from}', pero se obtuvo '{obtained_from}'"

        # Establecer la dirección de destino y verificar
        routes_page.set_to(address_to)
        obtained_to = routes_page.get_to()
        assert obtained_to == address_to, f"Esperado '{address_to}', pero se obtuvo '{obtained_to}'"

        # Hacer clic en los botones de taxi y confort
        routes_page.click_taxi_button()
        routes_page.click_comfort_button()

        # Establecer el número de teléfono y verificar
        phone = data.phone_number
        routes_page.set_phone_number(phone)
        obtained_phone = routes_page.get_phone_number()
        assert obtained_phone == phone, f"Esperado '{phone}', pero se obtuvo '{obtained_phone}'"

        # Establecer el código de confirmación
        routes_page.set_confirmation_code()

        # Establecer el método de pago y verificar
        card = data.card_number
        code_card = data.card_code
        routes_page.set_payment_method(card, code_card)
        obtained_card = routes_page.get_payment_card()
        assert obtained_card == card, f"Esperado '{card}', pero se obtuvo '{obtained_card}'"

        # Establecer un comentario y verificar
        message = data.message_for_driver
        routes_page.set_comment(message)
        obtained_message = routes_page.get_comment()
        assert obtained_message == message, f"Esperado '{message}', pero se obtuvo '{obtained_message}'"

        # Realizar otras acciones y aserciones según sea necesario
        routes_page.get_manta_panuelos()
        routes_page.get_ice_cream()
        routes_page.click_order_taxi_button()
        routes_page.wait_for_load_information()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

if __name__ == '__main__':
    test_valid = TestUrbanRoutes()
    test_valid.setup_class()
    test_valid.teardown_class()