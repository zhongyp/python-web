# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import reply
import receive
import pymysql

class Handle(object):
    def GET(self):# get请求
        try:
            data = web.input()
            if len(data) == 0:
                return "this is a demo"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "xuyf001" #请按照公众平台官网\基本配置中信息填写
            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            return Argument
    def POST(self):# post请求
        try:
            webData = web.data()
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text' and recMsg.Content[1] != "'":
                conn = pymysql.connect(host='', port=3306, user='root', passwd='', db='test',charset='utf8mb4')
                cursor = conn.cursor()
                cursor.execute("select * from questions where question like '%" + recMsg.Content + "%'")
                rows = cursor.fetchall()
                content=""
                if len(rows)>0:
                    for row in rows:
                        content += "问题:".decode('utf-8').encode('utf-8') +  row[1].encode('utf-8') + '\n' + "答案:".decode('utf-8').encode('utf-8')  + row[2].encode('utf-8') + '\n'
                else:
                    content = "没有找到相关问题！"
                conn.commit()
                cursor.close()
                conn.close()
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                description = content
                replyMsg = reply.ImageTextMsg(toUser, fromUser, description)
                return replyMsg.send()
            else:
                return "success"
        except Exception, Argment:
            return Argment 
