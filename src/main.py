import os
import asyncio
import logging

import photonpump
from photonpump.exceptions import SubscriptionCreationFailed

import config
from bigquery_writer import BigQueryWriter
from handler import EventHandler


async def setup_subscription(conn, stream, subscription):
    try:
        await conn.create_subscription(
            subscription,
            stream,
            start_from=0
        )
    except SubscriptionCreationFailed as exn:
        logging.info(exn)

    return await conn.connect_subscription(
        subscription,
        stream
    )


async def events_actor(subscription, event_types):
    handler = get_event_handler(event_types)

    async for e in subscription.events:
        try:
            logging.info(
                'Processing event: %s, %s, %s, %s',
                e.event.type,
                e.event.id,
                e.event.event_number,
                e.event.created
            )

            handler.handle_event(e.event)


        finally:
            await subscription.ack(e)


def get_event_handler(event_types):
    writer = BigQueryWriter(os.environ.get('BIGQUERY_DATASET'), event_types)
    writer.begin()
    return EventHandler(writer, event_types)


async def run(cfg):
    async with photonpump.connect(host=cfg['host'],
                                  port=cfg['port'],
                                  username=cfg['username'],
                                  password=cfg['password']) as conn:
        logging.info('Connected to EventStore')
        actions = []

        for stream in cfg['streams']:

            try:
                subscription = await setup_subscription(conn, stream['name'], cfg['subscription'])
                logging.info(
                    "Created subscriptions %s", subscription
                )
            except Exception as exn:
                logging.error(
                    "Failed while connecting to subscriptions: %s \n sleeping before exit",
                    exn,
                    exc_info=True
                )

                return

            actions.append(events_actor(subscription, stream['events']))

        return await asyncio.gather(*actions)


def main(env):
    config.configure_logging(env)
    eventstore_cfg = config.get_eventstore_config(env)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(eventstore_cfg))


if __name__ == '__main__':
    main(os.environ)
