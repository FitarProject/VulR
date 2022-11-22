def header_convert(request_data_read):
    header_data = []
    headers = {}
    for header_tmp in request_data_read:  # 删除行尾的换行符
        header_data.append(header_tmp.rstrip('\n'))
    for header in header_data:
        if header.find(': ') != -1:
            key_to_value = header.split(': ', maxsplit=1)
            headers[key_to_value[0]] = key_to_value[1]
        elif header.find(':') != -1:
            key_to_value = header.split(': ', maxsplit=1)
            headers[key_to_value[0]] = key_to_value[1]
        elif header.strip() == '':
            break
    # print(headers)
    return headers
    # 二次判断是否包含请求体
    # for index,value in enumerate(header_data[1:]):
    #     if value.find(':', 1, 30) == -1:        #因为几乎所有header头部字段长度都不超过30，所以判断前30个字符中是否包含'：'
    #         flag = index + 1
    #         break
    # 匹配数据类型
    # match = re.findall(r'^(.*?)x-www-form-urlencoded(.*?)', headers['Content-Type'])
    # match2 = re.findall(r'^(.*?)json(.*?)', headers['Content-Type'])
    # match3 = re.findall(r'^(.*?)multipart/form-data(.*?)', headers['Content-Type'])
