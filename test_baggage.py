from opentelemetry import baggage, trace, context
from opentelemetry.sdk.trace import TracerProvider
import threading
import unittest

#
# QUESTION how can I can fine tune for automatic "context key" handover? On could think of process context  a global variable?  of thread context bound that
#
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

thread_local = threading.local()


def init_thread_ctx():
    thread_local.global_ctx = baggage.set_baggage("pic", "wic")

    # Note here a new context is generated for each new baggage
    thread_local.global_ctx = baggage.set_baggage(
        "walace&", "gromit", context=thread_local.global_ctx
    )  # Bug


class TestBaggage(unittest.TestCase):
    def test_localstorage(self):
        init_thread_ctx()

        with tracer.start_span(name="root span") as root_span:
            ctx = baggage.set_baggage("foo", "bar", context={})
            global_ctx = context.get_current()

            self.assertDictEqual(
                {"pic": "wic", "walace&": "gromit"}, dict(baggage.get_all())
            )

            # print(f"Global context baggage: {baggage.get_all()}")

            self.assertDictEqual(
                {"pic": "wic", "walace&": "gromit"}, dict(baggage.get_all())
            )
            print(
                f"Global thread context baggage: {baggage.get_all(context=thread_local.global_ctx)}"
            )

        self.assertDictEqual({}, dict(baggage.get_all(thread_local.global_ctx)))

        print(f"Span context baggage: {baggage.get_all(context=ctx)}")

    def test_multithreading():
        pass
