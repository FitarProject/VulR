import json


def deal_data_form(data_list=[]):                                   # x-www-form-urlencoded
    data = {}                                                       # 将 key1=value1&key2=value2 转换为字典
    for data_tmp in data_list:
        if data_tmp.strip() != '':                                  # 判断是否为有效行
            data_data = data_tmp.split('&')                         # 分隔出form表单的值
            for data_form in data_data:                             # 将所有有效值导入字典
                if data_form.strip() != '':
                    data[data_form.split('=')[0]] = data_form.split('=')[1]
    return data


def deal_data_json(data_list: list):                                   # 返回json格式字符串
    return json.dumps(deal_data_form(data_list))


def list_to_str(data_list: list):
    data_str = ''
    for data_tmp in data_list:
        if data_tmp.strip() != '':
            data_str += data_tmp
    return data_str


def deal_content_type(content_type, data: list):                                # 判断content-type并处理，涵盖大部分类型的处理方式
    data_deal = None
    body_type = None
    if 'application' in content_type:                               # application
        body_type = 'application'
        if 'x-www-form-urlencoded' in content_type:                     # 非上传
            data_deal = list_to_str(data)
            return body_type, data_deal
        elif 'json' in content_type:                                    # 非上传
            data_deal = deal_data_json(data)
            return body_type, data_deal
        elif 'xml' in content_type:                                     # 非上传
            data_str = list_to_str(data)
            if 'xml' in data_str:
                data_deal = data_str.encode("utf-8")
            else:
                return body_type, data_deal
        elif 'octet-stream' in content_type:                            # 待确认
            data_deal = list_to_str(data).encode("utf-8")
            return body_type, data_deal
        else:                                                           # 待确认
            data_deal = list_to_str(data).encode("utf-8")
            return body_type, data_deal
    elif 'text' in content_type:                                    # text
        body_type = 'text'
        if 'plain' in content_type:                                     # 非上传
            data_deal = list_to_str(data)
            return body_type, data_deal
        elif 'html' in content_type:                                    # 非上传
            data_deal = list_to_str(data)
            return body_type, data_deal
        elif 'xml' in content_type:                                     # 非上传
            data_str = list_to_str(data)
            if 'xml' in data_str:
                data_deal = data_str.encode("utf-8")
            else:
                return body_type, data_deal
        elif 'javascript' in content_type:                              # 非上传
            data_deal = list_to_str(data)
            return body_type, data_deal
        else:                                                           # 非上传
            data_deal = list_to_str(data)
            return body_type, data_deal
    elif 'image' in content_type:                                   # image
        body_type = 'image'
        if 'gif' in content_type:                                       # 上传
            pass
        elif 'png' in content_type:                                     # 上传
            pass
        elif 'jpeg' in content_type:                                    # 上传
            pass
        elif 'icon' in content_type:                                    # 上传
            pass
        else:                                                           # 上传
            pass
    elif 'audio' in content_type or 'video' in content_type:        # audio or video
        body_type = 'video'
        pass
    elif content_type == 'multipart/form-data':                     # 表单提交
        body_type = 'form-data'
        pass
    elif 'application' not in content_type or 'text' not in content_type or 'image' not in content_type or 'multipart' not in content_type:
        body_type = 'None'
        print('content_type错误！')
        return body_type, data_deal
    else:                                                           # 使用requests_toolbelt自动识别
        body_type = 'requests_toolbelt'
        # 使用requests_toolbelt
        return body_type, data_deal
    return body_type, data_deal


def body_convert(request_data_read: list, content_type: str):
    if not content_type:
        content_type = 'application/x-www-form-urlencoded'
    body_type, data = deal_content_type(content_type, request_data_read)
    if data:
        pass
    pass
