import re

pattern = re.compile(r'(такси|taxi|didi|(яндекс|yandex)\.go|(яндекс|yandex)\.лавк|gett|(uber(?!2)))')

result = pattern.findall('ехали такси на , а оказалось ')
print(result)
print(result==[])