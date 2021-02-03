from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages

# Create your views here.

def home(request):
    import requests
    import json
    api_token = 'pk_a328e5c9b74f46e290c4954c27bda282'
    quote = 'aapl'
    error = False
    if request.method == 'POST':
        quote = request.POST.get('quote', '')
        api_url = 'https://cloud.iexapis.com/stable/stock/{}/quote?token={}'.format(quote,api_token)
        try:
            api_request = requests.get(api_url).content
            api = json.loads(api_request)
            obj, created = Stock.objects.get_or_create(quote=quote)

        except Exception as e:
            api = 'Error {}'.format(api_request)
            error = api.strip()
        ctx = {'api':api, 'error': error}
        return render(request, 'home.html', ctx)
    else:
        return render(request,'home.html', {})


def about(request):
    ctx = {}
    return render(request, 'about.html', ctx)

#just to add something
def add_stock(request):
    import requests
    import json
    api_token = 'pk_a328e5c9b74f46e290c4954c27bda282'
    quotes = Stock.objects.all().order_by('quote')

    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            #print("If check:",request.POST.get('quote') in list(quotes))
            quotes_set = set([item[0] for item in quotes.values_list('quote')])
            if not (request.POST.get('quote') in quotes_set):
            #print(quotes_set)
                form.save()
                #quotes.update()

            else:
                messages.error(request, 'This quote already exists in the database')
    else:
        form = StockForm()

    api_data = {}
    for item in quotes:
        quote = item.quote
        api_url = 'https://cloud.iexapis.com/stable/stock/{}/quote?token={}'.format(quote,api_token)
        api_request = requests.get(api_url).content

        try:
            api = json.loads(api_request)
        except:
            api = {}
        api_data[item] = api
        #print(api)


    ctx = {'form':form, 'api_data': api_data }
    return render(request, 'add_stock.html', ctx)

def delete_stock(request, quote_id):
    #print(quote_id)
    item = Stock.objects.get(pk=quote_id)
    item.delete()
    #print(request.GET)
    return redirect('add_stock')
