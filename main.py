import gspread

CODE = '1F0Mo_CrKpUj4qqq8vGEDTLhfOClg8v-W082kFJqH4wQ'
gc = gspread.service_account(filename = 'keys.json')
sh = gc.open_by_key(CODE)