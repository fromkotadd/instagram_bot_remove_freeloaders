from auto_login_insta import login
from selenium import webdriver
from auth_data import username, password, nickname
import time
import random


# метод отписки, отписываемся от всех кто не подписан на нас
def smart_unsubscribe(username):
	browser = webdriver.Chrome(r'chromedriver.exe')
	login(username, password, browser)
	browser.get(f"https://www.instagram.com/{nickname}/")
	time.sleep(random.randrange(3, 6))

	followers_button = browser.find_element_by_xpath(
		"/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span")
	followers_count = followers_button.get_attribute("title")

	following_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")
	following_count = following_button.find_element_by_tag_name("span").text

	time.sleep(random.randrange(3, 6))

	# если количество подписчиков больше 999, убираем из числа запятые
	if ',' in followers_count or following_count:
		followers_count, following_count = int(''.join(followers_count.split(','))), int(
			''.join(following_count.split(',')))
	else:
		followers_count, following_count = int(followers_count), int(following_count)

	print(f"Количество подписчиков: {followers_count}")
	followers_loops_count = int(followers_count / 12) + 1
	print(f"Число итераций для сбора подписчиков: {followers_loops_count}")

	print(f"Количество подписок: {following_count}")
	following_loops_count = int(following_count / 12) + 1
	print(f"Число итераций для сбора подписок: {following_loops_count}")

	# собираем список подписчиков
	followers_button.click()
	time.sleep(random.randrange(4, 6))

	followers_ul = browser.find_element_by_class_name("isgrP")
	time.sleep(random.randrange(4, 6))

	try:
		followers_urls = []
		print("Запускаем сбор подписчиков...")
		for i in range(1, followers_loops_count + 1):
			browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
			time.sleep(random.randrange(2, 4))
			print(f"Итерация #{i}")

		all_urls_div = followers_ul.find_elements_by_tag_name("li")

		for url in all_urls_div:
			url = url.find_element_by_tag_name("a").get_attribute("href")
			followers_urls.append(url)

		# сохраняем всех подписчиков пользователя в файл
		with open(f"{nickname}_followers_list.txt", "w") as followers_file:
			for link in followers_urls:
				followers_file.write(link + "\n")
	except Exception as ex:
		print(ex)
		browser.close()
		browser.quit()

	time.sleep(random.randrange(4, 6))
	browser.get(f"https://www.instagram.com/{nickname}/")
	time.sleep(random.randrange(3, 6))

	# собираем список подписок
	following_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")
	following_button.click()
	time.sleep(random.randrange(3, 5))

	following_ul = browser.find_element_by_class_name("isgrP")

	try:
		following_urls = []
		print("Запускаем сбор подписок")

		for i in range(1, following_loops_count + 1):
			browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", following_ul)
			time.sleep(random.randrange(2, 4))
			print(f"Итерация #{i}")

		all_urls_div = following_ul.find_elements_by_tag_name("li")

		for url in all_urls_div:
			url = url.find_element_by_tag_name("a").get_attribute("href")
			following_urls.append(url)

		# сохраняем всех подписок пользователя в файл
		with open(f"{nickname}_following_list.txt", "w") as following_file:
			for link in following_urls:
				following_file.write(link + "\n")

		"""Сравниваем два списка, если пользователь есть в подписках, но его нет в подписчиках,
		заносим его в отдельный список"""

		count = 0
		unfollow_list = []
		for user in following_urls:
			if user not in followers_urls:
				count += 1
				unfollow_list.append(user)
		print(f"Нужно отписаться от {count} пользователей")

		# сохраняем всех от кого нужно отписаться в файл
		with open(f"{nickname}_unfollow_list.txt", "w") as unfollow_file:
			for user in unfollow_list:
				unfollow_file.write(user + "\n")

		print('Список создан')
		print("Запускаем отписку...")
		time.sleep(2)

		# заходим к каждому пользователю на страницу и отписываемся
		with open(f"{nickname}_unfollow_list.txt") as unfollow_file:
			unfollow_users_list = unfollow_file.readlines()
			unfollow_users_list = [row.strip() for row in unfollow_users_list]

		try:
			count = len(unfollow_users_list)
			for user_url in unfollow_users_list:
				browser.get(user_url)
				time.sleep(random.randrange(4, 6))

				# кнопка отписки
				unfollow_button = browser.find_element_by_class_name("glyphsSpriteFriend_Follow")

				time.sleep(random.randrange(4, 6))
				unfollow_button.click()

				time.sleep(random.randrange(4, 6))

				# подтверждение отписки
				unfollow_button_confirm = browser.find_element_by_class_name("mt3GC").find_element_by_class_name(
					"aOOlW")
				unfollow_button_confirm.click()

				print(f"Отписались от {user_url}")
				count -= 1
				if not count:
					print('удаление завершенно')
				print(f"Осталось отписаться от: {count} пользователей")

				time.sleep(random.randrange(20, 30))


		except Exception as ex:
			print(ex)
			browser.close()
			browser.quit()

	except Exception as ex:
		print(ex)
		browser.close()
		browser.quit()

	time.sleep(random.randrange(4, 6))
	browser.close()
	browser.quit()



if __name__ == "__main__":
	smart_unsubscribe(username)
