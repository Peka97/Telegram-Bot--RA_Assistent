import datetime
import httplib2
import re
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from handlers.basic import tz_MOSCOW, check_date

CREDENTIALS_FILE = 'data/credentials.json'
spreadsheet_id = '16bqjSnz6IWeGpG1OSyFHuG2iSb-fspuOqnhgnQ9YN9k'

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)


def sheets_read(lst: str, start: str, finish: str, demension: str) -> dict:
    """Читает данные с таблицы, обращаясь к service. Принимает стартовую и конечную точку в таблице и
    параметр отображения (строки или столбцы)"""

    values_for_read = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f'{lst}!{start}:{finish}',
        majorDimension=demension,
    ).execute()
    return values_for_read['values']


def sheets_write(lst: str, start: str, finish: str, demension: str, content: list) -> None:
    """Записывает данные в таблицу, обращаясь к service. Принимает стартовую и конечную точку в таблице,
        параметр отображения (строки или столбцы) и контент. Последний может быть представлен в виде вложенных списков
        для заполнения нескольких ячеек"""

    values_for_write = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            'valueInputOption': 'USER_ENTERED',
            'data': [
                {'range': f'{lst}!{start}:{finish}',
                 'majorDimension': demension,
                 'values': [[content], [content]]}
            ]
        }
    ).execute()


def formatted_data(schedule: str, count=0) -> list:
    values = sheets_read(check_date, 'A1', 'AI6', 'COLUMNS')
    idx_of_name = values[2].index(schedule)
    date = datetime.date.strftime(datetime.datetime.now(tz_MOSCOW), '%d.%m.%Y')
    reply = []
    pattern = re.compile('[а-я]{2}')
    for idx, el in enumerate(values):
        try:
            if el[1] >= date and len(reply) < 8 and re.match(pattern, el[0]):
                if el[idx_of_name] == '11':
                    reply.append(f'{el[0]} {el[1]} 09:00 - 21:00')
                elif el[idx_of_name] == '3':
                    reply.append(f'{el[0]} {el[1]} 21:00 - 09:00')
                elif el[idx_of_name] == '8':
                    reply.append(f'{el[0]} {el[1]} отсыпной')
                elif el[idx_of_name] == '':
                    reply.append(f'{el[0]} {el[1]} выходной')
        except IndexError:
            reply.append(f'{el[0]} {el[1]} выходной')
    return reply


def formatted_for_all() -> list:
    values = sheets_read(check_date, 'A1', 'AI6', 'COLUMNS')
    agents = {}
    date = datetime.date.strftime(datetime.datetime.now(tz_MOSCOW), '%d.%m.%Y')
    reply = []
    for i in range(2, 6):
        agents[i - 2] = values[0][i]

    for idx, el in enumerate(values):
        if idx < 3:
            continue
        if el[1] >= date and len(reply) < 7:
            time: list = el[0:2]
            hours: list = el[2:]
            if '11' in hours and '3' in hours:
                morning = hours.index("11")
                night = hours.index("3")
                reply.append(f'{time[0]} {time[1]} | {agents[morning]} -> {agents[night]}')
            else:
                reply.append(f'{time[0]} {time[1]} | FormatError')
    return reply


def schedule_for_transfer_of_shifts() -> dict:
    values = sheets_read(check_date, 'A1', 'AI6', 'COLUMNS')
    date_now = datetime.date.strftime(datetime.datetime.now(tz_MOSCOW), '%d.%m.%Y')
    date_tomorrow = datetime.date.strftime(datetime.datetime.now(tz_MOSCOW) + datetime.timedelta(days=1), '%d.%m.%Y')
    agents = {}
    result = {}
    for i in range(2, 6):
        name = values[0][i]
        schedule_number = values[2][2:][i - 2]
        agents[i - 2] = [name, schedule_number]
    for idx, el in enumerate(values):
        if idx < 2:
            continue
        elif el[1] == date_now:
            hours: list = el[2:]
            night = hours.index("3")
            result["09:00"] = [agents[night][1]]
        elif el[1] == date_tomorrow:
            hours: list = el[2:]
            morning = hours.index("11")
            night = hours.index("3")
            result["09:00"].append(agents[morning][1])
            result["21:00"] = [agents[morning][1], agents[night][1]]
            break
    return result


def formatted_for_meets(date: datetime) -> list:
    """Функция, определяющая имена дежурных специалистов и номера их расписания для дальнейшей передачи в функцию
    автоматической организации встреч"""

    values = sheets_read(check_date, 'A1', 'AI6', 'COLUMNS')
    agents = {}
    date = datetime.date.strftime(datetime.datetime.now(tz_MOSCOW), '%d.%m.%Y')
    reply = []
    for i in range(2, 6):
        agents[i - 2] = values[0][i], values[2][i]
    for idx, el in enumerate(values):
        if idx < 3:
            continue
        if len(reply) < 3 and el[1] >= date:
            hours: list = el[2:]
            morning = hours.index("11")
            night = hours.index("3")
            reply.extend([agents[morning], agents[night]])
    print(reply)
    return reply
