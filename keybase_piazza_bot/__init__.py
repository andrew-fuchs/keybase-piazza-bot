#!/usr/bin/env python3

import argparse
import asyncio
import logging
import re
import sys

from pykeybasebot import Bot, KbEvent
from pykeybasebot.types import chat1

logger = logging.getLogger('keybase_piazza_bot')
# CSE220_ServerBot


def main(argv=sys.argv[1:]):
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('--username', type=str,
            default='PiazzaBot', help='the bot\'s Keybase username')
    args = argument_parser.parse_args(argv)

    logger.info('keybase_piazza_bot starting')

    event_loop = asyncio.get_event_loop()

    keybase_bot_handler = KeybaseBotHandler()
    keybase_bot = Bot(
        handler=keybase_bot_handler,
        loop=event_loop,
        # username=args.username,
    )
    future = keybase_bot.start({})

    event_loop.run_until_complete(future)
    event_loop.close()

    logger.info('keybase_piazza_bot exiting')


class KeybaseBotHandler:
    async def __call__(self, bot: Bot, event: KbEvent):
        print('handling', event)

        type_name = event.msg.content.type_name

        if type_name == chat1.MessageTypeStrings.TEXT.value:
            await self.handle_text_message(bot, event)
        elif type_name == chat1.MessageTypeStrings.REACTION.value:
            await self.handle_reaction_message(bot, event)
        elif type_name == chat1.MessageTypeStrings.DELETE.value:
            await self.handle_delete_message(bot, event)


    async def handle_text_message(self, bot: Bot, event: KbEvent):
        msg_id = event.msg.id
        msg_sender_username = event.msg.sender.username
        msg_channel = event.msg.channel
        msg_text_body = event.msg.content.text.body

        # is this the "!piazza" command?
        if msg_text_body.lower().startswith('!piazza'):
            # check if the command is valid and parse the post id
            match = re.match(r'^!piazza (?P<post_id>\d+?)$', msg_text_body, re.IGNORECASE)
            if match:
                try:
                    piazza_post_id = int(match['post_id'])
                except ValueError as exc:
                    logger.error('invalid post id', exc_info=exc)
                    return
                # send the bot's reply
                msg_sender_username_esc = escape_chat_chars(msg_sender_username)
                piazza_post_id_esc = escape_chat_chars(str(piazza_post_id))
                await chat_reply(bot, msg_channel, msg_id,
                        '@{} Piazza post `@{}`'.format(
                            msg_sender_username_esc, piazza_post_id_esc
                        ))
            else:
                # send an error message
                msg_sender_username_esc = escape_chat_chars(msg_sender_username)
                await chat_reply(bot, msg_channel, msg_id,
                        '@{} Use `!piazza <Post ID>`'.format(
                            msg_sender_username_esc
                        ))

    async def handle_reaction_message(self, bot: Bot, event: KbEvent):
        # channel = event.msg.channel
        # sender_username = event.sender.username
        # msg_id = event.msg.id
        # reaction_to = event.msg.content.reaction.message_id
        pass


    async def handle_delete_message(self, bot: Bot, event: KbEvent):
        # channel = event.msg.channel
        # delete_message_ids = event.msg.content.delete.message_i_ds
        pass


async def create_message(bot: Bot, channel: chat1.ChatChannel):
    send_result = await bot.chat.send(channel, '[Piazza Post Notification Text Goes Here]')
    await bot.chat.react(channel, send_result.message_id, ':speech_baloon:')


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

    # escape anything that is not a letter ([a-zA-Z]) or number ([0-9])
    out_str = ''
    for ch in escape_str:
        if ch.isalnum():
            out_str += ch
        else:
            out_str += '\\' + ch
    return out_str


if __name__ == '__main__':
    main()
