import ssl
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.conf import settings


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
        html_content = f"""
            <html lang="es">
            <head>
                <meta charset="UTF-8" />
                <meta http-equiv="X-UA-Compatible" content="IE=edge" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <title>Notification</title>
                <style>
                .styled-table {{
                    border-collapse: collapse;
                    margin: 25px 0;
                    font-size: 0.9em;
                    font-family: sans-serif;
                    min-width: 400px;
                    box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
                }}

                .styled-table thead tr {{
                    background-color: #009879;
                    color: #ffffff;
                    text-align: left;
                }}

                .styled-table th,
                .styled-table td {{
                    padding: 12px 15px;
                }}

                .styled-table tbody tr {{
                    border-bottom: 1px solid #dddddd;
                }}

                .styled-table tbody tr:nth-of-type(even) {{
                    background-color: #f3f3f3;
                }}

                .styled-table tbody tr:last-of-type {{
                    border-bottom: 2px solid #009879;
                }}
                </style>
            </head>
            <body>
                <h2>{salutation}</h2>
                <h3>{description}</h3>
                {self.create_html_table(data)}
            </body>
            </html>
        """
        return html_content

    def config_email(self):
        """
        """
        self.email_sender = settings.email_sender
        self.email_password = settings.email_password

    def get_email_template(self, name: str, data_table: list) -> dict:
        """
        """
        subject: str = "Productos analizados"
        saludo: str = f"Buen día {name}: "
        description: str = f"Se encontraron {len(data_table)} productos por debajo del precio limite."
        body = self.create_html_content(data_table, saludo, description)

        return {
            "subject": subject,
            "body": body
        }

    def send_email(self, email_receiver: str, name_receiver: str, data: list):
        """
        """
        print(f"Preparando el envio de la notificación.")
        self.config_email()
        get_template = self.get_email_template(name_receiver, data)

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

                print("La notificación fue enviada correctamente.")
        except Exception as error:
            print(f"ERROR NOTIFICATION: {error}")


notification = Notification()
