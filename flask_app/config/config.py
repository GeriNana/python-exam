from flask_mail import Mail

def init_mail(app):
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'gastroglide.albania@gmail.com'
    app.config['MAIL_PASSWORD'] = 'blummen2024'
    mail = Mail(app)
    return mail
