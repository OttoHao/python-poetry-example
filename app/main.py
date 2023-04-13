import os

from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore
from services.receiver import BatchReceiver


# TODO: this is duplicated with emb-databricks provider
def get_event_hub_consumer_client() -> EventHubConsumerClient:
    blob_storage_connection_string = os.environ.get("EVENT_HUB_BLOB_STORAGE_CONNECTION_STRING", "")
    blob_container_name = os.environ.get("EVENT_HUB_BLOB_CONTAINER_NAME", "")
    event_hub_connection_str = os.environ.get("EVENT_HUB_CONNECTION_STR", "")
    event_hub_name = os.environ.get("EVENT_HUB_NAME", "")
    consumer_group = os.environ.get("EVENT_HUB_CONSUMER_GROUP", "")

    checkpoint_store = BlobCheckpointStore.from_connection_string(  # type: ignore
        conn_str=blob_storage_connection_string, container_name=blob_container_name
    )
    return EventHubConsumerClient.from_connection_string(
        event_hub_connection_str,
        consumer_group=consumer_group,
        eventhub_name=event_hub_name,
        checkpoint_store=checkpoint_store,
    )


def main() -> None:
    event_hub_consumer_client = get_event_hub_consumer_client()
    BatchReceiver(event_hub_consumer_client=event_hub_consumer_client).run()


if __name__ == "__main__":
    main()
