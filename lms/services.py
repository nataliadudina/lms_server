import stripe

from config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(course_name):
    """Создает продукт в Stripe для курса."""
    product = stripe.Product.create(
      name=course_name,
      type="service"
    )
    return product


def create_stripe_price(product_id, amount, currency='usd'):
    """Создает цену для продукта в Stripe."""
    price = stripe.Price.create(
      product=product_id,
      unit_amount=int(amount * 100),  # Stripe requires amount in cents
      currency=currency
    )
    return price


def create_stripe_checkout_session(price_id, user_email):
    """Создает сессию оплаты в Stripe."""
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:8000/payment-status/?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://127.0.0.1:8000/',
            customer_email=user_email,
        )
        return session
    except stripe.error.StripeError as e:
        print(f"Failed to create session: {e}")
        return None


def retrieve_stripe_checkout_session(session_id):
    """Проверка статуса платежа"""
    session = stripe.checkout.Session.retrieve(session_id)
    return session
