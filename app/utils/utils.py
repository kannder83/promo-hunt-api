import random
import datetime


class Utils():
    def get_time_now(self):
        return datetime.datetime.now()

    def format_datetime(self, format_date):
        return format_date.strftime("%Y-%m-%d %H:%M:%S")

    def authority(self, portal: str):
        return {
            "amazon": "www.amazon.com",
            "mercadolibre": "listado.mercadolibre.com.co"
        }.get(portal)

    def referer(self, portal: str):
        return {
            "amazon": "https://www.amazon.com/ref=nav_logo",
            "mercadolibre": "https://listado.mercadolibre.com.co/"
        }.get(portal)

    def random_platform(self):
        """
        """
        platform: list = [
            '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
            '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
        ]
        return random.choice(platform)

    def random_agent(self) -> str:
        """
        """
        user_agents: list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.126 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.54'
        ]
        return random.choice(user_agents)

    def headers(self, portal: str):
        """
        """
        headers: dict = {}

        headers['amazon'] = {
            'authority': 'www.amazon.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'Origin': 'https://www.amazon.com',
            'referer': 'https://www.amazon.com/',
            'device-memory': '8',
            'downlink': '10',
            'dpr': '1',
            'ect': '4g',
            'rtt': '50',
            'sec-ch-device-memory': '8',
            'sec-ch-dpr': '1',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'macOS',
            'sec-ch-viewport-width': '1024',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-site',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'viewport-width': '1024',
        }

        headers['mercadolibre']: dict = {
            'authority': 'listado.mercadolibre.com.co',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'device-memory': '8',
            'downlink': '10',
            'dpr': '1',
            'ect': '4g',
            'referer': 'https://www.mercadolibre.com.co/',
            'rtt': '0',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-site',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'viewport-width': '1469',
        }

        # logging.info(f"Headers: {headers[portal]}")

        return headers[portal]


web_utils = Utils()
