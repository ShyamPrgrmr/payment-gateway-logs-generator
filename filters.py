import logging

import threading
import uuid

_context = threading.local()

def set_context():
    _context.paymentId = f"pay_{uuid.uuid4().hex[:8]}"
    _context.accountId = f"acc_{uuid.uuid4().hex[:6]}"
    _context.merchantId = f"mer_{uuid.uuid4().hex[:6]}"

def get_context():
    return (
        getattr(_context, "paymentId", "-"),
        getattr(_context, "accountId", "-"),
        getattr(_context, "merchantId", "-")
    )

class MDCFilter(logging.Filter):
    def filter(self, record):
        paymentId, accountId, merchantId = get_context()
        record.paymentId = paymentId
        record.accountId = accountId
        record.merchantId = merchantId
        record.traceId = getattr(record, "traceId", "-")
        record.spanId = getattr(record, "spanId", "-")
        return True