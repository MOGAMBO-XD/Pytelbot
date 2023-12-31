# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import sleep, Lock
from re import match
from pyrogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    CallbackQuery,)
from . import (
    FloodWait,
    ChatSendInlineForbidden,
    MessageNotModified,
    BotResponseTimeout,
    QueryIdInvalid,
    eor,
    filters,
    get_text,
    plugins_helper,
    px,
    pytel,
    pytel_tgb,
    random_prefixies,
    suppress,
    unpack_inline,
    plugins_button,
    _try_purged,
    buttons,
    ikmarkup,)

_HELP_LOCK = Lock()


@pytel.instruction(
    ["help", "ihelp"],
    outgoing=True,
    force_edit=False,
    supergroups=True,
    disable_errors=True,
)
async def _help(client, message):
    if message.command[0] == "ihelp":
        plugins_n = "xdbnafghjrt"
        try:
            _ = await client.get_inline_bot_results(
                pytel_tgb.me.username,
                plugins_n,
            )
            for name in _.results:
                try:
                    await message.reply_inline_bot_result(
                        _.query_id,
                        name.id,
                    )
                except ChatSendInlineForbidden:
                    return await message.reply(
                        "You cannot use inline bots to send messages in this chat."
                    )
        except BotResponseTimeout:
            await eor(
                message,
                text="Did not answer the request, please try again.",
            )
            return
        return await _try_purged(
            message
        )

    if message.command[0] == "help":
        plugins_name = get_text(message)
        name = None

        if not plugins_name:
            text = f"<b>Command Guide</b>\n\n<b><u>Example</u></b>\n</b>❯</b> <code>{random_prefixies(px)}help webtools</code>\n    └ <u>To get plugins webtools.</u>\n</b>❯</b> <code>{random_prefixies(px)}ihelp</code>\n    └ <u>To get Inline helper.</u>"
            await eor(
                message,
                text=text,
            )
            return

        if (
            plugins_name
            in plugins_helper
        ):
            name = plugins_name
        else:
            for (
                x
            ) in plugins_name.split():
                if x in plugins_helper:
                    name = x
                    break
        if name:
            cmds = plugins_helper[name]
            text = f"<b>{len(cmds)} Commands For <u>{name.upper()}</u></b>\n\n"
            for (
                cmd,
                desc,
            ) in cmds.items():
                text += "</b>❯</b> <code>{}</code>\n<b>Description:</b> <i>{}</i>\n\n".format(
                    cmd,
                    desc,
                )
            text += (
                "(c) @kastaid #pytel"
            )
            await eor(
                message,
                text=text,
            )
            return
        await eor(
            message,
            text=f"<b>Plugins Not Found</b> for <code>{plugins_name}</code>\n<b><u>Example</u>:</b> <code>{random_prefixies(px)}ihelp</code> to see inline helper.",
        )
        return


@pytel_tgb.on_inline_query(
    filters.regex("^xdbnafghjrt")
)
async def _helper_inline(
    client,
    cq: CallbackQuery,
):
    content = "<b>❏ <u>Help Menu</u>\n├ Plugins : {}\n├ Commands : {}\n└  Prefixies : <code>{}</code></b>\n\n".format(
        plugins_helper.count,
        plugins_helper.total,
        random_prefixies(px),
    )
    content += "(c) @kastaid #pytel"
    await sleep(0.2)
    with suppress(QueryIdInvalid):
        await client.answer_inline_query(
            cq.id,
            is_personal=True,
            results=[
                (
                    InlineQueryResultArticle(
                        title="MENU\n@kastaid #pytel",
                        reply_markup=ikmarkup(
                            plugins_button(
                                0,
                                plugins_helper,
                                "help",
                            )
                        ),
                        input_message_content=InputTextMessageContent(
                            content
                        ),
                    )
                )
            ],
        )


