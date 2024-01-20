import yaml
from django.conf import settings
from shop.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
import requests
from shop.celery import app
from yaml import load as load_yaml, Loader
from .models import User, Shop, Category, Product, ProductInfo, Parameter, ProductParameter, ConfirmEmailToken




@app.task()
def send_email(message: str, email: str, *args, **kwargs) -> str:
    title = 'Title'
    email_list = [email]
    try:
        msg = EmailMultiAlternatives(subject=title, body=message, from_email=EMAIL_HOST_USER, to=email_list)
        msg.send()
        return f'Title: {msg.subject}, Message:{msg.body}'
    except Exception as e:
        raise e


@app.task()
def import_shop_data(partner_id, url):
    
    stream = requests.get(url).content
    data = load_yaml(stream, Loader=Loader)
    shop, _ = Shop.objects.get_or_create(name=data['shop'], user_id=partner_id)
    for category in data['categories']:
        category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
        category_object.shops.add(shop.id)
        category_object.save()
    ProductInfo.objects.filter(shop_id=shop.id).delete()
    for item in data['goods']:
        product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])

        product_info = ProductInfo.objects.create(product_id=product.id,
                                                model=item['model'],
                                                price=item['price'],
                                                price_rrc=item['price_rrc'],
                                                quantity=item['quantity'],
                                                shop_id=shop.id)
        for name, value in item['parameters'].items():
            parameter_object, _ = Parameter.objects.get_or_create(name=name)
            ProductParameter.objects.create(product_info_id=product_info.id,
                                            parameter_id=parameter_object.id,
                                            value=value)
            
@app.task()
def get_user_image(request):
    if request.method == 'POST':
        form = UploadFile.obje
    requests.FILES()