import screen_brightness_control as sbc


def get_brightness():
    current_brightness = sbc.get_brightness()
    return current_brightness


def set_brightness(brightness):
    # `fade_brightness` может занять > 5 секунд при большой разнице значений.
    # Сделаем плавное изменение быстрее, чтобы HTTP-запрос не падал по timeout.
    sbc.fade_brightness(brightness, interval=0.01)
    return True
