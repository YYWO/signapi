'''
JD's signature Writen and Open Source By DDO
京东签名算法 - 由 DDO 开源

Please don't upload this script to any public repository or sharing on the Internet. Otherwise, you may be exposed to legal risk！
请不要将此脚本上传至任何公共仓库或共享在互联网上。否则，您可能会面临法律风险！

匿名作者在此基础之上适配开箱即用的API服务框架，与Nolan公益接口使用方法完全相同。
脚本仅供学习交流使用，不得用于商业用途，否则后果自负，请不要为自己的无知买单！
'''

from flask import Flask, request, abort
import base64, hashlib, time, random, urllib.parse, uuid, json

sign_client = 'android'
sign_clientVersion = '11.1.4'

string1 = "KLMNOPQRSTABCDEFGHIJUVWXYZabcdopqrstuvwxefghijklmnyz0123456789+/"
string2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
def randomstr(num):
    randomstr = ''.join(str(uuid.uuid4()).split('-'))[num:]
    return randomstr
def randomstr1(num):
    randomstr = ""
    for i in range(num):
        randomstr = randomstr + random.choice("abcdefghijklmnopqrstuvwxyz0123456789")
    return randomstr
def sign_core(inarg):
    key = b'80306f4370b39fd5630ad0529f77adb6'
    mask = [0x37, 0x92, 0x44, 0x68, 0xA5, 0x3D, 0xCC, 0x7F, 0xBB, 0xF, 0xD9, 0x88, 0xEE, 0x9A, 0xE9, 0x5A]
    array = [0 for _ in range(len(inarg))]
    for i in range(len(inarg)):
        r0 = int(inarg[i])
        r2 = mask[i & 0xf]
        r4 = int(key[i & 7])
        r0 = r2 ^ r0
        r0 = r0 ^ r4
        r0 = r0 + r2
        r2 = r2 ^ r0
        r1 = int(key[i & 7])
        r2 = r2 ^ r1
        array[i] = r2 & 0xff
    return bytes(array)
def base64Encode(string):
    return base64.b64encode(string.encode("utf-8")).decode('utf-8').translate(str.maketrans(string1, string2))
def base64Decode(string):
    return base64.b64decode(string.translate(str.maketrans(string1, string2))).decode('utf-8')
def randomeid():
    return 'eidAaf8081218as20a2GM%s7FnfQYOecyDYLcd0rfzm3Fy2ePY4UJJOeV0Ub840kG8C7lmIqt3DTlc11fB/s4qsAP8gtPTSoxu' % randomstr1(20)
def get_ep():
    jduuid = randomstr(16)
    # jduuid=base64Decode('EQHtZNG2CJu5CzcnCzu0CK==')
    # print(jduuid)
    ts = str(int(time.time() * 1000))
    bsjduuid = base64Encode(jduuid)
    # ts='1643792319938'
    area = base64Encode('%s_%s_%s_%s' % (
        random.randint(1, 10000), random.randint(1, 10000), random.randint(1, 10000), random.randint(1, 10000)))
    d_model = random.choice(['Mi11Ultra', 'Mi11', 'Mi10'])
    d_model = base64Encode(d_model)
    return '{"hdid":"JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw=","ts":%s,"ridx":-1,"cipher":{"area":"%s","d_model":"%s","wifiBssid":"dW5hbw93bq==","osVersion":"CJS=","d_brand":"WQvrb21f","screen":"CtS1DIenCNqm","uuid":"%s","aid":"%s","openudid":"%s"},"ciphertype":5,"version":"1.2.0","appname":"com.jingdong.app.mall"}' % (
        int(ts) - random.randint(100, 1000), area, d_model, bsjduuid, bsjduuid, bsjduuid), jduuid, ts
def get_sign(functionId, body, client, clientVersion):
    ep, suid, st = get_ep()
    # print(ep)
    sv = random.choice(["102", "111", "120"])
    # sv = '102'
    all_arg = "functionId=%s&body=%s&uuid=%s&client=%s&clientVersion=%s&st=%s&sv=%s" % (
        functionId, body, suid, client, clientVersion, st, sv)
    # print(all_arg)
    back_bytes = sign_core(str.encode(all_arg))
    info = hashlib.md5(base64.b64encode(back_bytes)).hexdigest()
    # print(info)
    # print(ep)
    return 'functionId=%s&clientVersion=%s&client=%s&sdkVersion=31&lang=zh_CN&harmonyOs=0&networkType=wifi&oaid=%s&eid=%s&ef=1&ep=%s&st=%s&sign=%s&sv=%s&body=%s' % (
        functionId, clientVersion, client, suid, randomeid(), urllib.parse.quote(ep), st, info, sv, urllib.parse.quote(body))


app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    abort(403)

@app.route('/genSign', methods=['GET', 'POST'])
def genSign():
    data = request.get_data()
    if data:
        try:
            data = json.loads(data)
            functionId = data['fn']
            body = data['body']
            sign = get_sign(functionId, body, sign_client, sign_clientVersion)
            rep = {
                "body": sign,
                "fn": functionId
            }
            return rep
        except Exception as e:
            errorMsg = f"❌ 第{e.__traceback__.tb_lineno}行：{e}"
            print(errorMsg)
            abort(400)

    else:
        abort(403)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4545, debug=False)
