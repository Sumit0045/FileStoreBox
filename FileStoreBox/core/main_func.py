from config import HOST_URL
from pyrogram.enums import MessageMediaType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
from FileStoreBox.core.mongo import toolsdb


async def must_join(_, message, user_id):
    data = await toolsdb.get_data(user_id)
    if data and data.get("force_channel"):
        force_channel = data.get("force_channel")
        if force_channel:
            invite_link = await _.create_chat_invite_link(force_channel)
            try:
                user = await _.get_chat_member(force_channel, message.from_user.id)
                if user.status == "kicked":
                    await message.reply_text("Sorry Sir, You are Banned from using me.")
                    return
            except UserNotParticipant:
                await message.reply_photo(
                    "https://telegra.ph/file/b7a933f423c153f866699.jpg", 
                    caption=script.FORCE_MSG.format(message.from_user.mention),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🤖 Join Update Channel", url=invite_link.invite_link)]
                    ])
                )
                return 1
    else:
        pass
        return 0



async def fetch_files(_, message):
    try:
        parts = message.text.split("_")
        user_id = parts[1]
        id = parts[2]

        joined = await must_join(_, message, user_id)
        if joined == 1:
            return

        data = await toolsdb.get_data(user_id)
        force_channel = data.get("force_channel") if data else None
        database_channel = data.get("channel_id") if data else None

        if force_channel:
            invite_link = await _.create_chat_invite_link(force_channel)
            try:
                user = await _.get_chat_member(force_channel, message.from_user.id)
                if user.status == "kicked":
                    await message.reply_text("Sorry Sir, You are Banned from using me.")
                    return
            except Exception:
                await message.reply_photo(
                    "https://telegra.ph/file/b7a933f423c153f866699.jpg",
                    caption=script.FORCE_MSG.format(message.from_user.mention),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🤖 Join Update Channel", url=invite_link.invite_link)],
                        [InlineKeyboardButton("🔄 Try Again", callback_data=f"checksub#{id}")]
                    ])
                )
                return

        file = await _.get_messages(database_channel, int(id))
        if file.media == "video":
            file_id = file.video.file_id
            title = file.video.file_name
        else:
            file_id = file.document.file_id
            title = file.document.file_name

        file_caption = f"📑 {title}"
        buttons = [[InlineKeyboardButton('Downloads', url=f"{HOST_URL}/{id}")]]

        await _.send_cached_media(
            chat_id=message.from_user.id,
            file_id=file_id,
            caption=file_caption,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return
    except Exception as e:
        await message.reply_text(f"Error: `{str(e)}`")
        return



