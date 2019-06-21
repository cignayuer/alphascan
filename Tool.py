import chardet
import pandas as pd
import os, shutil
import platform

"""
通用工具类
"""


def html_tag(tag_name, content=None, inner=None):
    if inner is None:
        t_tag = str('<' + tag_name + ' >')
    else:
        t_tag = str('<' + tag_name + ' ' + inner + '>')
    if content is None:
        t_tag += str('</' + tag_name + '>')
    else:
        if type(content) is list:
            my_content = str()
            for key in content:
                my_content += key + '\n'
            t_tag += str(my_content + '</' + tag_name + '>')
        else:
            content = '' if str(content) == '0' or str(content) == '0%' else str(content)
            t_tag += str(str(content) + '</' + tag_name + '>')
    return t_tag


def html_inner(tag_dict):
    ret = str(' ')
    for (k, v) in tag_dict.items():
        # ret += str(k + '=' + '"' + v + '" ')
        ret += str('%s="%s" ' % (k, v))
    return ret


def build_path(root_path, path):
    """
    构建绝对路径
    :param root_path:
    :param path:
    :return:
    """
    if path.startswith('/') or path.startswith('\\'):
        return path
    path = str(path).replace('\\', '/')
    root_path = str(root_path).replace('\\', '/')
    if root_path.endswith('/'):
        root_path = root_path[:-1]
    list_path = root_path.split('/')
    while path.startswith('./'):
        path = path.replace('./', '')
    while path.startswith('../'):
        path = path.replace('../', '')
        list_path.pop()
    ret_path = str()
    for item in list_path:
        ret_path += item
        ret_path += '/'
    ret_path += path
    if str_compare(discern_system(), 'Windows'):
        ret_path = ret_path.replace('/', '\\')
    elif str_compare(discern_system(), 'Linux'):
        ret_path = ret_path.replace('\\', '/')
    return ret_path


def discern_system():
    if platform.system() == 'Windows':
        return 'Windows'
    elif platform.system() == 'Linux':
        return 'Linux'
    else:
        return 'Other'


def str_compare(str_one, str_two, ignore_empty=True, ignore_case=True):
    """
    比较两个字符串是否相同
    :param str_one:
    :param str_two:
    :param ignore_empty:
    :param ignore_case:
    :return:
    """
    if type(str_one) is not str or type(str_two) is not str:
        return False
    if ignore_empty:
        str_one = str_one.replace(' ', '')
        str_two = str_two.replace(' ', '')
    if ignore_case:
        str_one = str_one.lower()
        str_two = str_two.lower()
    return True if str_one == str_two else False


def write_html(template_html, result_html, content_str, mark_line='mark-mark-mark'):
    """
    合并两个html文件
    :param template_html: 模板html文件
    :param content_str: 内容html
    :param result_html: 生成新的html文件
    :param mark_line: 合并标记位置
    :return:
    """
    result = []
    with open(template_html, mode='r', encoding=get_encoding(template_html)) as template_file:
        for line in template_file.readlines():
            result.append(line)
            if mark_line in str(line):
                print('找到了找到了')
                result.append(content_str)
    with open(result_html, mode='w', encoding='utf-8') as result_file:
        result_file.writelines(result)


def edit_html(template_html, source_html, result_html, mark_line='mark-mark-mark', form_title=None):
    """
    合并两个html文件
    :param form_title:
    :param template_html: 模板html文件
    :param source_html: 内容html文件
    :param result_html: 生成新的html文件
    :param mark_line: 合并标记位置
    :return:
    """
    result = []
    with open(template_html, mode='r', encoding=get_encoding(template_html)) as template_file:
        for line in template_file.readlines():
            result.append(line)
            if mark_line in str(line):
                print('找到了找到了')
                if form_title is not None and type(form_title) is str:
                    result.append(form_title)
                with open(source_html, mode='r', encoding=get_encoding(source_html)) as source_html:
                    result.extend(source_html.readlines())
    with open(result_html, mode='w', encoding='utf-8') as result_file:
        result_file.writelines(result)


def attach_html_form_title(msg):
    """
    在html body中添加标题
    :param msg: 标题内容
    :return: 返回添加了标题标签的字符串
    """
    return str('<h1 class="title">' + str(msg) + '</h1>')


