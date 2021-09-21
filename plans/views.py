from django.shortcuts import render, get_object_or_404, redirect
from .forms import CustomSignupForm
from django.urls import reverse_lazy
from django.views import generic
from .models import TechBlogs, Customer
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
import stripe
from django.http import HttpResponse



plan = 'basic'
coupon = 'none'
price = 2500
og_dollar = 25
coupon_dollar = 0
final_dollar = 25


stripe.api_key = 'sk_test_51Ja1P3BUeFQdhI0D2vEozHcwjrlbqTziXmNLOMgVbKg0TceF8BoeHlYnPIhMYU8NNFQzeiE2AD7m7MIgda4LlW4v00ZBXLgrR4'

# Create your views here.

def home(request):
    plans = TechBlogs.objects
    return render(request, 'plans/home.html', {'plans':plans})

def plan(request,pk):
    plan = get_object_or_404(TechBlogs, pk=pk)
    if plan.premium:
        if request.user.is_authenticated:
            try:
                if request.user.customer.membership:
                        return render(request, 'plans/plan.html', {'plan':plan})
            except Customer.DoesNotExist:
                    return redirect('join')

        return redirect('join')
    else:
        return render(request, 'plans/plan.html', {'plan':plan})

def join(request):
    return render(request, 'plans/join.html')

@login_required
def checkout(request):
    
    try:
        if request.user.customer.membership:
            return redirect('settings')
    except Customer.DoesNotExist:
        pass

    coupons = {'welcome':10, 'cheema':50}

    if request.method == 'POST':
        stripe_customer = stripe.Customer.create(email=request.user.email, source=request.POST['stripeToken'])
        plan = 'price_1Ja5uYBUeFQdhI0Dj7rrVUHx'
        
        if request.POST['plan'] == 'gold':
            plan = 'price_1Ja5v3BUeFQdhI0DduxX12y5'

        if request.POST['plan'] == 'gold yearly':
            plan = 'price_1Ja5vMBUeFQdhI0DUey2gGcK'
        
        if request.POST['coupon'] in coupons:
            percentage = coupons[request.POST['coupon'].lower()]
            try:
                coupon = stripe.Coupon.create(duration='once', id=request.POST['coupon'].lower(), percent_off=percentage)
            except:
                pass
            subscription = stripe.Subscription.create(customer=stripe_customer.id, items=[{'plan':plan}], coupon=request.POST['coupon'].lower())

        else:
            subscription = stripe.Subscription.create(customer=stripe_customer.id, items=[{'plan':plan}])

        customer = Customer()
        customer.user = request.user
        customer.stripeid = stripe_customer.id
        customer.membership = True
        customer.cancel_at_period_end = False
        customer.stripe_subscription_id = subscription.id
        customer.save()


        return redirect('home')
    else:
        plan = 'basic'
        coupon = 'none'
        price = 2500
        og_dollar = 25
        coupon_dollar = 0
        final_dollar = 25
        if request.method == 'GET' and 'plan' in request.GET:
            if request.GET['plan'] == 'gold':
                plan = 'gold'
                price = 5000
                og_dollar = 50
                final_dollar = 00
            if request.GET['plan'] == 'gold yearly':
                plan = 'gold yearly'
                price = 50000
                og_dollar = 500
                final_dollar = 500
        
        if request.method == 'GET' and 'coupon' in request.GET:
            if request.GET['coupon'].lower() in coupons:
                coupon = request.GET['coupon'].lower()
                percentage = coupons[coupon]
                coupon_price = int((percentage / 100) * price)
                price -= coupon_price
                coupon_dollar = str(coupon_price)[:-2] + "." + str(coupon_price)[-2:]
                final_dollar = str(price)[:-2] + "." + str(price)[-2:]
        return render(request, 'plans/checkout.html', {'plan':plan, 'coupon':coupon, 'price':price, 'og_dollar':og_dollar, 'coupon_dollar':coupon_dollar, 'final_dollar':final_dollar})



