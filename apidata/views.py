from django.shortcuts import render
import requests
import pandas as pd
from django.http import HttpResponse
import csv

# Create your views here.

def index(request):

    #if request.method == "POST":   

    def get_var_dict(var_list):
        vars = {}
        for var in var_list:
            vars[var] = request.GET.get(f'{var}')
            if vars[var] == None:
                vars[var] = ''
        return vars
    
    filter_list = ['location', 'name', 'sort', 'limit', 'amenity', 'csv']
    filters=get_var_dict(filter_list)

    print()
    print(filters['location'])

    url = 'https://hosteldata.herokuapp.com/json?' + '&'.join([(f + f'={filters[f]}') for f in filters if filters[f]!=''])
    print(url)

    hostels_json = requests.get(url).json()
    hostels = [dict(hostels_json[hostel]) for hostel in hostels_json]
    print(f'{len(hostels)} hostels returned')

    if filters['csv'] == 'true':
        hostels_df = pd.read_json(requests.get(url).text, orient='index')
        csv = hostels_df.to_csv()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename="hosteldata.csv"'
        response.write(csv)

        return response

    

    message = f"Returned the top {len(hostels)} hostels "
    if filters['amenity'] != '':
        message += f"with {filters['amenity']} "
    if filters['location'] != '':
        message += f"in {filters['location']} "
    if filters['sort'] != '':
        message += f"sorted by {filters['sort']} "
    else: 
        message += "sorted by rating "
    print(message)

    context = filters.copy()
    context['message'] = message
    context['hostels'] = hostels

    print(context['location'])


    return render(request, "apidata/index.html", context)

def get_csv(request):
    def get_var_dict(var_list):
        vars = {}
        for var in var_list:
            vars[var] = request.GET.get(f'{var}')
            if (vars[var] == None) & (var != 'limit'):
                vars[var] = ''
            elif (vars[var] == None) & (var == 'limit'):
                vars[var] = 50
        return vars
    
    filter_list = ['location', 'name', 'sort', 'amenity', 'limit']
    filters=get_var_dict(filter_list)

    url = 'https://hosteldata.herokuapp.com/json?' + '&'.join([(f + f'={filters[f]}') for f in filters if filters[f]!=''])
    
    hostels_df = pd.read_json(requests.get(url).text, orient='index')
    csv = hostels_df.to_csv()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="hosteldata.csv"'
    response.write(csv)

    return response