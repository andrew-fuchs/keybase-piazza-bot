from pykeybasebot import Bot, KbEvent
from pykeybasebot.types import chat1


async def chat_reply(bot: Bot, channel: chat1.ChatChannel,
            message_id: chat1.MessageID, message: str
        ) -> chat1.SendRes:
    await bot.ensure_initialized()
    # TODO do we need to handle `chat1.ConvIDStr` in `channel`?
    result = await bot.chat.execute({
        "method": "send",
        "params": {
            "options": {
                "channel": {
                    "name": channel.name
                },
                "message": {
                    "body": message,
                },
                "reply_to": message_id,
            },
        },
    })
    return chat1.SendRes.from_dict(result)


async def create_message(bot: Bot, channel: chat1.ChatChannel):
    send_result = await bot.chat.send(channel, '[Piazza Post Notification Text Goes Here]')
    await bot.chat.react(channel, send_result.message_id, ':speech_baloon:')


def kb_quote(in_str: str):
    return in_str.replace('\n', '\n>')


def escape_chat_chars(escape_str: str):
    # replace formatting chars with escaped versions
    # # TODO I doubt this is comprehensive
    # #      maybe escape anything not in [a-zA-Z0-9]?
    # escape_str = escape_str.replace('*', '\\*')
    # escape_str = escape_str.replace('_', '\\_')
    # escape_str = escape_str.replace('`', '\\`')
    # escape_str = escape_str.replace('>', '\\>')
    # escape_str = escape_str.replace('@', '\\@')
    # escape_str = escape_str.replace('#', '\\#')
    # return escape_str

    # escape anything that is not a letter ([a-zA-Z]), number ([0-9]), or whitespace
    out_str = ''
    for ch in escape_str:
        if ch.isalnum() or ch.isspace():
            out_str += ch
        else:
            out_str += '\\' + ch
    return out_str