@login_required
def checkout_sepa(request):
    global plan, coupon, price, og_dollar, coupon_dollar, final_dollar

    coupons = {'welcome':10, 'cheema':50}

    
    try:
        if request.user.customer.membership:
            return redirect('settings')
    except Customer.DoesNotExist:
        pass

    coupons = {'welcome':10, 'cheema':50}


    if request.method == 'POST':
        print("YAYYYYYYYYYYYY DEKHHHH", dict(request.POST))

        plan = 'price_1JbwHHBUeFQdhI0DOhDF6JwK'

        if request.POST['plan'] == 'gold':
            plan = 'price_1JbwHVBUeFQdhI0DO5yYzRSP'

        if request.POST['plan'] == 'gold yearly':
            plan = 'price_1JbwHtBUeFQdhI0DPZnqjnje'


        source = stripe.Source.create(
        type='sepa_debit',
        sepa_debit={'iban': request.POST['iban']},
        currency='eur',
        owner={'name': request.POST['name'],},)

        stripe_customer_sepa = stripe.Customer.create(
                                                        email=request.user.email, 
                                                        source=source,)
        
        if request.POST['coupon'] in coupons:
            percentage = coupons[request.POST['coupon'].lower()]

            try:
                coupon = stripe.Coupon.create(duration='once', id=request.POST['coupon'].lower(), percent_off=percentage)
            except:
                pass
            subscription = stripe.Subscription.create(customer=stripe_customer_sepa.id, items=[{'plan':plan}], coupon=request.POST['coupon'].lower())

        else:
            subscription = stripe.Subscription.create(customer=stripe_customer_sepa.id, items=[{'plan':plan}])
        
        customer = Customer()
        customer.user = request.user
        customer.stripeid = stripe_customer_sepa.id
        customer.membership = True
        customer.cancel_at_period_end = False
        customer.stripe_subscription_id = subscription.id
        customer.save()
    
        return redirect('home')
    
    else:
        
        plan = 'basic'
        coupon = 'none'
        price = 1000
        og_dollar = 10
        coupon_dollar = 0
        final_dollar = 10
        if request.method == 'GET' and 'plan' in request.GET:
           if request.GET['plan'] == 'gold':
               plan = 'gold'
               price = 2000
               og_dollar = 20
               final_dollar = 20
           if request.GET['plan'] == 'gold yearly':
                plan = 'gold yearly'
                price = 5000
                og_dollar = 50
                final_dollar = 50
        
        if request.method == 'GET' and 'coupon' in request.GET:
            if request.GET['coupon'].lower() in coupons:
                coupon = request.GET['coupon'].lower()
                percentage = coupons[coupon]
                coupon_price = int((percentage / 100) * price)
                price -= coupon_price
                coupon_dollar = str(coupon_price)[:-2] + "." + str(coupon_price)[-2:]
                final_dollar = str(price)[:-2] + "." + str(price)[-2:]
        return render(request, 'plans/checkout_sepa.html', {'plan':plan, 'coupon':coupon, 'price':price, 'og_dollar':og_dollar, 'coupon_dollar':coupon_dollar, 'final_dollar':final_dollar})



def settings(request):

    membership = False
    cancel_at_period_end = False

    if request.method == 'POST':
        subscription = stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)
        subscription.cancel_at_period_end = True
        request.user.customer.cancel_at_period_end = True
        subscription.save()
        request.user.customer.save()

    else:

        try:
            if request.user.customer.membership:
                membership = True

            if request.user.customer.cancel_at_period_end:
                cancel_at_period_end = True
        
        except Customer.DoesNotExist:
            membership = False

    return render(request, 'registration/settings.html', {'membership':membership, 'cancel_at_period_end':cancel_at_period_end})


@user_passes_test(lambda u: u.is_superuser)
def updateaccounts(request):
    customers = Customer.objects.all()
    for customer in customers:
        subscription = stripe.Subscription.retrieve(customer.stripe_subscription_id)
        if subscription.status != 'active':
            customer.membership = False
        else:
            customer.membership = True
        
        customer.cancel_at_period_end = subscription.cancel_at_period_end
        customer.save()

        return HttpResponse('completed')



class SignUp(generic.CreateView):
    form_class = CustomSignupForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        valid = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid
