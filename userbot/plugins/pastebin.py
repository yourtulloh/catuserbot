import os

import pygments
from pygments.formatters import ImageFormatter
from pygments.lexers import Python3Lexer

from userbot import catub

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.tools import media_type
from ..helpers.utils import reply_id

plugin_category = "utils"

LOGS = logging.getLogger(__name__)


@catub.cat_cmd(
    pattern="pcode(?: |$)(.*)",
    command=("pcode", plugin_category),
    info={
        "header": "Will paste the entire text on the blank page and will send as image",
        "usage": ["{tr}pcode <reply>", "{tr}paste text"],
    },
)
async def _(event):
    "To paste text to image."
    reply_to = await reply_id(event)
    d_file_name = None
    catevent = await edit_or_reply(event, "`Pasting the text on blank page`")
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    text_to_print = ""
    if reply:
        mediatype = media_type(reply)
        if mediatype == "Document":
            d_file_name = await event.client.download_media(reply, "./temp/")
            with open(d_file_name, "r") as f:
                text_to_print = f.read()
    if text_to_print == "":
        if input_str:
            text_to_print = input_str
        elif event.reply_to_msg_id:
            text_to_print = reply.message
        else:
            await edit_delete(
                catevent,
                "`Either reply to text/code file or reply to text message or give text along with command`",
            )
    pygments.highlight(
        text_to_print,
        Python3Lexer(),
        ImageFormatter(font_name="DejaVu Sans Mono", line_numbers=True),
        "out.png",
    )
    try:
        await event.client.send_file(
            event.chat_id, "out.png", force_document=True, reply_to=reply_to
        )
        await catevent.delete()
        os.remove("out.png")
        if d_file_name is not None:
            os.remove(d_file_name)
    except Exception as e:
        await edit_delete(catevent, f"**Error:**\n`{str(e)}`", time=10)
