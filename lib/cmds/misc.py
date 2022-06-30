from typing import final
from lib.analysis import finalscores

def help(bot, prefix, cmds):
	bot.send_message(f"Registered commands: "
		+ ", ".join([f"{prefix}{cmd.callables[0]}" for cmd in sorted(cmds, key=lambda cmd: cmd.callables[0])]))

	bot.send_message(f"Registered commands (incl. aliases): "
		+ ", ".join([f"{prefix}{'/'.join(cmd.callables)}" for cmd in sorted(cmds, key=lambda cmd: cmd.callables[0])]))

def hello(bot, user, *args):
	bot.send_message(f"Hey {user['name']}!")

def mood(bot, message, *args):
	bot.send_message(message = f"{finalscores}")

