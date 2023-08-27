import ssl
import smtplib
import logging
from pathlib import Path
from string import Template
from config.conf import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Notification():
    def __init__(self):
        self.email_sender: str = ""
        self.email_password: str = ""

    def create_html_table(self, data):
        table_html = "<table class='styled-table'>\n"
        table_html += "<thead>\n"

        # Generar los encabezados de la tabla dinámicamente
        headers = data[0].keys() if data else []
        table_html += "<tr>\n"
        for header in headers:
            table_html += f"<th>{header}</th>\n"
        table_html += "</tr>\n"

        table_html += "</thead>\n"
        table_html += "<tbody>\n"

        # Generar los datos de la tabla dinámicamente
        for item in data:
            table_html += "<tr>\n"
            for value in item.values():
                table_html += f"<td>{value}</td>\n"
            table_html += "</tr>\n"

        table_html += "</tbody>\n"
        table_html += "</table>"

        return table_html

    def create_html_content(self, data, salutation, description):
        html_content = Template(
            Path("app/templates/simple_table.html").read_text())

        html_sustitute = {
            "salutation": salutation,
            "description": description,
            "simple_table": self.create_html_table(data)
        }

        return html_content.substitute(html_sustitute)

    def config_email(self):
        """
        """
        self.email_sender = settings.email_sender
        self.email_password = settings.email_password

    def get_email_template(self, name: str, data_subject: str, data_description: str, data_table: list) -> dict:
        """
        """
        saludo: str = f"Buen día {name}: "
        body = self.create_html_content(data_table, saludo, data_description)

        return {
            "subject": data_subject,
            "body": body
        }

    def send_email(self, email_receiver: str, name_receiver: str, description: str, subject: str, data: list) -> bool:
        """
        """
        logging.info(f"Preparando el envio de la notificación.")
        self.config_email()
        get_template = self.get_email_template(
            name_receiver, subject, description, data)

        em = MIMEMultipart('alternative')
        em["From"] = self.email_sender
        em["To"] = email_receiver
        em["Subject"] = get_template.get('subject')
        em.attach(MIMEText(get_template.get('body'), 'html'))

        context = ssl.create_default_context()

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                smtp.login(self.email_sender, self.email_password)
                smtp.sendmail(self.email_sender,
                              email_receiver, em.as_string())

                logging.info("La notificación fue enviada correctamente.")
                return True
        except Exception as error:
            logging.error(f"ERROR NOTIFICATION: {error}")
            return False


notification = Notification()
