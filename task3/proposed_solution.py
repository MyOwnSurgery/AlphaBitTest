@classmethod
def buy(cls, user, item_id):
    product = Product.objects.get(item_id=item_id)

    if not product.available:
        raise NotAvailable

    with transaction.atomic():
        user.withdraw(product.price)
        product.available = False
        product.buyer = user
        product.save()

    if not Product.objects.exists(item_id=item_id, buyer=user):
        raise TransactionFault

# Лучше считать, что метод отработал, если не бросил исключение
# Вызов метода обернуть в try except, ловить DoesNotExist, MultipleObjectsReturned, NotAvailable, TransactionFault
# Например, на DoesNotExist возвращать 404, bad request или conflict (зависит от контекста),
# на MultipleObjectsReturned, NotAvailable возвращать 409 Conflict, ну и 500 на TransactionFault

# Если все же сильно нужно полное сохранение интерфейса с типом возвращаемого значения, то пусть будет так
@classmethod
def buy(cls, user, item_id):
    product_qs = Product.objects.filter(item_id=item_id)
    if product_qs.count() != 1:
        return False

    product = product_qs.first()

    if not product.available:
        return False

    with transaction.atomic():
        user.withdraw(product.price)
        product.available = False
        product.buyer = user
        product.save()

    if not Product.objects.exists(item_id=item_id, buyer=user):
        return False

    return True
