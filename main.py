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
    taxi_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[1]/div[3]/div[1]/button')
    comfort_button = (By.XPATH, '/html/body/div/div/div[3]/div[3]/div[2]/div[1]/div[5]')
    phone_button = (By.CLASS_NAME, 'np-button')
    phone_field = (By.ID, 'phone')
    next_button = (By.XPATH, '/html/body/div/div/div[1]/div[2]/div[1]/form/div[2]/button')
    phone_code = (By.ID, 'code')
    confirm_button = (By.XPATH, '/html/body/div/div/div[1]/div[2]/div[2]/form/div[2]/button[1]')
    payment_button = (By.CSS_SELECTOR, '.pp-button.filled')
    add_card_button = (By.CSS_SELECTOR, '.pp-row.disabled')
    number_card_field = (By.ID, 'number')
    code_card_field = (By.XPATH, '/html/body/div/div/div[2]/div[2]/div[2]/form/div[1]/div[2]/div[2]/div[2]/input')
    link_button = (By.XPATH, '/html/body/div/div/div[2]/div[2]/div[2]/form/div[3]/button[1]')
    close_window_button = (By.XPATH, '/html/body/div/div/div[2]/div[2]/div[1]/button')
    comment_field = (By.ID, 'comment')
    slide_button = (By.CLASS_NAME, 'slider.round')
    ice_cream = (By.XPATH, '/html/body/div/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')
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

    def set_phone_number(self, phone): #Se ingresará un número telefónico en ésta área
        self.driver.find_element(*self.phone_button).click() #se hará click para agregar número
        self.driver.find_element(*self.phone_field).send_keys(phone) #Se ingresará el número telefónico
        self.driver.find_element(*self.next_button).click() #botón siguiente

    def set_confirmation_code(self): #Para ingresar SMS
        self.driver.find_element(*self.phone_code).send_keys(retrieve_phone_code(self.driver))#INGRESA CÓDIGO
        self.driver.find_element(*self.confirm_button).click() #botón para confirmar código

    def set_payment_method(self, card, code_card): #Se ingresa método de pago
        self.driver.find_element(*self.payment_button).click() #Click al botón para abrir campo de forma de pago
        self.driver.find_element(*self.add_card_button).click() #Click en botoón para ingresar una tarjeta de crédito
        self.driver.find_element(*self.number_card_field).send_keys(card) #Ingreso de número tarjeta
        self.driver.find_element(*self.code_card_field).send_keys(code_card) #Ingreso de número de código Seguridad
        self.driver.find_element(*self.code_card_field).send_keys(Keys.TAB) #Confirma código
        self.driver.find_element(*self.link_button).click() #Click en botón para continuar
        self.driver.find_element(*self.close_window_button).click() #Cierra ventana

    def set_comment(self, message): #Ingresar comentario
        self.driver.find_element(*self.comment_field).send_keys(message) #Click en campo de comentarios
        return self.driver.find_element(*self.comment_field).get_property('value')

    def get_manta_panuelos(self): #Se agrega una manta
        self.driver.find_element(*self.slide_button).click() #se clickea el botón para acceder a esa opción

    def get_ice_cream(self): #se piden dos helados en un click (X2)
        self.driver.find_element(*self.ice_cream).click()
        self.driver.find_element(*self.ice_cream).click()

    def click_order_taxi_button(self): #Botón con click para solicitar un taxi
        self.driver.find_element(*self.call_taxi_button).click()

    #Esperar a que aparezca la información del conductor en el modal
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
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

        routes_page.click_taxi_button()
        routes_page.click_comfort_button()

        phone = data.phone_number
        routes_page.set_phone_number(phone)

        routes_page.set_confirmation_code()

        card = data.card_number
        code_card = data.card_code
        routes_page.set_payment_method(card, code_card)

        message = data.message_for_driver
        routes_page.set_comment(message)

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