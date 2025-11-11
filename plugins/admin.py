# plugins/admin.py

from pyrogram import filters
from shared_client import app as X
from database import db
import os, asyncio

OWNER_ID = int(os.getenv("OWNER_ID", "0"))

@X.on_message(filters.command("users") & filters.private)
async def all_users_cmd(client, message):
    uid = message.from_user.id
    if uid != OWNER_ID:
        await message.reply_text("🚫 You are not allowed to use this command.")
        return

    status_msg = await message.reply_text("📦 Fetching users from database… ⏳")

    try:
        cursor = db.users.find(
            {},
            {
                "_id": 0,
                "user_id": 1,
                "is_premium": 1,
                "daily_count": 1,
                "daily_date": 1,
            },
        )

        total_users = await db.users.count_documents({})
        fetched = 0
        users = []

        anim = ["🔹", "🔸", "🔹", "🔸", "🔹"]
        step = 0

        async for u in cursor:
            users.append(u)
            fetched += 1

            if fetched % 100 == 0:
                step = (step + 1) % len(anim)
                await status_msg.edit_text(
                    f"{anim[step]} Fetching users... ({fetched}/{total_users})"
                )

        if not users:
            await status_msg.edit_text("ℹ️ No users found in database.")
            return

        await status_msg.edit_text(f"✅ Fetched all users ({fetched}/{total_users})")

        lines = []
        for u in users:
            u_id = u.get("user_id")
            prem = u.get("is_premium", False)
            cnt = u.get("daily_count", 0)
            dte = u.get("daily_date", "N/A")
            status = "💎 Premium" if prem else "🆓 Free"
            lines.append(f"{u_id} | {status} | {cnt} | {dte}")

        header = "user_id | status | daily_count | daily_date"
        content = header + "\n" + "\n".join(lines)
        filename = "users_list.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        await message.reply_document(
            filename,
            caption=f"👥 Total users: {len(users)}\n✨ Fetch complete successfully!",
        )
        os.remove(filename)
        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text(f"⚠️ Error fetching users: {str(e)[:100]}")
