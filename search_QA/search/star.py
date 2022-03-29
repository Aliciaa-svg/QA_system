import httpx

def get_star_sign(star_sign: str):
    #   这里使用的是聚合数据的api接口 星座运势 （免费）
    #   还请使用这个插件的人自己去申请一个key
    key = "cde5e16435cd0217f505a88898b60707"
    query = httpx.get("http://web.juhe.cn/constellation/getAll?consName={}&type=today&key={}".format(star_sign,key))
    #   这里的type参数中，聚合API提供了today,tomorrow,week,month,year ，我只用了today
    xingzuo = query.json()
    if xingzuo["error_code"]!=0:
        return xingzuo["reason"]
    else:
        name = xingzuo["name"]
        color = xingzuo["color"]
        work = xingzuo["work"]
        lucky_number = xingzuo["number"]
        summary = xingzuo["summary"]

        message = f"{name}今天的幸运色为{color}，工作/学习指数为{work}，幸运数字为{lucky_number}，{summary}"
        # print(message)
        return message

# if __name__ == '__main__' :
#     message = get_star_sign('白羊座')
#     print(message)
