import requests
import datetime as dt

url_translator = "https://microsoft-translator-text.p.rapidapi.com/translate"


class Record:
    records = []
    info_records = []

    def add_record(self, record):
        self.records.append(record)

    def add_info_record(self, record):
        self.info_records.append(record)


class Base(Record):
    def __init__(self, url):
        self.url = url

    def get_info(self, response):
        try:
            response = [response.headers, response.url, response.elapsed, response.encoding]
            self.info_records.append(response)
        except AttributeError:
            lang, response = response
            response = [response.headers, response.url, response.elapsed, response.encoding]
            return response


class GetTranslate(Base):

    def post(self, lang, text):
        print(lang)
        querystring = {"to": f"{lang.strip()}", "api-version": "3.0", "profanityAction": "NoAction",
                       "textType": "plain"}
        payload = ("[{\"Text\":\"" + text + "\"}]").encode('utf-8')
        headers = {
            'content-type': "application/json",
            'x-rapidapi-key': "4d559d2b2emsh1a8eef160e6bf8ep11ce26jsne29bc7830287",
            'x-rapidapi-host': "microsoft-translator-text.p.rapidapi.com"
        }
        response = requests.post(url=self.url, data=payload, headers=headers, params=querystring)
        self.get_info(response)
        return response, text, lang

    def get_translate(self, post):
        resp, text, lang = post
        now = dt.datetime.now().strftime('%c')
        text_translate = resp.json()[0]['translations'][0]['text']
        try:
            translate_result = (f"Ваш текст: {text}\nПеревод: {text_translate}\n"
                                f"Язык: {lang}\nВремя: {now}", resp)
        except KeyError:
            print(f"Ключ '{lang}' языка не найден")
            return exit(1)
        self.add_record(translate_result[0].split('\n'))
        return translate_result

    def get_all_time(self):
        time_row = []
        for row in self.info_records:
            row = round(row[2].total_seconds(), 3)
            time_row.append(row)
        return time_row

    def get_sum_time(self):
        seconds = 0
        for time in self.get_all_time():
            seconds += time
        seconds = round(seconds, 2)
        return f"Запросы заняли {seconds} секунд"


"""translate = GetTranslate(url=url_translator)
result = translate.get_translate(translate.post('ar', 'привет'))
result2 = translate.get_translate(translate.post('ja', 'привет'))
print(translate.get_info(result2))
res = translate.get_all_time()
print('\n'.join(Record.records[2]))
print(res)
print(translate.get_sum_time())"""
