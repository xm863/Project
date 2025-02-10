from django.core.mail import send_mail

def task_send_mail(subject1, message1, email):
    subject = subject1
    message = message1
    from_email = 'xamid.obidjon11@gmail.com'
    recipient_list = [email]

    return send_mail(subject, message, from_email, recipient_list, fail_silently=True)