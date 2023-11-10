from time import sleep
import pytest

from os import environ

from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
import opentelemetry.metrics as metrics_api
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.metrics import Meter
import random
from opentelemetry.metrics import Histogram, Counter


@pytest.fixture()
def setup():
    #  metrics setup
    otlp_endpoint = environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")
    exporter = OTLPMetricExporter(endpoint=otlp_endpoint)

    service_name = environ.get("OTEL_SERVICE_NAME", "undefined-service")
    resource = Resource(attributes={SERVICE_NAME: service_name})
    metric_reader = PeriodicExportingMetricReader(exporter=(exporter))
    metric_readers = [metric_reader]
    metric_provider = MeterProvider(metric_readers=metric_readers, resource=resource)
    metrics_api.set_meter_provider(meter_provider=metric_provider)
    meter: Meter = metric_provider.get_meter("test_meter_name")

    return (
        # meter.create_histogram(
        #     name="sandbox.metrics.test_histogram_name",
        #     unit="seconds",
        #     description="A test metric for exploring opentelemetry metrics integration with",
        # ),
        meter.create_counter(
            name="sandbox.metrics.test_counter_name",
            unit="peanuts",
            description="A test metric for counter metric",
        ),
        exporter,
        metric_reader,
    )


def test_send_metrics(setup):
    exporter: OTLPMetricExporter
    metric: Counter
    metric_reader: PeriodicExportingMetricReader
    (metric, exporter, metric_reader) = setup
    for i in range(1, 200):
        sleep(2)
        # metric.record(
        #     random.randint(0, 9),
        #     attributes={"attrt1": "ATTR1", "attr2": "ATTR2"},
        # )
        metric.add(
            random.randint(0, 9),
            attributes={"attrt1": "ATTR1", "attr2": "ATTR2"},
        )
    # exporter.force_flush() Tested impact of flushing...
    # metric_reader.force_flush()

    print("Done!")
