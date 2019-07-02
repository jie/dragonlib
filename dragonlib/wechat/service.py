import logging
import json
from hashlib import sha1
from tornado import httpclient
from urllib import parse

logger = logging.getLogger(__name__)


class WechatException(Exception):
    pass


class WechatCodeExpired(Exception):
    pass


class WechatRequestError(WechatException):
    pass


class WechatService(object):
    def __init__(self, config):
        config.update(
            authorize_url="https://open.weixin.qq.com/connect/oauth2/authorize?appid={appid}&redirect_uri={redirect_uri}&response_type=code&scope={scope}&state={state}#wechat_redirect",
            access_url="https://api.weixin.qq.com/sns/oauth2/access_token?appid={appid}&secret={secret}&code={code}&grant_type=authorization_code",
            refresh_url="https://api.weixin.qq.com/sns/oauth2/refresh_token?appid={appid}&grant_type=refresh_token&refresh_token={refresh_token}",
            userinfo_url="https://api.weixin.qq.com/sns/userinfo?access_token={access_token}&openid={openid}&lang=zh_CN",
            client_credential_url="https://api.weixin.qq.com/cgi-bin/token?grant_type={grant_type}&appid={appid}&secret={secret}",
            jsapi_ticket_url="https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={access_token}&type=jsapi",
            send_message_url="https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={access_token}",
        )
        self.config = config
        self.appid = self.config["appid"]
        self.appsecret = self.config["appsecret"]

    def parse_json(self, raw):
        return json.loads(str(raw, "utf8"))

    def http_request(self, url, body=None, method="GET", **kwargs):
        http_client = httpclient.HTTPClient()
        if method.upper() == "POST":
            response = http_client.fetch(url, method=method, body=body)
        else:
            response = http_client.fetch(url, method=method)
        return response

    def get_authorize_url(self, state, redirect_uri, scope="snsapi_userinfo"):
        kwargs = {
            "appid": self.appid,
            "redirect_uri": parse.quote(redirect_uri),
            "scope": scope,
            "state": state,
        }
        return self.config["authorize_url"].format(**kwargs)

    def get_access_token(self, code):
        kwargs = {"appid": self.appid, "secret": self.appsecret, "code": code}
        url = self.config["access_url"].format(**kwargs)
        response = self.http_request(url)
        result = self.parse_json(response.body)

        if result.get("errcode") != 0 and result.get("errcode") is not None:
            if result["errcode"] == 40029:
                raise WechatCodeExpired(response.body)
            raise WechatException("error when get_access_token: %s" % response.body)
        return result

    def get_userinfo(self, access_token, openid):
        kwargs = {"appid": self.appid, "openid": openid, "access_token": access_token}
        url = self.config["userinfo_url"].format(**kwargs)
        response = self.http_request(url)
        result = self.parse_json(response.body)

        if result.get("errcode") != 0 and result.get("errcode") is not None:
            raise WechatException("erro when get_userinfo: %s" % response.body)
        return result

    def get_access_token_by_client_credential(self):
        kwargs = {
            "appid": self.appid,
            "secret": self.appsecret,
            "grant_type": "client_credential",
        }
        response = self.http_request(
            self.config["client_credential_url"].format(**kwargs)
        )
        result = self.parse_json(response.body)

        if result.get("errcode") != 0 and result.get("errcode") is not None:
            raise WechatException(
                "error when get_access_token_by_client_credential: %s" % response.body
            )
        return result

    def get_jsapi_ticket(self, access_token):
        kwargs = {"access_token": access_token}
        response = self.http_request(self.config["jsapi_ticket_url"].format(**kwargs))
        result = self.parse_json(response.body)

        if result.get("errcode") != 0 and result.get("errcode") is not None:
            raise WechatException("error when get_jsapi_ticket: %s" % response.body)
        return result

    @staticmethod
    def get_signature(noncestr, jsapi_ticket, timestamp, url):
        data = {
            "noncestr": noncestr,
            "jsapi_ticket": jsapi_ticket,
            "timestamp": timestamp,
            "url": url,
        }
        keys = list(data.keys())
        keys.sort()
        da = "&".join(["%s=%s" % (key, data[key]) for key in keys])
        signature = sha1(da.encode("utf-8")).hexdigest()
        return signature

    def sendMessage(self, content, toUser, access_token):
        body = json.dumps(
            {"touser": toUser, "msgtype": "text", "text": {"content": content}},
            ensure_ascii=False
        )
        logger.info('sendMessage:%s' % body)
        response = self.http_request(
            self.config["send_message_url"].format(access_token=access_token),
            body=body,
            method="POST",
        )
        result = self.parse_json(response.body)
        logger.info('sendResponse:%s' % result)
        if result.get("errcode") != 0 and result.get("errcode") is not None:
            raise WechatException("error when sendMessage: %s" % response.body)
        return result
