"""
2) Уяви, що ти розробляєш систему для відправки повідомлень різними каналами: через SMS, Email та Push-повідомлення.
Усі ці канали мають різні інтерфейси для відправки повідомлень, але ти хочеш уніфікувати їх,
щоб використовувати один універсальний інтерфейс для відправки повідомлень незалежно від каналу.

Реалізуй систему відправки повідомлень, яка приймає список адаптерів і відправляє одне і те ж повідомлення
через усі доступні сервіси.
Додай обробку помилок для кожного сервісу, якщо відправка повідомлення не вдалася.
"""


# ---- Інтерфейс MessageSender ----
class MessageSender:
    """
    Abstract class for message sending services.
    """

    def send_message(self, message: str):
        """
        Send a message. Should be implemented by subclasses.

        :param message: The message to be sent.
        :type message: str
        """
        pass


# ---- Існуючі класи для відправки повідомлень ----
class SMSService:
    """
    Service for sending SMS messages.
    """

    def send_sms(self, phone_number, message):
        """
        Send an SMS to a specified phone number.

        :param phone_number: The recipient's phone number.
        :type phone_number: str
        :param message: The message content.
        :type message: str
        :raises ValueError: If the phone number is invalid.
        """
        if not phone_number:  # Симуляція помилки
            raise ValueError("Неправильний номер телефону!")
        print(f"Відправка SMS на {phone_number}: {message}")


class EmailService:
    """
    Service for sending email messages.
    """

    def send_email(self, email_address, message):
        """
        Send an email message to a specified address.

        :param email_address: The recipient's email address.
        :type email_address: str
        :param message: The message content.
        :type message: str
        :raises ValueError: If the email address is invalid.
        """
        if not email_address:  # Симуляція помилки
            raise ValueError("Невірний формат електронної пошти!")
        print(f"Відправка Email на {email_address}: {message}")


class PushService:
    """
    Service for sending push notifications.
    """

    def send_push(self, device_id, message):
        """
        Send a push notification to a specified device.

        :param device_id: The recipient's device ID.
        :type device_id: str
        :param message: The message content.
        :type message: str
        :raises ValueError: If the device ID is invalid.
        """
        if not device_id:  # Симуляція помилки
            raise ValueError("Невалідний ID пристрою!")
        print(f"Відправка Push-повідомлення на пристрій {device_id}: {message}")


# ---- Адаптери ----
class SMSAdapter(MessageSender):
    """
    Adapter for sending SMS messages using the MessageSender interface.
    """

    def __init__(self, sms_service, phone_number):
        """
        Initialize SMSAdapter with an SMS service and phone number.

        :param sms_service: The service used to send SMS messages.
        :type sms_service: SMSService
        :param phone_number: The phone number to send the SMS to.
        :type phone_number: str
        """
        self.sms_service = sms_service
        self.phone_number = phone_number

    def send_message(self, message: str):
        """
        Send a message via SMS.

        :param message: The message to send.
        :type message: str
        """
        self.sms_service.send_sms(self.phone_number, message)


class EmailAdapter(MessageSender):
    """
    Adapter for sending emails using the MessageSender interface.
    """

    def __init__(self, email_service, email_address):
        """
        Initialize EmailAdapter with an email service and email address.

        :param email_service: The service used to send emails.
        :type email_service: EmailService
        :param email_address: The email address to send the email to.
        :type email_address: str
        """
        self.email_service = email_service
        self.email_address = email_address

    def send_message(self, message: str):
        """
        Send a message via email.

        :param message: The message to send.
        :type message: str
        """
        self.email_service.send_email(self.email_address, message)


class PushAdapter(MessageSender):
    """
    Adapter for sending push notifications using the MessageSender interface.
    """

    def __init__(self, push_service, device_id):
        """
        Initialize PushAdapter with a push service and device ID.

        :param push_service: The service used to send push notifications.
        :type push_service: PushService
        :param device_id: The device ID to send the notification to.
        :type device_id: str
        """
        self.push_service = push_service
        self.device_id = device_id

    def send_message(self, message: str):
        """
        Send a message via push notification.

        :param message: The message to send.
        :type message: str
        """
        self.push_service.send_push(self.device_id, message)


# ---- Функція масової розсилки ----
def send_message_to_all(adapters: list[MessageSender], message: str):
    """
    Send a message via all adapters in the list.

    :param adapters: List of adapters implementing the MessageSender interface.
    :type adapters: list[MessageSender]
    :param message: The message to send.
    :type message: str
    """
    for adapter in adapters:
        try:
            adapter.send_message(message)
        except ValueError as e:
            print(f">>>> Помилка відправки повідомлення через {type(adapter).__name__}: {e}")


# ---- Підготовка до використання ----
sms_service = SMSService()
email_service = EmailService()
push_service = PushService()

sms_adapter = SMSAdapter(sms_service, "+380123456789")
email_adapter = EmailAdapter(email_service, "user@example.com")
push_adapter = PushAdapter(push_service, "device123")

message = "Привіт! Це тестове повідомлення."

# ---- Відправка повідомлень через окремі сервіси ----
print("---- Відправка повідомлень окремими сервісами ----")

sms_adapter.send_message(message)
email_adapter.send_message(message)
push_adapter.send_message(message)

# ---- Відправка повідомлення через всі сервіси одночасно ----
print("\n---- Відправка повідомлень через усі інтерфейси ----")
adapters = [sms_adapter, email_adapter, push_adapter]

send_message_to_all(adapters, message)

# ---- Тестування можливих помилок ----
print("\n---- Тестування можливих помилок ----")
push_adapter = PushAdapter(push_service, "")
adapters = [sms_adapter, email_adapter, push_adapter]

send_message_to_all(adapters, message)
