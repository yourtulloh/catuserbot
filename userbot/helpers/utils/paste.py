import json

import requests


async def p_paste(message, extension=None):
    """
    To Paste the given message/text/code to paste.pelkum.dev
    """
    siteurl = "https://paste.pelkum.dev/api/v1/pastes/"
    data = {"content": message}
    response = requests.post(url=siteurl, data=json.dumps(data))
    if response.ok:
        response = response.json()
        if extension is None:
            return {
                "url": f"https://paste.pelkum.dev/{response['id']}",
                "raw": "",
                "token": response["deletionToken"],
            }
        return {
            "url": f"https://paste.pelkum.dev/{response['id']}.{extension}",
            "raw": "",
            "token": response["deletionToken"],
        }
    return {"error": "Unable to reach paste.pelkum.dev"}


async def s_paste(message):
    """
    To Paste the given message/text/code to spaceb.in
    """
    siteurl = "https://spaceb.in/api/v1/documents/"
    response = requests.post(siteurl, data={"content": message, "extension": "txt"})
    if response.ok:
        response = response.json()
        if response["error"] != "" and response["status"] < 400:
            return {"error": response["error"]}
        return {
            "url": f"https://spaceb.in/{response['payload']['id']}",
            "raw": f"{siteurl}/{response['payload']['id']}/raw",
        }
    return {"error": "Unable to reach nekobin."}


async def n_paste(message, extension=None):
    """
    To Paste the given message/text/code to nekobin
    """
    siteurl = "https://nekobin.com/api/documents"
    data = {"content": message}
    response = requests.post(url=siteurl, data=json.dumps(data))
    if response.ok:
        response = response.json()
        if extension is None:
            return {
                "url": f"nekobin.com/{response['result']['key']}",
                "raw": f"nekobin.com/raw/{response['result']['key']}",
            }
        return {
            "url": f"nekobin.com/{response['result']['key']}.{extension}",
            "raw": f"nekobin.com/raw/{response['result']['key']}",
        }
    return {"error": "Unable to reach nekobin."}
