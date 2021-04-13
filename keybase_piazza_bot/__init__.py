#!/usr/bin/env python3

import argparse
import asyncio
import logging
import re
import sys
import urllib

from piazza_api import Piazza
from pykeybasebot import Bot, KbEvent
from pykeybasebot.types import chat1

from .piazza import piazza_post_url
from .keybase import chat_reply, escape_chat_chars, kb_quote

# !!! put the `network id` of the class this bot is for here
PIAZZA_NETWORK_ID = 'REPLACE WITH YOUR CLASS\'S PIAZZA NETWORK ID'

logger = logging.getLogger('keybase_piazza_bot')


def main(argv=sys.argv[1:]):
    argument_parser = argparse.ArgumentParser()
    # argument_parser.add_argument('--username', type=str,
    #         default='PiazzaBot', help='the bot\'s Keybase username')
    args = argument_parser.parse_args(argv)

    logger.info('keybase_piazza_bot starting')

    event_loop = asyncio.get_event_loop()

    piazza = Piazza()
    piazza.user_login() # login prompt
    cse220 = piazza.network(PIAZZA_NETWORK_ID)

    keybase_bot_handler = KeybaseBotHandler(piazza, cse220)
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
    def __init__(self, piazza, piazza_network):
        self.piazza = piazza
        self.piazza_network = piazza_network

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
            match = re.match(r'^!piazza @?(?P<post_id>\d+?)$', msg_text_body, re.IGNORECASE)
            if match:
                try:
                    piazza_post_id = int(match['post_id'])
                except ValueError as exc:
                    logger.error('invalid post id', exc_info=exc)
                    return

                # get post info from piazza
                post = self.piazza_network.get_post(piazza_post_id)
                # FIXME: for production code we should be doing error handling here

                # send the bot's reply
                await chat_reply(bot, msg_channel, msg_id,
                        '@{} Piazza post `@{}`:\n{}\n*{:.100s}*\n>{:.200s}'.format(
                            escape_chat_chars(msg_sender_username),
                            escape_chat_chars(str(post['nr'])),
                            piazza_post_url(PIAZZA_NETWORK_ID, post['nr']),
                            escape_chat_chars(str(post['history'][0]['subject'])),
                            kb_quote(escape_chat_chars(str(post['history'][0]['content']))),
                        ))
                # await chat_reply(bot, msg_channel, msg_id,
                #         '@{} Piazza post `@{}`'.format(
                #             msg_sender_username_esc, piazza_post_id_esc
                #         ))
            else:
                # send an error message
                await chat_reply(bot, msg_channel, msg_id,
                        '@{} Use `!piazza <Post ID>`'.format(
                            escape_chat_chars(msg_sender_username)
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


if __name__ == '__main__':
    main()
