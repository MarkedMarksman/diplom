from django.dispatch import receiver, Signal
from django_rest_passwordreset.signals import reset_password_token_created

from .models import ConfirmEmailToken, User
from .forms import UserAvatar

from .tasks import send_email

new_user_registered = Signal('user_id')

new_order = Signal('user_id')

avatar_upload = Signal('user_id')


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    """
    Отправляем письмо с токеном для сброса пароля
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    message = f'Token {reset_password_token.key}'
    email = reset_password_token.user
    send_email(message, email)


@receiver(new_user_registered)
def new_user_registered_signal(user_id, **kwargs):
    """
    отправляем письмо с подтверждением почты
    """
    # send an e-mail to the user
    token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)
    message = token.key
    email = token.user.email
    send_email(message, email)


@receiver(new_order)
def new_order_signal(user_id, **kwargs):
    """
    отправяем письмо при изменении статуса заказа
    """
    # send an e-mail to the user
    user = User.objects.get(id=user_id)
    title = "Обновление статуса заказа"
    message = 'Заказ сформирован'
    email = user.email
    send_email.apply_async((title, message, email), countdown=60)
    
@receiver(avatar_upload)
def upload_avatar(request,**kwargs):
    if request.method == 'POST':
        form = UserAvatar(request.POST, request.FILES)
        if form.is_valid():
            
            apply_async.form.save()
        else:
            context = {'form':UserAvatar()}
            return apply_async.render(request,'upload_avatar.html', context)
    context = {'form':UserAvatar()}
    return apply_async((render(request,'upload_avatar.html', context),countdown))

