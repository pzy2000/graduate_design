# coding=utf-8
from flask import Flask, render_template, request, jsonify
from datetime import timedelta
import execute
import time
import threading
import jieba

"""
定义心跳检测函数
"""


def heartbeat():
    print(time.strftime('%Y-%m-%d %H:%M:%S - heartbeat', time.localtime(time.time())))
    timer = threading.Timer(60, heartbeat)
    timer.start()


timer = threading.Timer(60, heartbeat)
timer.start()

"""
ElementTree在 Python 标准库中有两种实现。
一种是纯 Python 实现例如 xml.etree.ElementTree ，
另外一种是速度快一点的 xml.etree.cElementTree 。
 尽量使用 C 语言实现的那种，因为它速度更快，而且消耗的内存更少
"""

app = Flask(__name__, static_url_path="/static")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


@app.route('/message', methods=['POST'])
# """定义应答函数，用于获取输入信息并返回相应的答案"""
def reply():
    # 从请求中获取参数信息
    req_msg = request.form['msg']
    print(req_msg)
    # 将语句使用结巴分词进行分词
    if req_msg.find('法轮') != -1:
        res_msg = '请不要使用敏感词汇哦！'
        return jsonify({'text': res_msg})
    if req_msg.find('课程表') != -1 or req_msg.find('课表') != -1:
        res_msg = '<a href="http://r.photo.store.qq.com/psc?/V53fS6EP2JS1L602cJzy30' \
                  '5tn71MJMcn/ruAMsa53pVQWN7FLK88i5qmOUz6ajcd7miwsTsh740rDUcr9GtUiJ' \
                  'ceiT3dlJCUp7e2XfnzPYZokKB61LGih9MIpd6BNECuEZI0qJp54q90!/r"  target="opentype">点击查看课程表</a>'
        return jsonify({'text': res_msg})
    if req_msg.find('成绩') != -1:
        res_msg = '目前正在开发中...点击http://jwxs.hhu.edu.cn/login进入系统'
        return jsonify({'text': res_msg})
    if req_msg.find('泰勒') != -1:
        res_msg = '在数学中，泰勒公式是一个用函数在某点的信息描述其附近取值的公式。如果函数足够光滑的话，在已知函数在某一点的各阶导数值的情况之下，' \
                  '泰勒公式可以用这些导数值做系数构建一个多项式来近似函数在这一点的邻域中的值。泰勒公式还给出了这个多项式和实际的函数值之间的偏差。' \
                  '泰勒公式得名于英国数学家布鲁克·泰勒。他在1712年的一封信里首次叙述了这个公式，尽管1671年詹姆斯·格雷高里已经发现了它的特例。 '
        return jsonify({'text': res_msg})
    if req_msg.find('微积分') != -1:
        res_msg = '微积分（Calculus），数学概念，是高等数学中研究函数的微分(Differentiation)、积分(' \
                  'Integration' \
                  ')以及有关概念和应用的数学分支。它是数学的一个基础学科，内容主要包括极限、微分学、积分学及其应用。微分学包括求导数的运算，' \
                  '是一套关于变化率的理论。它使得函数、速度、加速度和曲线的斜率等均可用一套通用的符号进行讨论。积分学，包括求积分的运算，为定义和计算面积、体积等提供一套通用的方法 '
        return jsonify({'text': res_msg})
    if req_msg.find('地图') != -1 or req_msg.find('迷路') != -1:
        res_msg = '点我打开地图'
        res_msg = '<a href="https://map.baidu.com/search/%E6%B2%B3%E6%B5%B7' \
                  '%E5%A4%A7%E5%AD%A6%E5%B8%B8%E5%B7%9E%E6%A0%A1%E5%8C%BA/@13356852.9347' \
                  '983,3717584.54,17.94z?querytype=s&da_src=shareurl&wd=%E' \
                  '6%B2%B3%E6%B5%B7%E5%A4%A7%E5%AD%A6%E5%B8%B8%E5%B7%9E%E6%A0%A1%E5%8C%BA&c' \
                  '=348&src=0&pn=0&sug=0&l=13&b=(13337139,3707631;13383219,3733519)&from=webmap&biz_forward=%7' \
                  'B%22scaler%22:2,%22styles%22:%22pl%22%7D&device_ratio=2"  target="opentype">' + res_msg + '</a>'
        return jsonify({'text': res_msg})
    req_msg = " ".join(jieba.cut(req_msg))
    print(req_msg)
    # 调用decode_line对生成回答信息

    res_msg = execute.predict(req_msg)
    # 将unk值的词用微笑符号袋贴
    res_msg = res_msg.replace('_UNK', '^_^')
    res_msg = res_msg.strip()

    # 如果接受到的内容为空，则给出相应的回复
    if res_msg == ' ':
        res_msg = '请与我聊聊天吧'
    if res_msg == '':
        res_msg = '呜呜呜，这个我不会，主人'
    '''
    去除预测语句中的空格
    '''
    res_msg = res_msg.replace(' ', '')
    return jsonify({'text': res_msg})


"""
jsonify:是用于处理序列化json数据的函数，就是将数据组装成json格式返回

http://flask.pocoo.org/docs/0.12/api/#module-flask.json
"""


@app.route("/")
def index():
    return render_template("index.html")


'''
'''
# 启动APP
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8808)  # 确保公网可访问
