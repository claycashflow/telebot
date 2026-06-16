from __future__ import annotations

import argparse
import asyncio
from typing import Any

from app.bot.channel_forwarder import (
    has_string_session,
    load_forwarded_ids,
    load_forwarder_settings,
    match_message,
    save_forwarded_ids,
    should_forward,
    validate_forwarder_settings,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scan a Telegram channel for matching posts and optionally watch/forward them."
    )
    parser.add_argument("--limit", type=int, default=30, help="How many recent posts to scan.")
    parser.add_argument(
        "--forward-latest",
        action="store_true",
        help="Forward the newest matched post to the target channel.",
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Keep watching for new matching posts and forward them automatically.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="In watch mode, print matches without forwarding them.",
    )
    parser.add_argument(
        "--print-string-session",
        action="store_true",
        help="Print a reusable Telethon StringSession for Railway variables.",
    )
    return parser


async def start_client(settings: Any) -> Any:
    try:
        from telethon import TelegramClient
        from telethon.sessions import StringSession
    except ImportError:
        print("Telethon is not installed. Run: pip install telethon")
        return None

    session: Any = settings.session_name
    if has_string_session(settings):
        session = StringSession(settings.string_session)

    client = TelegramClient(session, int(settings.api_id), settings.api_hash)
    await client.start(
        phone=settings.phone or None,
        code_callback=(lambda: settings.login_code) if settings.login_code else None,
        password=settings.password or None,
    )
    return client


async def scan_recent_messages(client: Any, settings: Any, limit: int) -> list[Any]:
    matches: list[Any] = []
    async for message in client.iter_messages(settings.source_channel, limit=limit):
        result = match_message(message.message, settings.filter_text)
        if result.matched:
            matches.append(message)
    return matches


async def run_scan(limit: int, forward_latest: bool) -> int:
    settings = load_forwarder_settings()
    missing = validate_forwarder_settings(settings)
    if missing:
        print("Missing required .env values:")
        for key in missing:
            print(f"- {key}")
        return 1

    client = await start_client(settings)
    if client is None:
        return 1

    print(f"Scanning @{settings.source_channel} for '{settings.filter_text}'")
    matches = await scan_recent_messages(client, settings, limit)

    if not matches:
        print(f"No matching posts found in the latest {limit} posts.")
        await client.disconnect()
        return 0

    newest = matches[0]
    print(f"Found {len(matches)} matching post(s) in the latest {limit} posts.")
    print(f"Latest matched message id: {newest.id}")
    preview = (newest.message or "")[:200].replace("\n", " ")
    print(f"Preview: {preview}")

    if forward_latest:
        await client.forward_messages(settings.target_channel, newest)
        print(f"Forwarded message {newest.id} to @{settings.target_channel}")
    else:
        print("Dry run only. Re-run with --forward-latest to send one matched post.")

    await client.disconnect()
    return 0


async def run_watch(dry_run: bool) -> int:
    settings = load_forwarder_settings()
    missing = validate_forwarder_settings(settings)
    if missing:
        print("Missing required .env values:")
        for key in missing:
            print(f"- {key}")
        return 1

    client = await start_client(settings)
    if client is None:
        return 1

    forwarded_ids = load_forwarded_ids(settings.state_path)
    source = await client.get_entity(settings.source_channel)

    print(f"Watching @{settings.source_channel} for '{settings.filter_text}'")
    print(f"Target channel: @{settings.target_channel}")
    print(f"Dry run: {'on' if dry_run else 'off'}")

    @client.on(__import__("telethon").events.NewMessage(chats=source))
    async def handle_new_message(event: Any) -> None:
        message = event.message
        result = match_message(message.message, settings.filter_text)
        if not result.matched:
            return
        if not should_forward(message.id, forwarded_ids):
            print(f"Skipped duplicate matched message {message.id}")
            return

        preview = result.text[:200].replace("\n", " ")
        print(f"Matched new post {message.id}: {preview}")

        if dry_run:
            forwarded_ids.add(message.id)
            save_forwarded_ids(settings.state_path, forwarded_ids)
            print(f"Recorded message {message.id} in dry-run state file.")
            return

        await client.forward_messages(settings.target_channel, message)
        forwarded_ids.add(message.id)
        save_forwarded_ids(settings.state_path, forwarded_ids)
        print(f"Forwarded message {message.id} to @{settings.target_channel}")

    await client.run_until_disconnected()
    return 0


async def run_print_string_session() -> int:
    settings = load_forwarder_settings()
    missing = validate_forwarder_settings(settings)
    if missing:
        print("Missing required .env values:")
        for key in missing:
            print(f"- {key}")
        return 1

    client = await start_client(settings)
    if client is None:
        return 1

    from telethon.sessions import StringSession

    session_string = StringSession.save(client.session)
    print("TELEGRAM_STRING_SESSION=")
    print(session_string)
    await client.disconnect()
    return 0


def main() -> None:
    args = build_parser().parse_args()
    if args.print_string_session:
        raise SystemExit(asyncio.run(run_print_string_session()))
    if args.watch:
        raise SystemExit(asyncio.run(run_watch(dry_run=args.dry_run)))
    raise SystemExit(asyncio.run(run_scan(limit=args.limit, forward_latest=args.forward_latest)))


if __name__ == "__main__":
    main()
