import time

def gen_text_message(tousername, fromusername, content):
    """generate a text message with wechat format.

    Args:
        to_user_name: who the message send to
        from_user_name: who the messge from
        content: the message contents

    Returns:
        a complete text message
    """
    xml_response = """<xml>
                    <ToUserName><![CDATA[%s]]></ToUserName>
                    <FromUserName><![CDATA[%s]]></FromUserName>
                    <CreateTime>%s</CreateTime>
                    <MsgType><![CDATA[%s]]></MsgType>
                    <Content><![CDATA[%s]]></Content>
                    </xml>"""
    response = xml_response % (tousername, fromusername, str(int(time.time())), "text", content)
    return response

def gen_text_picture_message(tousername, fromusername, title, desc, picurl, url):
    """generate a text & picture message with wechat format.

    Args:
        to_user_name: who the message send to
        from_user_name: who the messge from
        title: the message title
        desc: the description of message
        picurl: the url of picture in message
        url: the links which click on the graphic message will jump to

    Returns:
        a complete text & picture message

    """
    xml_response = """<xml>
                    <ToUserName><![CDATA[%s]]></ToUserName>
                    <FromUserName><![CDATA[%s]]></FromUserName>
                    <CreateTime>%s</CreateTime>
                    <MsgType><![CDATA[news]]></MsgType>
                    <ArticleCount>1</ArticleCount>
                    <Articles>
                    <item>
                    <Title><![CDATA[%s]]></Title>
                    <Description><![CDATA[%s]]></Description>
                    <PicUrl><![CDATA[%s]]></PicUrl>
                    <Url><![CDATA[%s]]></Url>
                    </item>
                    </Articles>
                    </xml>"""
    response = xml_response % (tousername, fromusername, str(int(time.time())),
                                title, desc, picurl, url)
    return response
