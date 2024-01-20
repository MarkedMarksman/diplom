from rest_framework.authtoken.models import Token
from .models import Shop, ProductInfo, Order, User, Contact, ConfirmEmailToken
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class ApiTests(APITestCase):
        
    #Регистрация пользователя
    def test_register_account(self):
        count = User.objects.count()
        user = {
                
                "full_name": "Nikita" ,
                "username" : "Moro",
                "email": "admin@admin.ru", 
                "password": "Oreiro1435",
                "company": "Мобильный салон №1",
                "position": "Админстратор склада"
        }

        url = reverse('user-register')
        response = self.client.post(url, user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['Status'], True)
        self.assertEqual(User.objects.count(), count + 1)

    #Подтверждение регистрации
    def test_confirm_register(self):
        user = User.objects.create_user(
                full_name = "Nikita" ,
                username= "Moro",
                email = "admin@admin.ru", 
                password = "Oreiro1435",
                company = "Мобильный салон №1",
                position = "Админстратор склада",
                type = "shop"
        )
        token = ConfirmEmailToken.objects.create(user_id=user.id).key
        url = reverse('user-register-confirm')
        data = {'email': user.email, 'token': token}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['Status'], True)

#Создание контактов пользьзователя
    def test_create_contact(self):
        user = User.objects.create_user(
        full_name = "Nikita" ,
        username= "Moro",
        email = "admin@admin.ru", 
        password = "Oreiro1435",
        company = "Мобильный салон №1",
        position = "Админстратор склада",
        type = "shop",
        is_active=True
        )
        
        url = reverse('user-contact')
        token = Token.objects.create(user=user).key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        data = {'adress': 'Moscow', 'email': user.email, 'phone': '+88805555535'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

#Просмотр данных пользователя
    def test_get_account_details(self):
        url = reverse('user-details')
        user = User.objects.create_user(
                full_name = "Nikita" ,
                username= "Moro",
                email = "admin@admin.ru", 
                password = "Oreiro1435",
                company = "Мобильный салон №1",
                position = "Админстратор склада",
        )
        token = Token.objects.create(user=user).key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
#Изменение данных пользователя
    def test_post_account_details(self):
        url = reverse('user-details')
        user = User.objects.create_user(
        full_name = "Nikita" ,
        username= "Moro",
        email = "admin@admin.ru", 
        password = "Oreiro1435",
        company = "Мобильный салон №1",
        position = "Админстратор склада",
        is_active=True
        )
        updated_user = {'full_name': 'new_one'}
        token = Token.objects.create(user=user).key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.post(url, updated_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['Status'], True)

#Восстановаление пароля
    def test_reset_password(self):
        url = reverse('password-reset')
        User.objects.create_user(
        full_name = "Nikita" ,
        username= "Moro",
        email = "admin@admin.ru", 
        password = "Oreiro1435",
        company = "Мобильный салон №1",
        position = "Админстратор склада",
        )
        data = {'email': 'email@email.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

