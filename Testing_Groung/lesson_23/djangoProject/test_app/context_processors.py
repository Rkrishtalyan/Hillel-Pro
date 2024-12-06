from ipware import get_client_ip


def site_settings(request):
    """Додає загальні налаштування сайту у всі шаблони."""
    return {
        'site_name': 'Мій дивовижний сайт',
        'current_year': 2024,
    }


def get_client_ip_address(request):
    """
    Получает IP-адрес клиента из запроса.
    Возвращает '0.0.0.0', если IP определить не удалось.
    """
    ip, is_routable = get_client_ip(request)
    return {
        'ip': str(ip) if ip else '0.0.0.0',
    }
