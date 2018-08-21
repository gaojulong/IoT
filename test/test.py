
import json
import datetime

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        # elif isinstance(obj, date):
        #     return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)



str='G20-放假-安排'
result = str.split('-')[1:]
print(result)
print(str.split('-')[:1])

print(str.split('-')[:2])

print(str.split('-')[:])