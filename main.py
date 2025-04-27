import asyncio
from shared_client import start_client
import importlib
import os
import sys
import signal

# Function to handle graceful shutdown
def graceful_shutdown(loop, signal=None):
    print("Shutting down gracefully...")
    loop.stop()

async def load_and_run_plugins():
    await start_client()
    plugin_dir = "plugins"
    plugins = [f[:-3] for f in os.listdir(plugin_dir) if f.endswith(".py") and f != "__init__.py"]

    for plugin in plugins:
        module = importlib.import_module(f"plugins.{plugin}")
        if hasattr(module, f"run_{plugin}_plugin"):
            print(f"Running {plugin} plugin...")
            await getattr(module, f"run_{plugin}_plugin")()

async def main():
    await load_and_run_plugins()
    while True:
        await asyncio.sleep(1)  # Keeps the bot running

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    # Listen for shutdown signals like Ctrl+C
    signal.signal(signal.SIGINT, lambda s, f: graceful_shutdown(loop, s))

    print("Starting clients ...")
    try:
        loop.run_until_complete(main())  # Run the bot
    except KeyboardInterrupt:
        print("Bot interrupted manually.")
    except Exception as e:
        print(e)
        sys.exit(1)
    finally:
        try:
            loop.close()  # Ensure the event loop is closed properly
        except Exception:
            pass
