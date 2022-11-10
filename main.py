import json
import math
import urllib.request


def to_str(data: dict) -> str:
    ret = f"\t{data['class']}\t{data['grade']}\t{data['liankao']}"
    return ret


def cal_rank(number: dict, rank: dict) -> str:
    biao = {
        'A1': (0, 1),
        'A2': (1, 3),
        'A3': (3, 6),
        'A4': (6, 10),
        'A5': (10, 15),
        'B1': (15, 21),
        'B2': (21, 28),
        'B3': (28, 36),
        'B4': (36, 43),
        'B5': (43, 50),
        'C1': (50, 56),
        'C2': (56, 64),
        'C3': (64, 71),
        'C4': (71, 78),
        'C5': (78, 84),
        'D1': (84, 89),
        'D2': (89, 93),
        'D3': (93, 96),
        'D4': (96, 98),
        'D5': (98, 99),
        'E': (99, 100)
    }
    ret = ''
    for i in ('class', 'grade', 'liankao'):
        tot = int(number[i])
        mine = biao[rank[i]]
        high = math.ceil(tot*mine[0]/100)+1
        low = math.floor(tot*mine[1]/100)+1
        ret += f'\t{high}~{low}' if high != low else f'\t{high}'
    return ret


def parse_subject(data: dict) -> list:
    ret = []
    ret.append('   等级'+to_str(data['rankPart']))
    ret.append('   排名'+cal_rank(data['number'], data['rankPart']))
    ret.append('   人数'+to_str(data['number']))
    ret.append('   平均'+to_str(data['avg']))
    ret.append('   最高'+to_str(data['highest']))
    return ret


if __name__ == '__main__':
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69', 'cookie': 'hfs-session-id = '+input('请输入 hfs-session-id: ')}
    baseurl = 'https://hfs-be.yunxiao.com/v3/exam/1667208'
    scoreurl = 'https://hfs-be.yunxiao.com/v3/exam/1667208/overview'
    subjects = {3: '语文', 4: '数学', 5: '英语', 6: '物理', 7: '历史', 8: '政治'}

    req = urllib.request.Request(scoreurl, headers=headers)
    data = urllib.request.urlopen(req).read()
    scoredata = json.loads(data)['data']
    score = {}
    for i in scoredata["papers"]:
        score[int(i['paperId'][6])] = i['score']

    for i, j in subjects.items():
        #req = urllib.request.Request(
        #    f'{baseurl}/papers/652942{i}-86397/rank-info', headers=headers)
        req = urllib.request.Request(
            f'{baseurl}/papers/652942{i}-88062/rank-info', headers=headers)
        data = urllib.request.urlopen(req).read()
        data = json.loads(data)['data']
        print(f'\n{j}\t班级\t年段\t联考')
        for k in parse_subject(data):
            print(k)
        print(f'   成绩\t{score[i]}')

    req = urllib.request.Request(baseurl+'/rank-info', headers=headers)
    data = urllib.request.urlopen(req).read()
    data = json.loads(data)['data']
    print(f'\n总分\t班级\t年段\t联考')
    for k in parse_subject(data):
        print(k)
    print(f'   成绩\t{scoredata["score"]}')
    input()
