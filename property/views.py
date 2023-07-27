from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from account.visitor import Visitor
from .models import Property, PropertyImage, PropertyWishList, LocationSearchTracking
from .forms import PropertyAddressForm, PropertyFeatureForm, PropertyPriceForm, PropertyUploadForm, ImageInlineFormset, EmailForm
from .utils import get_location_coordinates
from notification.models import Notification


def search_by_location(request):
    location = request.GET.get('location')
    sale = request.GET.get('sale')
    let = request.GET.get('let')
    qs = Property.location.filter_by_loaction(location)
    if sale:
        qs = qs.filter(for_sale=True)
    if let:
        qs = qs.filter(for_sale=False)
    try:
        search_loacation = LocationSearchTracking.objects.get(location__iexact=location)
        search_loacation.increment_count()
    except LocationSearchTracking.DoesNotExist:
        search_loacation = LocationSearchTracking.objects.create(location=location, search_count=1)
    
    context = {'qs': qs, 'location': location}
    return render(request, 'property/search-result.html', context)


def sort_by(request):
    location = request.GET.get("q")
    sort_by = request.GET.get('sort-by')
    if sort_by == '1':
        qs = Property.location.filter_by_loaction(location).order_by('-property_price__price')
    elif sort_by == '2':
        qs = Property.location.filter_by_loaction(location).order_by('property_price__price')
    elif sort_by == '3':
        qs = Property.location.filter_by_loaction(location).order_by('-added_at')
    elif sort_by == '4':
        qs = Property.location.filter_by_loaction(location).order_by('added_at')
    else:
        qs = Property.location.filter_by_loaction(location)
    context = {'qs': qs}
    return render(request, 'property/partials/sort-result.html', context)


def filter_search(request):
    location = request.GET.get("q")
    min_price = request.GET.get('minPrice')
    max_price = request.GET.get('maxPrice')
    min_beds = request.GET.get('minBeds')
    max_beds = request.GET.get('maxBeds')
    property_type = request.GET.get('propertyType')

    qs = Property.location.filter_by_loaction(location)
    filter_conditions = Q()

    if min_price:
        filter_conditions &= Q(property_price__price__gt=min_price)
    if max_price:
        filter_conditions &= Q(property_price__price__lte=max_price)
    if min_beds:
        filter_conditions &= Q(property_feature__bedroom__gte=min_beds)
    if max_beds:
        filter_conditions &= Q(property_feature__bedroom__lt=max_beds)
    if property_type:
        filter_conditions &= Q(property_feature__property_type__iexact=property_type)
    
    qs = qs.filter(filter_conditions)

    context = {'qs': qs}
    return render(request, 'property/partials/sort-result.html', context)


def property_detail_view(request, pk):
    property_obj = Property.location.get(pk=pk)
    property_obj.views_count += 1
    property_obj.save()
    if request.user.is_authenticated:
        try:
            wishlist_property = PropertyWishList.objects.get(user_id=request.user.id, property=property_obj)
        except:
            wishlist_property = None
        if wishlist_property is not None:
            liked = True 
        else:
            liked = False
    else:
        user = Visitor(request)
        if user.check_liked_status(pk):
            liked = True 
        else:
            liked = False
    context = {'obj': property_obj, 'liked': liked}
    return render(request, 'property/property-detail.html', context)


def show_on_map(request, pk):
    property_obj = Property.location.get(pk=pk)
    address = property_obj.property_address
    api_key = settings.GOOGLE_MAP_API_KEY
    location_coor = get_location_coordinates(address, api_key)
    response = {
        'api_key': api_key,
        'location_coor': location_coor,
        'property_id': pk,
    }
    return JsonResponse(response)


