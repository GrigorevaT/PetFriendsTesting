from api import PetFriends
from settings import valid_email, valid_password
from settings import incorrect_email, incorrect_password

import os

pf = PetFriends()

#1
def test_get_api_key_correct_emal_incorrect_password(email=valid_email, password=incorrect_password):
    """Проверяем получение ключа с некорректным паролем и валидным email"""

    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert 'key' not in result

#2
def test_get_api_key_incorrect_emal_correct_password(email=incorrect_email, password=valid_password):
    """Проверяем получение ключа с некорректным email и валидным паролем"""

    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert 'key' not in result

#3
def test_get_api_key_incorrect_emal_incorrect_password(email=incorrect_email, password=incorrect_password):
    """Проверяем получение ключа с некорректным email и некорректным паролем"""

    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert 'key' not in result

#4
def test_get_all_pets_with_invalid_key(filter = ''):
    """Проверяем получение списка питомцев с использованием невалидного ключа"""

    auth_key = {'key': '123'}

    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status != 200

#5
def test_add_new_pet_without_photo_valid_data(name='Белка', animal_type='белка-летяга', age='1'):
    """Проверяем, что можно добавить питомца с корректными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

#6
def test_add_new_pet_without_photo_invalid_data_name(name=123, animal_type='белка', age='2'):
    """Проверяем, что можно добавить питомца с некорректными данными, в имя введем число"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status != 200
    assert result['name'] != name

#7
def test_add_new_pet_without_photo_invalid_data_age(name='Белка', animal_type='белка', age='Питомец'):
    """Проверяем, что можно добавить питомца с некорректными данными, в возраст введем слово"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status != 200
    assert result['name'] != name

#8
def test_add_new_pet_without_photo_invalid_data(name='Белка', age='2'):
    """Проверяем, что можно добавить питомца с некорректными данными, введем меньшее количество данных"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, age)
    assert status != 200
    assert result['name'] != name

#9
def test_add_photo_with_valid_data(pet_photo='images/belka.jpg'):
    """Поверяем возможность добавления фото ранее созданному питомцу"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.add_new_photo(auth_key, pet_id, pet_photo)
        assert status == 200
        assert result['pet_photo'] == pet_photo
    else:
        raise Exception("There is no my pets")

#10
def test_add_photo_with_invalid_data(pet_photo='belka.txt'):
    """Поверяем возможность добавления фото недопустимого формата ранее созданному питомцу"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.add_new_photo(auth_key, pet_id, pet_photo)
        assert status != 200
        assert result['pet_photo'] != pet_photo
    else:
        raise Exception("There is no my pets")



