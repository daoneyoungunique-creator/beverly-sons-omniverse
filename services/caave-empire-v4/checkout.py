"""Stripe hosted checkout: private server-side invocation only."""
import os
import stripe

def create_checkout(asset, *, asset_id, success_url=None, cancel_url=None):
    secret = os.getenv("STRIPE_SECRET_KEY")
    if not secret:
        raise RuntimeError("STRIPE_SECRET_KEY not configured")
    success_url = success_url or os.getenv("CAAVE_SUCCESS_URL")
    cancel_url = cancel_url or os.getenv("CAAVE_CANCEL_URL")
    if not success_url or not cancel_url or not all(u.startswith("https://") for u in (success_url,cancel_url)):
        raise ValueError("HTTPS success and cancel URLs required")
    if not isinstance(asset["price_cents"], int) or asset["price_cents"] <= 0:
        raise ValueError("Invalid price")
    stripe.api_key = secret
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[{"price_data":{"currency":"usd",
          "unit_amount":asset["price_cents"],
          "product_data":{"name":asset["title"]}},"quantity":1}],
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={"caave_asset_id":asset_id},
    )
    return {"checkout_url":session.url,"session_id":session.id}
