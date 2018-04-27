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
            print "Handle Post webdata is ", webData
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                conn = pymysql.connect(host='47.93.228.142',port='3306', db='test', user='root', passwd='Roc2z2209861`', charset='utf8')
                cur = conn.cursor()
                cur.execute("select * from ta where id=%d and cust_type=%d")
                rows = cur.fetchall()
                print "%s"%rows
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = "test"
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            else:
                print "暂且不处理"
                return "success"
        except Exception, Argment:
            return Argment