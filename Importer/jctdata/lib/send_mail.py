import requests
from jctdata import settings


def send_mail(subject, message, attachment, attachment_name="details.json"):
    """Send an email to the status email address, with the given subject and message."""
    print("Sending email: {subject}".format(subject=subject))
    key = settings.MAILGUN_KEY
    url = settings.MAILGUN_DOMAIN
    recipient = settings.STATUS_EMAIL_RECEIVER
    sender = settings.STATUS_EMAIL_SENDER
    subject = "{a}: {b}".format(a=settings.MAILGUN_SUBJECT_PREFIX, b=subject)
    files = {}
    if attachment:
        files = {"attachment": (attachment_name, open(attachment, 'rb'))}
    request_url = 'https://api.mailgun.net/v3/{url}/messages'.format(url=url)
    response = requests.post(request_url, auth=('api', key), files=files, data={
        'from': sender,
        'to': recipient,
        'subject': subject,
        'text': message
    })
    if response.status_code != 200:
        print("error sending email: #{subject}".format(subject=subject))
        print("Email body")
        print(message)
        if attachment:
            print("Attachment: #{a}".format(a=attachment))
    return
