from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def send_email(subject, template_name, context, recipient_list, from_email=None):
    if from_email is None:
        from_email = 'rkrishtalyan@gmail.com'
    message = render_to_string(template_name, context)
    email = EmailMessage(subject, message, from_email, recipient_list)
    email.content_subtype = 'html'
    email.send()
