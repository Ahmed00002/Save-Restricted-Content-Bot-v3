# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

import asyncio
from shared_client import start_client
import importlib
import os
import sys

async def load_and_run_plugins():
    # 🔹 Pyrogram clients start
    await start_client()

    plugin_dir = "plugins"
    plugins = [
        f[:-3]
        for f in os.listdir(plugin_dir)
        if f.endswith(".py") and f != "__init__.py"
    ]

    for plugin in plugins:
        module = importlib.import_module(f"plugins.{plugin}")
        # ইচ্ছা করলে আলাদা runner ফাংশন থাকলে চালাবে
        if hasattr(module, f"run_{plugin}_plugin"):
            print(f"Running {plugin} plugin...")
            await getattr(module, f"run_{plugin}_plugin")()

async def main():
    await load_and_run_plugins()
    print("✅ Bot started successfully. Waiting for events...")

    # আগের while True: sleep(1) এর বদলে — clean way
    stop_event = asyncio.Event()
    await stop_event.wait()  # কখনো set করছো না, মানে চিরকাল wait করবে

if __name__ == "__main__":
    print("Starting clients ...")
    try:
        # 🔥 asyncio.run নিজেই loop create+close করে, নিজে loop manage করা লাগবে না
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down...")
    except Exception as e:
        print(e)
        sys.exit(1)
