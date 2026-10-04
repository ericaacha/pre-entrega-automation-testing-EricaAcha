import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


@pytest.fixture(scope="module")
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    yield driver 

    driver.quit()


def test_login(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    assert "https://www.saucedemo.com/inventory.html" in driver.current_url; f"ERROR: No se redirigió a la página de inventario, la URL actual es {driver.current_url}"


def test_login_successful_title(driver):
    app_logo = driver.find_element(By.CLASS_NAME, "app_logo").text
    assert "Swag Labs" == app_logo; f"ERROR: El titulo no es Swag Labs"


def test_catalogo_con_productos (driver):
    inventory_list = driver.find_element(By.CLASS_NAME, "inventory_list")
    inventory_items = inventory_list.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(inventory_items) > 0, "ERROR: No hay productos en el catálogo"


def test_primer_producto_name(driver):
    inventory_list = driver.find_element(By.CLASS_NAME, "inventory_list")
    first_item = inventory_list.find_elements(By.CLASS_NAME, "inventory_item")[0]
    item_name = first_item.find_element(By.CLASS_NAME, "inventory_item_name").text
    assert item_name == "Sauce Labs Backpack", f"ERROR: El primer producto no es Sauce Labs Backpack, es {item_name}"


def test_primer_producto_precio(driver):
    inventory_list = driver.find_element(By.CLASS_NAME, "inventory_list")
    first_item = inventory_list.find_elements(By.CLASS_NAME, "inventory_item")[0]
    item_price = first_item.find_element(By.CLASS_NAME, "inventory_item_price").text
    assert item_price == "$29.99", f"ERROR: El precio del primer producto no es $29.99, es {item_price}"



def test_agregar_producto_al_carrito(driver):
    inventory_list = driver.find_element(By.CLASS_NAME, "inventory_list")
    first_item = inventory_list.find_elements(By.CLASS_NAME, "inventory_item")[0]
    add_to_cart_button = first_item.find_element(By.CLASS_NAME, "btn_inventory")
    add_to_cart_button.click()

    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    assert cart_badge == "1", f"ERROR: El carrito no tiene 1 producto, tiene {cart_badge}"


def test_ir_al_carrito(driver):
    cart_link = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    cart_link.click()

    assert "https://www.saucedemo.com/cart.html" in driver.current_url, f"ERROR: No se redirigió al carrito, la URL actual es {driver.current_url}"


def test_verificar_producto_en_carrito(driver):
    element_carrito = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
    assert element_carrito == "Sauce Labs Backpack", f"ERROR: El producto en el carrito no es Sauce Labs Backpack, es {element_carrito}"