MAX_NAME_LENGTH = 100
MIN_NAME_LENGTH = 5
MIN_DESCRIPTION_LENGTH = 10
DATABASE_URL = 'sqlite+aiosqlite:///./cat_charity.db'
APP_TITLE = 'Cat Charity'
MIN_PASSWORD_LENGTH = 3

GOOGLE_API_AUTH_URL = 'https://www.googleapis.com/auth/'
SPREADSHEET_BODY = {
    'properties': {
        'title': 'Отчёт от ',
        'locale': 'ru_RU'
    },
    'sheets': [
        {
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'Лист1',
                'gridProperties': {
                    'rowCount': 100,
                    'columnCount': 11
                }
            }
        }
    ]
}