@login_required
def property_upload_view(request):
    if request.method == 'POST':
        address_form = PropertyAddressForm(request.POST)
        feature_form = PropertyFeatureForm(request.POST)
        price_form = PropertyPriceForm(request.POST)
        property_upload_form = PropertyUploadForm(request.POST)
        formset = ImageInlineFormset(request.POST, request.FILES, queryset=None)
        
        if address_form.is_valid() and feature_form.is_valid() and price_form.is_valid() and property_upload_form.is_valid() and formset.is_valid():
            property_obj = property_upload_form.save(commit=False)
            property_obj.owner = request.user
            property_obj.save()
            address = address_form.save(commit=False)
            address.property = property_obj
            address.save()
            feature = feature_form.save(commit=False)
            feature.property = property_obj
            feature.save()
            price = price_form.save(commit=False)
            price.property = property_obj
            price.save()
        
            for _form in formset:
                if _form.has_changed():
                    img = _form.save(commit=False)
                    img.property = property_obj
                    img.save()

            return redirect('index')
    else:
        address_form = PropertyAddressForm()
        feature_form = PropertyFeatureForm()
        price_form = PropertyPriceForm()
        property_upload_form = PropertyUploadForm()
        formset = ImageInlineFormset(queryset=PropertyImage.objects.none())
        
    context = {
        'address_form': address_form,
        'feature_form': feature_form,
        'price_form': price_form,
        'property_upload_form': property_upload_form,
        'formset': formset
    }
    return render(request, 'property/property-upload.html', context)


@login_required
def update_property_detail_view(request, pk=None):
    property_obj = get_object_or_404(Property, pk=pk)
    image_qs = PropertyImage.objects.filter(property=property_obj)
    address_form = PropertyAddressForm(request.POST or None, instance=property_obj.property_address)
    feature_form = PropertyFeatureForm(request.POST or None, instance=property_obj.property_feature)
    price_form = PropertyPriceForm(request.POST or None, instance=property_obj.property_price)
    property_upload_form = PropertyUploadForm(request.POST or None, instance=property_obj)
    image_formset = ImageInlineFormset(request.POST or None, request.FILES or None, queryset=image_qs)

    if address_form.is_valid() and feature_form.is_valid() and price_form.is_valid() and property_upload_form.is_valid() and image_formset.is_valid():
        address = address_form.save(commit=False)
        property_obj.property_address = address
        address.save()

        feature = feature_form.save(commit=False)
        property_obj.property_feature = feature
        feature.save()

        price = price_form.save(commit=False)
        property_obj.property_price = price
        price.save()
    
        updated_obj = property_upload_form.save(commit=False)
        property_obj = updated_obj
        property_obj.save()

        image_formset.save(commit=False)
        for _form in image_formset:
            if _form.has_changed():
                is_delete = _form.cleaned_data.get("DELETE")
                try:     
                    img_obj = _form.save(commit=False)
                except:
                    img_obj = None
                if is_delete:
                    if img_obj is not None:
                        if img_obj.pk:
                            img_obj.delete()
                else:
                    if img_obj is not None:
                        img_obj.property = property_obj
                        img_obj.save()
                        messages.success(request, 'data updated')
        return redirect(reverse('property:update-property', kwargs={'pk': property_obj.pk }))

    context = {
        'property_obj': property_obj,
        'address_form': address_form,
        'feature_form': feature_form,
        'price_form': price_form,
        'property_upload_form': property_upload_form,
        'image_formset': image_formset
    }

    return render(request, 'property/property-update.html', context)


@csrf_exempt
def update_wishlist(request, pk):
    property_obj = Property.objects.get(pk=pk)
    if request.user.is_authenticated:
        try:
            saved_obj = PropertyWishList.objects.get(user=request.user.id, property=property_obj)
        except:
            saved_obj = None

        if saved_obj is None:
            saved_obj = PropertyWishList.objects.create(user_id=request.user.id, property=property_obj)
            response = {'liked': True}
        else:
            saved_obj.delete()
            response = {'liked': False}
    else:
        user = Visitor(request)
        if user.add_or_remove_liked_property(pk):
            response = {'liked': True}
        else:
            response = {'liked': False}
    return JsonResponse(response)


def email_owner(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    send_to = property_obj.owner.email
    sender = request.user.email
    default_subject = f"Regard to property on {property_obj.property_address}"
    initial= {'email_from': sender, 'send_to': send_to, 'subject': default_subject}
    form = EmailForm(request.POST or None, initial=initial)
    
    if form.is_valid():
        send_to = form.cleaned_data['send_to']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        send_mail(subject=subject, message=message, from_email=sender, recipient_list=[send_to])
        msg = f"Someone sent you an email regard to property on {property_obj.property_address}"
        Notification.objects.create(sender=request.user, recipient=property_obj.owner, property=property_obj, message=msg)
        return HttpResponse('Email sent successfully.')
    
    context = {'form': form}
    return render(request, 'property/email_owner.html', context)

