from selenium import webdriver
from selenium.webdriver.common.by import By
from settings import valid_password, valid_email
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_show_my_pets(driver):
   driver = webdriver.Chrome()
   # Переходим на страницу авторизации
   driver.get('http://petfriends.skillfactory.ru/login')
   driver.implicitly_wait(10)
   # Вводим email
   field_email = driver.find_element(By.ID, 'email')
   field_email.clear()
   field_email.send_keys(valid_email)
   # Вводим пароль
   field_pass = driver.find_element(By.ID, 'pass')
   field_pass.clear()
   field_pass.send_keys(valid_password)
   # Нажимаем на кнопку входа в аккаунт
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Нажимаем на кнопку "Мои питомцы"
   driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul[1]/li[1]/a[1]').click()

   driver.implicitly_wait(10)
   images = driver.find_elements(By.XPATH, "//tbody//th")
   names = driver.find_elements(By.XPATH, '//tbody//td[1]')
   breed = driver.find_elements(By.XPATH, '//tbody//td[2]')
   age = driver.find_elements(By.XPATH, '//tbody//td[3]')
   driver.implicitly_wait(10)
   num1 = driver.find_element(By.XPATH, '//body/div[1]/div/div[1]').text.split(' ')
   num2 = num1[1].split('\n')
   num_of_pets = int(num2[0])

   # Проверяем, что присутствуют все питомцы
   assert len(names) == num_of_pets

   # Проверяем имена
   names_all = []
   for i in range(len(names)):
      if names[i].text != '':
         names_all.append(names[i].text)
   unique_names = list(set(names_all))
   assert len(names_all) == num_of_pets
   assert len(names_all) == len(unique_names)

   # Проверяем фото
   images_src = []
   for i in range(len(images)):
      if images[i].get_attribute('src') != '':
         images_src.append(images[i].get_attribute('src'))
   assert len(images_src) >= num_of_pets // 2

   # Проверяем породу
   breed_all = []
   for i in range(len(breed)):
      if breed[i].text != '':
         breed_all.append(breed[i].text)
   assert len(breed_all) == num_of_pets

   # Проверяем возраст
   age_all = []
   for i in range(len(breed)):
      if age[i].text != '':
         age_all.append(age[i].text)
   assert len(age_all) == num_of_pets

   # Проверяем уникальность карточек
   WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//tbody//td")))
   pet_cards = driver.find_elements(By.XPATH, "//tbody//td")
   pets = []
   for i in range(0, len(pet_cards), 4):
      pet = [pet_cards[i].text, pet_cards[i+1].text, pet_cards[i+2].text, pet_cards[i+3].text]
      pets.append(pet)
   unique_pets = []
   for pet in pets:
      if pet in unique_pets:
         pass
      else:
         unique_pets.append(pet)
   assert len(pets) == len(unique_pets)

   driver.quit()