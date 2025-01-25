import screen_brightness_control as sbc


def get_brightness():
    current_brightness = sbc.get_brightness()
    return current_brightness


def set_brightness(brightness):
    sbc.fade_brightness(brightness, interval=0.1)
    return True
