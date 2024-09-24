import re

text = """
**屋主自租**
金雅重劃區~~金雅八街
~~採光好~~棟距佳~~
~~警衛管理~~代收包裹~~
~~垃圾集中處理~~家俱可談~~
~~全室大金冷暖變頻空調~~
租金：30000
押金：2個月
格局：3/2/2
水電：台水台電帳單計費
管理費：租客負擔
寵物：可貓
車位：1平面汽車+1機車
"""

maximum = 9500
lines = text.split('\n')
for line in lines:
    cleaned_line = line.replace(',', '')
    match = re.search(r'(\d+).*/月', cleaned_line)
    if match:
        number = match.group(1)
        num_value = int(number[:])
        if num_value > maximum:
            continue

    if '租金' in line or '月租' in line:
        match = re.search(r'(\d+)(\D?)', cleaned_line)
        if match:
            start_index = match.start(1)
            end_index = match.start(2)
            number = cleaned_line[start_index:end_index]
            print(number)
            num_value = int(number)
            if num_value > maximum:
                continue