@pytel_tgb.on_callback_query(
    filters.regex(r"help_(.*?)")
)
async def _(
    client,
    cq: CallbackQuery,
):
    plugins_text = "<b>❏ <u>Help Menu</u>\n├ Plugins : {}\n├ Commands : {}\n└ Prefixies : <code>{}</code></b>\n\n".format(
        plugins_helper.count,
        plugins_helper.total,
        random_prefixies(px),
    )
    plugins_text += (
        "(c) @kastaid #pytel"
    )
    plugins_match = match(
        r"help_plug\((.+?)\)",
        cq.data,
    )
    prev_page = match(
        r"help_prev\((.+?)\)",
        cq.data,
    )
    next_page = match(
        r"help_next\((.+?)\)",
        cq.data,
    )
    back_page = match(
        r"help_back",
        cq.data,
    )
    close_page = match(
        r"help_close",
        cq.data,
    )
    async with _HELP_LOCK:
        if plugins_match:
            nm = plugins_match[1]
            for _ in nm:
                name = (
                    _
                    if _
                    in plugins_helper
                    else nm
                )
                cmds = plugins_helper[
                    name
                ]
                text = f"<b>{len(cmds)} Commands For <u>{name.upper()}</b></u>\n\n"
                for (
                    cmd,
                    desc,
                ) in cmds.items():
                    text += "<b>❯</b><code>{}</code>\n<b>Description:</b> <i>{}</i>\n\n".format(
                        cmd,
                        desc,
                    )
                text += "(c) @kastaid #pytel"
                button = [
                    [
                        buttons(
                            "‹ ʙᴀᴄᴋ",
                            callback_data="help_back",
                        ),
                        buttons(
                            "ᴄʟᴏꜱᴇ ›",
                            callback_data="help_close",
                        ),
                    ]
                ]
                for _ in pytel._client:
                    if (
                        cq.from_user.id
                        == int(_.me.id)
                    ):
                        try:
                            await cq.edit_message_text(
                                text=text,
                                reply_markup=ikmarkup(
                                    button
                                ),
                                disable_web_page_preview=True,
                            )
                            return
                        except (
                            MessageNotModified,
                            FloodWait,
                        ) as excp:
                            if (
                                excp.ID
                                == "FLOOD_WAIT_X"
                            ):
                                await sleep(
                                    excp.value
                                )
                            elif (
                                excp.ID
                                == "MESSAGE_NOT_MODIFIED"
                            ):
                                await sleep(
                                    0.1
                                )
        #                    else:
        #                        text = "You're not allowed."
        #                        await client.answer_callback_query(
        #                            cq.id,
        #                            text,
        #                            show_alert=True,
        #                        )

        elif prev_page:
            curr_page = int(
                prev_page[1]
            )
            for _ in pytel._client:
                if (
                    cq.from_user.id
                    == int(_.me.id)
                ):
                    try:
                        await cq.edit_message_text(
                            text=plugins_text,
                            reply_markup=ikmarkup(
                                plugins_button(
                                    curr_page
                                    - 1,
                                    plugins_helper,
                                    "help",
                                )
                            ),
                        )
                        return
                    except (
                        MessageNotModified,
                        FloodWait,
                    ) as excp:
                        if (
                            excp.ID
                            == "FLOOD_WAIT_X"
                        ):
                            await sleep(
                                excp.value
                                + 3
                            )
                        elif (
                            excp.ID
                            == "MESSAGE_NOT_MODIFIED"
                        ):
                            await sleep(
                                0.1
                            )
        #                else:
        #                    text = "You're not allowed."
        #                    await client.answer_callback_query(
        #                        cq.id,
        #                        text,
        #                        show_alert=True,
        #                    )

        elif next_page:
            nx_page = int(next_page[1])
            for _ in pytel._client:
                if (
                    cq.from_user.id
                    == int(_.me.id)
                ):
                    try:
                        await cq.edit_message_text(
                            text=plugins_text,
                            reply_markup=ikmarkup(
                                plugins_button(
                                    nx_page
                                    + 1,
                                    plugins_helper,
                                    "help",
                                )
                            ),
                        )
                        return
                    except (
                        MessageNotModified,
                        FloodWait,
                    ) as excp:
                        if (
                            excp.ID
                            == "FLOOD_WAIT_X"
                        ):
                            await sleep(
                                excp.value
                                + 3
                            )
                        elif (
                            excp.ID
                            == "MESSAGE_NOT_MODIFIED"
                        ):
                            await sleep(
                                0.1
                            )
        #                else:
        #                    text = "You're not allowed."
        #                    await client.answer_callback_query(
        #                        cq.id,
        #                        text,
        #                        show_alert=True,
        #                    )

        elif back_page:
            for _ in pytel._client:
                if (
                    cq.from_user.id
                    == int(_.me.id)
                ):
                    with suppress(
                        FloodWait
                    ):
                        await cq.edit_message_text(
                            text=plugins_text,
                            reply_markup=ikmarkup(
                                plugins_button(
                                    0,
                                    plugins_helper,
                                    "help",
                                )
                            ),
                        )
                        return
        #                else:
        #                    text = "You're not allowed."
        #                    await client.answer_callback_query(
        #                        cq.id,
        #                        text,
        #                        show_alert=True,
        #                    )

        elif close_page:
            cq.data.split()
            for _ in pytel._client:
                if (
                    cq.from_user.id
                    == int(_.me.id)
                ):
                    un = unpack_inline(
                        cq.inline_message_id
                    )
                    chat_id: int = un[
                        "chat_id"
                    ]
                    message_id: int = (
                        un["message_id"]
                    )
                    await _.delete_messages(
                        chat_id=int(
                            chat_id
                        ),
                        message_ids=int(
                            message_id
                        ),
                    )
                    return


#                else:
#                    text = "Only senders can close this inline."
#                    await client.answer_callback_query(
#                        cq.id,
#                        text,
#                        show_alert=True,
#                    )
#                    return


plugins_helper["help"] = {
    f"{random_prefixies(px)}help [plugin_name]/[reply]": "Get common/plugin/command help by filling the plugin name or reply single word or message that contains plugin name.",
    f"{random_prefixies(px)}ihelp": "Get inline helper.",
}
