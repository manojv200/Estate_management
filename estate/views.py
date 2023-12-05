from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import auth
from.models import *
BASE_DIR = settings.BASE_DIR
import requests
# Create your views here.

def index_page(request):
    return render(request,'index.html')
@csrf_exempt
def admin_login(request):
    try:
        data = request.POST
        username = data['username']
        password = data['password']
        if User.objects.filter(email=username).count() > 0 :
            obj=User.objects.get(email=username)
            print(obj)
            if obj and obj.is_superuser:
                print('jjjjjjjjjjj')
                if obj.check_password(password):
                    auth.login(request,obj)
                    msg='success'
                    otp='ok'
                    user_id = obj.id
                    res={
               'msg':msg,'otp':otp,'userId':user_id,
           }
                    
                else:
                    msg="Invalid  password"
                    res={'msg':msg}
                    print(res)
                    user_id = obj.id
            else:
                msg = "User is not admin"
        return redirect('/home_page')
    except Exception as e:
        print(str(e))
        return HttpResponse(status =404)
    
# @login_required
def home_page(request):
    opencage_api_key = 'e864c71e2c524bb4b68a6ec4edcaf494'  # Replace with your API key
    property = Property.objects.all()
    unit = Unit.objects.all()
    Tenants = Tenant.objects.all()
    context ={}
    context['property']= property
    context['tenant']= Tenants
    context['unit']= unit
    for prop in property:
        coordinates = prop.location
        cord = coordinates.split(',')
        late = float(cord[0])
        long = float(cord[1])
        base_url = "https://api.opencagedata.com/geocode/v1/json"
        params = {
        'key': opencage_api_key,
        'q': f"{late},{long}",
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if 'results' in data and data['results']:
            result = data['results'][0]
            formatted_address = result.get('formatted', 'N/A')
        prop.location = formatted_address

    return render(request,'home.html',context=context)

@csrf_exempt
def add_property(request):
    opencage_api_key = 'e864c71e2c524bb4b68a6ec4edcaf494'  # Replace with your API key
    if request.method == 'POST':
        try:
            if 'v' in request.POST:
                p_id = request.POST.get('id')
                p_name = request.POST.get('p_name')
                address = request.POST.get('address')
                u_name = request.POST.get('u_name')
                type = request.POST.get('type')
                rent = request.POST.get('rent')
                place_name = request.POST['location']
               
                print(request.POST)
                base_url = "https://api.opencagedata.com/geocode/v1/json"
                params = {
                'key': opencage_api_key,
                'q': place_name,
                'limit': 1  # Limit to one result
            }

                response = requests.get(base_url, params=params)
                data = response.json()
                print(data)
                if 'results' in data and data['results']:
                    result = data['results'][0]
                    geometry = result['geometry']
                    lat, lng = geometry['lat'], geometry['lng']
                    Property.objects.filter(id=p_id).update(name=p_name,address=address,location=str(lat)+','+str(lng))
                    Unit.objects.filter(property=p_id).update(unit_name=u_name,type=type,rent_cost=rent)
                    return JsonResponse({'msg':'success'})
                else:
                    return JsonResponse({'error': 'Coordinates not found for the specified place name'}, status=400)
            else:
                print(request.POST)
                p_name = request.POST.get('p_name')
                address = request.POST.get('address')
                feature = request.POST.get('features')
                place_name = request.POST.get('location')
                u_name = request.POST.get('u_name')
                rent = request.POST.get('rent_cost')
                type = request.POST.get('type')
            
           

                base_url = "https://api.opencagedata.com/geocode/v1/json"
                params = {
                'key': opencage_api_key,
                'q': place_name,
                'limit': 1  # Limit to one result
            }

                response = requests.get(base_url, params=params)
                data = response.json()
                print(data)
                if 'results' in data and data['results']:
                    result = data['results'][0]
                    geometry = result['geometry']
                    lat, lng = geometry['lat'], geometry['lng']
                    prop = Property.objects.create(name=p_name,address=address,location=str(lat)+','+str(lng))
                    Unit.objects.create(unit_name = u_name,rent_cost=rent,type = type,property=prop)

                    return JsonResponse({'msg':'success'})
                else:
                    return JsonResponse({'error': 'Coordinates not found for the specified place name'}, status=400)
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'form.html')
@csrf_exempt
def add_tenant(request):
    if request.method == 'POST':
        try:
            print(request.POST)

            t_name = request.POST['t_name']
            contact_number = request.POST['c_num']
            doc = request.FILES['doc']
            doc_name = doc.name
            agre_end_date = request.POST['agre_end_date']
            mon_rent_date = request.POST['mon_rent_date']
            as_prop = request.POST['as_prop']
            document = DocumentProof.objects.create(proof_name=doc_name,document=doc)
            Tenant(name=t_name,contact_number=contact_number,agreement_end_date=agre_end_date,monthly_rent_date=mon_rent_date,document_proof=document,property=as_prop).save()

            
            return JsonResponse({'msg':'success'})
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': str(e)}, status=500)


def view_prop(request,prop_id):
   print(prop_id)
   property = Property.objects.get(id = prop_id)
   unit = Unit.objects.get(property = prop_id)
   prop_name = property.name
   tenant = Tenant.objects.get(property=prop_name)
   context={}
   context['property'] = property
   context['unit'] = unit
   context['tenant'] = tenant
   return render(request,'prop_list.html',context=context)

def view_ten(request,ten_id):
   print(ten_id)
   tenant = Tenant.objects.get(id = ten_id)
   
   print(tenant.property)
   prop = Property.objects.get(name=tenant.property)
   prop_id = prop.id
   unit = Unit.objects.get(property = prop_id)
   context={}
   context['unit'] = unit
   context['tenant'] = tenant
   return render(request,'ten_list.html',context=context)

def del_prop(request,prop_id):
   try:
       print(prop_id)
       property = Property.objects.get(id = prop_id)
       unit = Unit.objects.get(property = prop_id)
       property.delete()
       unit.delete()
       return redirect('/home_page')
   except Exception as e:
       print(str(e))
       return HttpResponse(status = 404)
def del_ten(request,ten_id):
   try:
       print(ten_id)
       tenant = Tenant.objects.get(id = ten_id)
    #    unit = Unit.objects.get(property = prop_id)
       tenant.delete()
    #    unit.delete()
       return redirect('/home_page')
   except Exception as e:
       print(str(e))
       return HttpResponse(status = 404)
   

def user_logout(request):
	logout(request)
	return redirect('/')






