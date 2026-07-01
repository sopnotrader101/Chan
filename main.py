import asyncio
import re
import html
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TOKEN = "8648013365:AAHeCpJQYJ3z7VS7FfI8Jf7yptbcjbWl2pA"
SOURCE_CHANNEL_ID = -1003722624508
DEST_CHANNEL_ID = -1003824270566

def remove_telefeed(text: str) -> str:
    if not text:
        return text
    text = re.sub(r'\n*[•\-]?\s*Sent via TeleFeed[^\n]*', '', text, flags=re.IGNORECASE)
    text = text.rstrip()
    return text

def has_other_link_or_username(text: str) -> bool:
    if not text:
        return False
    cleaned = re.sub(r'https?://t\.me/tg_feedbot\S*', '', text, flags=re.IGNORECASE)
    if re.search(r'https?://', cleaned, re.IGNORECASE):
        return True
    if re.search(r'@\w+', cleaned):
        return True
    return False

def bold_quote(text: str) -> str:
    return f"<blockquote><b>{text}</b></blockquote>"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.channel_post:
        return

    channel_post = update.channel_post

    if channel_post.chat_id != SOURCE_CHANNEL_ID:
        return

    raw_text = channel_post.text or channel_post.caption or ""
    text = remove_telefeed(raw_text)

    if has_other_link_or_username(text):
        return

    lines = text.split('\n')
    market = ""
    entry_time = ""
    timeframe = ""
    direction = ""
    is_win = "𝗪𝗜𝗡" in text
    is_loss = "𝗛𝗜𝗧 𝗚𝗔𝗟𝗘" in text

    for line in lines:
        line_stripped = line.strip()
        if '💷' in line:
            market = line.replace('💷', '').strip()
        elif '⏳' in line:
            entry_time = line.replace('⏳', '').strip()
        elif '⌚️' in line or '⌚' in line:
            timeframe = line.replace('⌚️', '').replace('⌚', '').strip()
        elif any(d in line for d in ['🔴', '🟢', 'PUT', 'CALL']):
            direction = line_stripped
        elif '𝗪𝗜𝗡' in line or '𝗛𝗜𝗧 𝗚𝗔𝗟𝗘' in line:
            parts = line.split('|')
            if len(parts) > 1:
                time_part = parts[1].replace('⏰', '').strip()
                market_match = re.search(r'(?:✅|☑️|°)\s*([A-Z0-9\-]+)', parts[0])
                if market_match:
                    market = market_match.group(1).strip()
                else:
                    market_part = parts[0].split('✅')[-1].strip() if '✅' in parts[0] else parts[0].split('☑️')[-1].strip()
                    market = market_part.replace('°', '').strip()
                entry_time = time_part

    m = html.escape(market)
    et = html.escape(entry_time)

    if is_win:
        new_text = bold_quote(
            "╔═══ 🟢 SIGNAL RESULT 🟢 ═══╗\n\n"
            f"✅ 𝗪𝗜𝗡 ➤ {m}\n\n"
            f"⏰ Entry Time ➤ {et}\n\n"
            "📈 Perfect Signal • Clean Profit 🔥\n\n"
            "👑 Join Vip up to 99% signal profit ➜ @SHOPNO_XDN\n"
            "╚═━════════✦═══════━═╝"
        )
    elif is_loss:
        new_text = bold_quote(
            "╔═══ 🔴 SIGNAL RESULT 🔴 ═══╗\n\n"
            f"❌ 𝗟𝗢𝗦𝗦 ➤ {m}\n\n"
            f"⏰ Entry Time ➤ {et}\n\n"
            "♻️ Recovery On Process ⚡\n\n"
            "📊 Next Signal Coming Soon\n"
            "╚═━═══════✦════════━═╝"
        )
    elif market and entry_time:
        dir_label = "🔴 PUT ⬇️ DOWN"
        if 'CALL' in direction or '🟢' in direction:
            dir_label = "🟢 CALL ⬆️ UP"

        new_text = bold_quote(
            "☂𝗦𝗢𝗣𝗡𝗢 𝗧𝗥𝗔𝗗𝗘𝗥•LIVE SIGNAL ☂\n\n"
            "💱 ╭─〔 𝗠𝗔𝗥𝗞𝗘𝗧 𝗣𝗔𝗜𝗥 〕─╮\n"
            f"     ➤  → 『 {m} 』\n"
            "      ╰────────────────✦\n\n"
            "⏰ ╭─〔 𝗘𝗡𝗧𝗥𝗬 𝗧𝗜𝗠𝗘 〕─╮\n"
            f"    ➤   ⌚  →  {et}\n"
            "      ╰───────◈──────╯\n\n"
            "⏳ ╭─〔 𝗧𝗥𝗔𝗗𝗘 𝗘𝗫𝗣𝗜𝗥𝗬 〕─╮\n"
            "        ➤ → 1 Minutes\n"
            "      ╰──────────────✦\n\n"
            "♻️ ╭─〔 𝗥𝗘𝗖𝗢𝗩𝗘𝗥𝗬 (𝗜𝗙 𝗟𝗢𝗦𝗦) 〕\n"
            "            ➤  ⚡ MTG→1\n"
            "      ╰──────────────✦\n\n"
            "📊 ╭─〔 𝗧𝗥𝗔𝗗𝗘 𝗗𝗜𝗥𝗘𝗖𝗧𝗜𝗢𝗡 〕─╮\n"
            f"       ➤ {dir_label}\n"
            "       ╰••┈┈┈┈┈✦✧✦┈┈┈┈┈••✦\n\n"
            "👑 Join Vip group ➜ @SHOPNO_XDN\n"
            "╚═━═══════─═══════ ═━═╝"
        )
    else:
        new_text = bold_quote(
            f"{html.escape(text)}\n\n"
            "👑 Join Vip group ➜ @SHOPNO_XDN\n"
            "╚═━════════─════════━═╝"
        )

    try:
        if channel_post.photo:
            await context.bot.send_photo(
                chat_id=DEST_CHANNEL_ID,
                photo=channel_post.photo[-1].file_id,
                caption=new_text,
                parse_mode=ParseMode.HTML
            )
        else:
            await context.bot.send_message(
                chat_id=DEST_CHANNEL_ID,
                text=new_text,
                parse_mode=ParseMode.HTML
            )
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    channel_handler = MessageHandler(filters.ChatType.CHANNEL, handle_message)
    application.add_handler(channel_handler)

    print("Bot is running...")
    application.run_polling()
