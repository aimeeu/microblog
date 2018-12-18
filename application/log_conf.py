import os
import logging
from logging.handlers import SMTPHandler, TimedRotatingFileHandler


def configure_logging(app):
    configure_mail_logging(app)
    configure_file_logging(app)


def configure_mail_logging(app):
    if app.config['MAIL_SERVER']:
        auth = None
    if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
    if app.config['MAIL_USE_TLS']:
        secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


def configure_file_logging(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = TimedRotatingFileHandler('logs/microblog.log',
                                            when='midnight', utc=True,
                                            backupCount=30)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')
