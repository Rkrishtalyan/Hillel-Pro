# ---- Import Statements ----
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


# ---- Email Utility Function ----

def send_email(subject, template_name, context, recipient_list, from_email=None):
    """
    Send an email using a rendered HTML template.

    :param subject: The subject of the email.
    :type subject: str
    :param template_name: The path to the email template.
    :type template_name: str
    :param context: Context data to render the template.
    :type context: dict
    :param recipient_list: A list of recipient email addresses.
    :type recipient_list: list
    :param from_email: The sender's email address (default: None).
    :type from_email: str or None
    """
    if from_email is None:
        from_email = 'rkrishtalyan@gmail.com'
    message = render_to_string(template_name, context)
    email = EmailMessage(subject, message, from_email, recipient_list)
    email.content_subtype = 'html'
    email.send()
