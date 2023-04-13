from __future__ import annotations

from collections import defaultdict
from typing import List

from alchemist_event_hub.batch_receiver import AbstractBatchReceiver
from azure.eventhub import EventData
from azure.eventhub.aio import EventHubConsumerClient

ENCODING = 'utf-8'


class BatchReceiver(AbstractBatchReceiver):
    def __init__(self, event_hub_consumer_client: EventHubConsumerClient) -> None:
        super().__init__(event_hub_consumer_client)

    def _get_service_code(self, event: EventData) -> str | None:
        default_service_code = '$twin.tags.serviceCode'
        service_code = str(event.properties.get('service-code'.encode(ENCODING), default_service_code), ENCODING)
        if service_code == default_service_code:
            return None
        return service_code

    def _get_data_partition_id(self, event: EventData) -> str | None:
        default_data_partition_id = '$twin.tags.dataPartitionId'
        data_partition_id = str(
            event.properties.get('data-partition-id'.encode(ENCODING), default_data_partition_id), ENCODING
        )
        if data_partition_id == default_data_partition_id:
            return None
        return data_partition_id

    def _get_sink_location(self, event: EventData) -> str | None:
        service_code = self._get_service_code(event)
        data_partition_id = self._get_data_partition_id(event)

        if service_code and data_partition_id:
            return service_code + '_' + data_partition_id
        else:
            return None

    async def _process_event_batch(self, events: List[EventData]) -> None:
        # TODO: remove debug log
        print("Received count: {}".format(len(events)))

        dict = defaultdict(list)
        for event in events:
            sink_location = self._get_sink_location(event)
            if sink_location:
                dict[sink_location].append(event)

        for k, v in dict.items():
            # TODO: remove debug log and add writing to sink database logic here
            print("Writing to {} with {} events".format(k, len(v)))
