from django.shortcuts import render
from django.http import HttpResponse
import json
import random
import os.path
BASE = os.path.dirname(os.path.abspath(__file__))

from . import add_random_passenger
from .backend.seating_plan import get_seat_plan
from . import similarity

def index(request):
    return HttpResponse("Hello, world. You're at the api index.")



def init(request):
    """ 
        Remove all data & seating plan
    """
    with open(os.path.join(BASE, 'data.json'), 'w') as f:
        json.dump([], f)
    with open(os.path.join(BASE, 'plan.json'), 'w') as f:
        json.dump([], f)
    return HttpResponse("All data removed.")


#######################################################################################
#
#    Preference
#
#######################################################################################

def pref(request):

    DEFAULT_WEIGHT = {1:1, 2:0}
    NOT_SET = 0

    in_f =  open(os.path.join(BASE, 'data.json'), 'r')
    data = json.load(in_f)
    in_f.close()
    
    existed = False
    for item in data:
        if item['Name'] == request.GET.get('Name', 'NA'):
            existed = True
    
    if not existed:
        data.append({
            'Name':request.GET.get('Name', 'NA'),
            'Preferences':{
                'Window':int(request.GET.get('Window', NOT_SET)),
                'Sleep':int(request.GET.get('Sleep', NOT_SET)),
                'Networking':int(request.GET.get('Networking', NOT_SET)),
                'WindowShading':int(request.GET.get('WindowShading', NOT_SET)),
            },
            'Weights':{
                'Window': DEFAULT_WEIGHT,
                'Sleep': DEFAULT_WEIGHT,
                'Networking': DEFAULT_WEIGHT,
                'WindowShading': DEFAULT_WEIGHT,
            }
        })
        
        with open(os.path.join(BASE, 'data.json'), 'w') as out_f:
            json.dump(data, out_f, sort_keys=True, indent=4)

    return render(request, 'pref.html', context={'Key':'Value'})
    #return HttpResponse("ok")



#######################################################################################
#
#    Feedback
#
#######################################################################################


def feedback(request):
    return HttpResponse("ok")


#######################################################################################
#
#    Final Seating
#
#######################################################################################

def finalseating(request):
    in_f =  open(os.path.join(BASE, 'data.json'), 'r')
    data = json.load(in_f)
    in_f.close()

    plan = [get_seat_plan(data)]
    with open(os.path.join(BASE, 'plan.json'), 'w') as out_f:
            json.dump(plan, out_f, sort_keys=True, indent=4)

    return HttpResponse('ok')
    

#######################################################################################
#
# Demo-use: The 200th passenger should be highlighted in the demo picture.
#
#######################################################################################

def random199(request):
    
    HIGHLIGHTED = 200

    passenger =[]
    for i in range(HIGHLIGHTED-1):
        add_random_passenger.add_random_passenger(passenger)
    with open(os.path.join(BASE, 'data.json'), 'w') as out_f:
            json.dump(passenger, out_f, sort_keys=True, indent=4)
    return HttpResponse(passenger)
    

def result(request):

    HIGHLIGHTED = 200

    finalseating(request)
    ret = similarity.visualize(HIGHLIGHTED)
    return HttpResponse(ret)
