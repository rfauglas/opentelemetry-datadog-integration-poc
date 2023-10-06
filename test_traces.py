import pytest
from os import environ

from opentelemetry import trace

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, SERVICE_VERSION, Resource
from opentelemetry.trace import (
    get_tracer,
    Span,
    SpanKind,
    StatusCode,
    types,
)
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SpanExporter,
    SpanExportResult,
)
from opentelemetry.sdk.trace import TracerProvider


@pytest.fixture()
def exporter():
    #  trace setup
    service_name = environ.get("OTEL_SERVICE_NAME", "undefined-service")
    service_version = environ.get("OTEL_SERVICE_VERSION", "undefined-version")
    resource = Resource(
        attributes={SERVICE_NAME: service_name, SERVICE_VERSION: service_version}
    )
    exporter_endpoint = environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")
    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=exporter_endpoint)
    processor = BatchSpanProcessor(exporter)

    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    return exporter


def test_send_trace(
    exporter: OTLPSpanExporter,
):  # initially used to flush but useless...
    tracer = get_tracer(__name__)

    with tracer.start_as_current_span(
        "opentelemetry-poc-span-nmae", kind=SpanKind.SERVER
    ) as span:
        print("Done!")
        span.end()