def attach_html_span(msg, class_name=None):
    """
    给内容添加html span标签
    :param msg: 内容
    :param class_name: 标签类名
    :return: 返回添加完成后的msg
    """
    if type(msg) is not str:
        raise Exception('msg类型错误，应为字符串。')
    if class_name is None or type(class_name) is not str:
        return str('<span>' + str(msg) + '</span>')
    else:
        return str('<span class="' + str(class_name) + '">' + str(msg) + '</span>')


def list_safe_sum(data_list):
    """
    将list中的数字或能转化成数字的数据相加
    :param data_list:
    :return:
    """
    result = 0
    for i in data_list:
        try:
            result += int(i)
        except Exception:
            pass
    return int(result)


def delete_file(file):
    """
    删除文件
    :param file:
    :return:
    """
    if os.path.exists(file):
        os.remove(file)


def file_backup(file, destination_file=None):
    """
    文件备份
    :param file: 要备份的原文件
    :param destination_file: 备份的目标文件
    :return: 返回备份文件
    """
    if destination_file is None:
        destination_file = file + '-bak'
    shutil.copyfile(file, destination_file)
    return destination_file


def check_contain_chinese(check_str):
    """
    核验是否是中文字符串
    :param check_str: 要检查的字符串
    :return:
    """
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
        else:
            return False


def str_contain(str_a, str_b):
    """
    字符串是否存在包含关系，if a is in b
    :param str_a:
    :param str_b:
    :return:
    """
    if str_a.strip() in str_b.strip():
        return True
    return False


# 获取文件编码格式
def get_encoding(file):
    with open(file, 'rb') as f:
        return chardet.detect(f.read())['encoding']


def list_to_df(dfc, my_list):
    """
    把list对象按照dfc格式生成dateFrame
    :param dfc: dateFrame格式模板
    :param my_list: 数据对象
    :return: 生成的新的dateFrame对象
    """
    my_dic = dict()
    t = 0
    for i in dfc.columns.values.tolist():
        my_dic[i] = [my_list[t]]
        t += 1
    return pd.DataFrame(my_dic)


# 重置索引序列
def reset_index(df):
    """
    使dateFrame数据索引变得有序
    :param df: dateFrame对象
    :return:
    """
    dfc = df.reset_index()
    dfc.drop('index', axis=1, inplace=True)
    return dfc


# 按照格式添加一行
def add_line(dfc, index, my_list):
    """
    添加一行数据到dateFrame中
    :param dfc: 要操作的dateFrame对象
    :param index: 把@my_list添加到@dfc中的位置
    :param my_list: 要添加的数据，list类型
    :return:
    """
    # dfc = pd.DataFrame({'A': ['aaa', 'bbb', 'ccc'], 'B': [1, 2, 3]})
    # dfc.loc[2] = ['mmm', 5]
    new_df = list_to_df(dfc, my_list)
    if dfc.shape[0] < 1:
        '''纯粹新添加行'''
        dfc = new_df.append(dfc)
        dfc = reset_index(dfc)
    elif index == 0:
        '''首行添加'''
        dfc = new_df.append(dfc)
        dfc = reset_index(dfc)
    elif index >= dfc.shape[0]:
        '''末尾添加'''
        dfc = dfc.append(new_df)
        dfc = reset_index(dfc)
    else:
        one_df = dfc[:index]
        two_df = dfc[index:]
        dfc = one_df.append(new_df)
        dfc = dfc.append(two_df)
        dfc = reset_index(dfc)
    return dfc


def safe_sum(data_list):
    """
    将list中的数字相加
    :param data_list:
    :return:
    """
    result = 0
    for i in data_list:
        try:
            result += int(i)
        except Exception:
            pass
    return int(result)


def to_per(data_integer):
    """
    把整数或者小数，改成百分数
    :param data_integer:
    :return: 百分数字符串
    """
    return "%.1f%%" % (data_integer * 100)


def to_per_(data_integer, bbb):
    try:
        bbb = int(bbb)
    except Exception as e:
        return "0%"
    if bbb <= 0:
        return "0%"
    value = data_integer / bbb
    """
    把整数或者小数，改成百分数
    :param data_integer:
    :return: 百分数字符串
    """
    return "%.1f%%" % (value * 100)
