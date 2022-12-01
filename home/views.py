from django.shortcuts import render
from products.models import Product
# Create your views here.
from django.http import HttpResponseRedirect


def index(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'home/index.html', context)



##my search, the logic
# since the input to enter our text was a form 
# i set up a form as post and gave the input a name to catch it
#in view after setting the url in urls.py and having an hmtl that looks like index
# i catch the post request
# get the value of text
# get all the items in product
# i ask that if any string of item is same as my text
# return that item and not its stirng and pass it over in context
# in my form i catch without iterating to display result

#if all else fail get me an empty search page

def search_item(request):
    if request.method == "POST":

        text = request.POST.get('text')
        print("TEXT: ", text)
        queryset = Product.objects.all()
        for itm in queryset:
            if str(itm)== text:
                print(itm)
        # if text in queryset:
        #     print(text)
        #     if text == item:
                return render(request, 'home/search.html', context={'item': itm })
        # print(queryset)

    return render(request, 'home/search.html', context={})
