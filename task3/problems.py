@classmethod
def buy(cls, user, item_id):
    product_qs = Product.objects.filter(item_id=item_id)
    if product_qs.exists():
        product = product_qs[0]
    if product.available:
        # списание средств со счета пользователя
        user.withdraw(product.price)
        # информация о купленном товаре
        send_email_to_user_of_buy_product(user)
        product.available = False
        product.buyer = user
        product.save()
        return True
    else:
        return False

# Проблемы (отсортированы не по важности)
# 1) Нет смысла применять метод filter, если желаемого объекта нет - нужно выходить из метода
# 2) Проверку на available можно было бы перевернуть, не делая индентацию для почти всего кода метода
# 3) Код, начинающийся с if product.available должен быть в первом if, т.к. exists может вернуть False,
# и это тоже можно было бы перевернуть, сделав обратную проверку
# 4) А вообще если available = False, то выходить из метода
# 5) Списание и назначение продукту юзера должны быть атомарной операцией
# 6) Отправка письма на почту должна быть после того, как транзакция успешно завершилась, и вообще не в этом методе
# (следуем single responsibility)
# 7) Возврат булевого значения методом с названием buy нарушает command-query separation
# 8) Булевое значение мало о чем говорит - неясна причина, почему не удалось произвести покупку
