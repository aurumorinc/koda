import sentry_sdk
from koda.config.main import settings

def init_sentry() -> None:
    """Initialize Sentry and tag events with the current OTel trace_id."""
    sentry_dsn = getattr(settings, "sentry_dsn", None)
    if not sentry_dsn:
        return

    sentry_sdk.init(
        dsn=sentry_dsn,
        send_default_pii=True,
        traces_sample_rate=1.0,
    )

    # Tag all subsequent Sentry events in this process with the Windmill trace_id
    trace_id = settings.trace_id
    if trace_id:
        sentry_sdk.set_tag("trace_id", trace_id)
