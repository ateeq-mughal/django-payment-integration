# from django.test import TestCase

# Create your tests here.
import stripe

# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
stripe.api_key = 'sk_test_51Ja1P3BUeFQdhI0D2vEozHcwjrlbqTziXmNLOMgVbKg0TceF8BoeHlYnPIhMYU8NNFQzeiE2AD7m7MIgda4LlW4v00ZBXLgrR4'

product = stripe.Product.update('{{prod_KGTEa91mxijIql}}',tax_code='txcd_10000000',)

stripe.Subscription.modify(
  "sub_1JjnxxBUeFQdhI0DOL3ie2R1",
  automatic_tax={"enabled": True},
)
