from telethon import events, functions, types

from .managers import edit_or_reply


@events.common.name_inner_event
class NewMessage(events.NewMessage):
    def __init__(self, require_admin: bool = None, inline: bool = False, **kwargs):
        super().__init__(**kwargs)

        self.require_admin = require_admin
        self.inline = inline

    def filter(self, event):
        _event = super().filter(event)
        if not _event:
            return

        if self.inline is not None and bool(self.inline) != bool(
            event.message.via_bot_id
        ):
            return

        if self.require_admin and not isinstance(event._chat_peer, types.PeerUser):
            is_creator = False
            is_admin = False
            creator = hasattr(event.chat, "creator")
            admin_rights = hasattr(event.chat, "admin_rights")
            if not creator and not admin_rights:
                event.chat = event._client.loop.create_task(event.get_chat())

            if self.incoming:
                try:
                    p = event._client.loop.create_task(
                        event._client(
                            functions.channels.GetParticipantRequest(
                                event.chat_id, event.sender_id
                            )
                        )
                    )
                    participant = p.participant
                except Exception:
                    participant = None
                if isinstance(participant, types.ChannelParticipantCreator):
                    is_creator = True
                if isinstance(participant, types.ChannelParticipantAdmin):
                    is_admin = True
            else:
                is_creator = event.chat.creator
                is_admin = event.chat.admin_rights

            if not is_creator and not is_admin:
                text = "`I need admin rights to be able to use this command!`"

                event._client.loop.create_task(edit_or_reply(event, text))
                return
        return event


@events.common.name_inner_event
class MessageEdited(NewMessage):
    @classmethod
    def build(cls, update, others=None, self_id=None):
        if isinstance(update, types.UpdateEditMessage):
            return cls.Event(update.message)
        if isinstance(update, types.UpdateEditChannelMessage):
            if (
                update.message.edit_date
                and update.message.is_channel
                and not update.message.is_group
            ):
                return
            return cls.Event(update.message)

    class Event(NewMessage.Event):
        pass

async def send_message(client, **kwargs):
    chatid = kwargs.get("entity",-100)
    if str(chatid) == str(Config.BOTLOG_CHATID):
        return await client.send_message(**kwargs)
    msg = kwargs.get("message","")
    if (Config.STRING_SESSION in msg) or (Config.APP_ID in msg) or (Config.API_HASH in msg) or (Config.TG_BOT_TOKEN in msg) or (Config.HEROKU_API_KEY and Config.HEROKU_API_KEY in msg) or (Config.SCREEN_SHOT_LAYER_ACCESS_KEY and Config.SCREEN_SHOT_LAYER_ACCESS_KEY in msg):
        if BOTLOG:
            kwargs["entity"] = Config.BOTLOG_CHATID
            await client.send_message(**kwargs)
        msg = "Sorry I can't send this information in public chats i will send it in Bot Log group check it from there"
    kwargs["message"] = msg
    kwargs["entity"] = chatid
    return await client.send_message(**kwargs)

async def send_file(client, **kwargs):
    chatid = kwargs.get("entity",-100)
    if str(chatid) == str(Config.BOTLOG_CHATID):
        return await client.send_file(**kwargs)
    msg = kwargs.get("caption","")
    if (Config.STRING_SESSION in msg) or (Config.APP_ID in msg) or (Config.API_HASH in msg) or (Config.TG_BOT_TOKEN in msg) or (Config.HEROKU_API_KEY and Config.HEROKU_API_KEY in msg) or (Config.SCREEN_SHOT_LAYER_ACCESS_KEY and Config.SCREEN_SHOT_LAYER_ACCESS_KEY in msg):
        if BOTLOG:
            kwargs["entity"] = Config.BOTLOG_CHATID
            await client.send_file(**kwargs)
        msg = "Sorry I can't send this information in public chats i will send it in Bot Log group check it from there"
    kwargs["caption"] = msg
    kwargs["entity"] = chatid
    return await client.send_file(**kwargs)
    
async def edit_message(client, **kwargs):
    chatid = kwargs.get("entity",-100)
    if str(chatid) == str(Config.BOTLOG_CHATID):
        return await client.edit_message(**kwargs)
    msg = kwargs.get("message","")
    if (Config.STRING_SESSION in msg) or (Config.APP_ID in msg) or (Config.API_HASH in msg) or (Config.TG_BOT_TOKEN in msg) or (Config.HEROKU_API_KEY and Config.HEROKU_API_KEY in msg) or (Config.SCREEN_SHOT_LAYER_ACCESS_KEY and Config.SCREEN_SHOT_LAYER_ACCESS_KEY in msg):
        if BOTLOG:
            kwargs["entity"] = Config.BOTLOG_CHATID
            await client.edit_message(**kwargs)
        msg = "Sorry I can't send this information in public chats i will send it in Bot Log group check it from there"
    kwargs["message"] = msg
    kwargs["entity"] = chatid
    return await client.edit_message(**kwargs)
