from django.shortcuts import render, redirect
from .models import *
from word.models import *
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, timedelta
from .forms import *
import requests 
from lxml import html
from django.http import JsonResponse
from django.db.models.query_utils import Q
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from django.core.exceptions import ValidationError


from .serializers import InformationSerializer, PartySerializer, TagSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from .serializers import *

import facebook_scraper as fs

@login_required
def home(request):
    parties = Party.objects.all()
    headlines = Headline.objects.all()
    information = Info.objects.all()

    if request.method == 'POST': 
        if request.POST.get("form_type") == 'addInfo':
            POST_ID = request.POST.get('link')
            try:
                if POST_ID != '' and 'www.facebook.com' or 'watch' in POST_ID and 'groups' not in POST_ID:
                    gen = fs.get_posts(
                        post_urls=[POST_ID],
                        options={"progress": True},
                        cookies = {
                        #	'datr': "bhfzZHyvnnHjPbSD1jdCyltD",
                        #	'x-src': "value_from_browser",
                        #	'sb': "m-T9ZMpc43EvcIR887-htOy6",
                        #	'spin': "value_from_browser",
                        #	'wd': "1280x595",
                            'c_user': "100004074013764",
                            'xs': "14%3AB6Mv0BVFDVz6bg%3A2%3A1696426952%3A-1%3A7109%3A%3AAcWDbxf0J0NR2zwjn-NWEq3jxyiHmK-yRX6K-jcifA",
                        #	'fr': "0vspNHQAakijgzqvz.AWUSKIQ8YCjXtjoAFsnFnsNaBaA.BlI-ak.eV.AAA.0.0.BlI-ak.AWVcEzKNrgg"
                        }                    
                    )
                    post = next(gen)
                    post_text = post['post_text']
                    try:
                        post_images = post['images']
                        post_image = post_images[0]
                        
                    except:
                        post_image = ''
                    try:
                        post_video = post['video']                    
                    except:
                        post_video = ''                        


                    newInfo = Info.objects.create(
                        title = request.POST.get('title'),
                        text = post_text,
                        link = request.POST.get('link'),
                        creator = request.user,
                    )
                    if post_image != '':
                        response = requests.get(post_image)
                        response.raise_for_status()
                        img_temp = NamedTemporaryFile()
                        img_temp.write(response.content)
                        img_temp.flush()
                        newInfo.file.save(f'{newInfo.title}.jpg', File(img_temp))
                    else:
                        pass
                    if post_video != None:
                        response = requests.get(post_video)
                        response.raise_for_status()
                        video_temp = NamedTemporaryFile()
                        video_temp.write(response.content)
                        video_temp.flush()
                        newInfo.file.save(f'{newInfo.title}.mp4', File(video_temp))
                    else:
                        pass
            
                else:
                    newInfo = Info.objects.create(
                        title = request.POST.get('title'),
                        text = request.POST.get('text'),
                        link = request.POST.get('link'),
                        creator = request.user,
                    )

                    if newInfo.text == '':
                        newInfo.text = f"تمت إضافة هذه المعلومة بالتحديد في {newInfo.created_at}..."
                        newInfo.save()  

            except:        
                pass
            

            Fparties = request.POST.get('parties')
            if Fparties == '':
                pass
            else:
                parties_list = Fparties.split(' ')
                for party in parties_list:
                    newParty, created = Party.objects.get_or_create(title=party, creator=request.user)
                    newInfo.party.add(newParty)

            hashtags = request.POST.get('tags')
            if hashtags == '':
                pass
            else:
                hashtag_list = hashtags.split(' ')
                for tag in hashtag_list:
                    newTag, created = Tag.objects.get_or_create(title=tag, creator=request.user)
                    newInfo.tags.add(newTag)
  

                                
        elif request.POST.get("form_type") == 'editInfo':
            info = Info.objects.get(id=request.POST.get('id'))
            info.title = request.POST.get('title')
            info.text = request.POST.get('text')
            info.link = request.POST.get('link')
            info.save()

            messages.success(request, ('Your item was successfully added!'))
            return redirect("home")
    context = {'information': information, 'parties': parties, 'headlines': headlines, }
    return render(request, 'main/home.html', context)


@login_required
def party(request, pk):
    parties = Party.objects.all()
    headlines = Headline.objects.all()
    party = get_object_or_404(Party, id=pk)

    if request.method == 'POST': 
        if request.POST.get("form_type") == 'editInfo':
            info = Info.objects.get(id=request.POST.get('id'))
            info.title = request.POST.get('title')
            info.text = request.POST.get('text')
            info.link = request.POST.get('link')
            info.save()

            messages.success(request, ('Your item was successfully added!'))
            return redirect("home")
 
        elif request.POST.get("form_type") == 'editpartyform':
            party.title = request.POST.get("title")
            party.text = request.POST.get("text")
            headlines = request.POST.getlist('headlines')
            party.headline.set(headlines)
            
            party.save()
            if party.title == '':
                party.title = "Untitled"
                party.save()
            messages.success(request, ('Your item was successfully added!'))
            return redirect("party", pk=party.id)

    context = {'party': party, 'parties': parties, 'headlines': headlines}
    return render(request, 'main/party.html', context)

@login_required
def tag(request, pk):
    parties = Party.objects.all()
    headlines = Headline.objects.all()
    tag = get_object_or_404(Tag, id=pk)

    if request.method == 'POST':                        
        if request.POST.get("form_type") == 'editInfo':
            info = Info.objects.get(id=request.POST.get('id'))
            info.title = request.POST.get('title')
            info.text = request.POST.get('text')
            info.link = request.POST.get('link')
            info.save()

            messages.success(request, ('Your item was successfully added!'))
            return redirect("home")
 
        elif request.POST.get("form_type") == 'edittagform':
            tag.title = request.POST.get("title")
            tag.save()
            if tag.title == '':
                tag.title = "Untitled"
                tag.save()
            messages.success(request, ('Your item was successfully added!'))
            return redirect("tag", pk=tag.id)

    context = {'tag': tag, 'parties': parties, 'headlines': headlines}
    return render(request, 'main/tag.html', context)


@login_required
def parties(request):
    parties = Party.objects.all()
    headlines = Headline.objects.all()

    if request.method == 'POST': 
        newparty = Party.objects.create(
            title = request.POST.get('title'),
            text = request.POST.get('text'),
            creator=request.user
        )
        headlines = request.POST.getlist('headlines')
        newparty.headline.set(headlines)
            

        if newparty.title == '':
            newparty.title = "Untitled Party"
            newparty.save()        
        messages.success(request, ('Your item was successfully added!'))
        return redirect("parties")

    context = {'parties': parties, 'headlines': headlines,}
    return render(request, 'main/parties.html', context)

@login_required
def headline(request, pk):
    headline = Headline.objects.get(id=pk)
    parties = headline.Pheadline.all()
    headlines = Headline.objects.all()

    if request.method == 'POST': 
        newparty = Party.objects.create(
            title = request.POST.get('title'),
            text = request.POST.get('text'),
            creator=request.user
        )
        setHeadline = Headline.objects.filter(id=headline.id)
        newparty.headline.set(setHeadline)
            

        if newparty.title == '':
            newparty.title = "Untitled Party"
            newparty.save()        
        messages.success(request, ('Your item was successfully added!'))
        return redirect("headline", pk = headline.id)

    context = {'parties': parties, 'headlines': headlines, 'headline': headline}
    return render(request, 'main/headline.html', context)


@login_required
def search(request):
    search = request.GET.get('query')
    if request.GET.get("form_type") == 'infosearchform':
        searchForm = "info"
        information = Info.objects.filter(
            Q(title__icontains=search)|
            Q(link__icontains=search)|
            Q(creator__username__icontains=search)|
            Q(party__title__icontains=search)|
            Q(tags__title__icontains=search)|
            Q(created_at__icontains=search)
            ).distinct()


    elif request.GET.get("form_type") == 'partysearchform':
        searchForm = "party"
        information = Party.objects.filter(
            Q(title__icontains=search)
            ).distinct()

    elif request.GET.get("form_type") == 'documentsearchform':
        searchForm = "document"
        information = Document.objects.filter(
            Q(title__icontains=search)
            )

    documents = Document.objects.all()
    parties = Party.objects.all()
    headlines = Headline.objects.all()

    if request.method == 'POST': 
        if request.POST.get("form_type") == 'editInfo':
            info = Info.objects.get(id=request.POST.get('id'))
            info = Info.objects.get(id=request.POST.get('id'))
            info.title = request.POST.get('title')
            info.text = request.POST.get('text')
            info.link = request.POST.get('link')
            info.save()

            messages.success(request, ('Your item was successfully added!'))
            return redirect("home")
    context = {'information': information, 'parties': parties, 'headlines': headlines, 'documents':documents, 'searchForm':searchForm}

    return render(request, 'main/components/search.html', context)





@login_required
def delete_party(request, pk):
    party = Party.objects.get(id=pk)
    party.delete()
    return redirect('home')

@login_required
def delete_tag(request, pk):
    element = Tag.objects.get(id=pk)
    element.delete()
    return redirect('home')

@login_required
def delete_info(request, pk):
    info = Info.objects.get(id=pk)
    info.delete()
    return redirect('home')







def loginPage(request):
    page = 'loginPage'
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username, password=password)
        except:
            messages.error(request, "Invalid username or password!")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if 'next' in request.GET:
                return redirect(request.GET['next'])
            else:
                return redirect('home')
        else:
            messages.error(request, "This user does not exist!")

    if request.user.is_authenticated:
        if 'next' in request.GET:
            return redirect(request.GET['next'])
        else:
            return redirect('home')    
    context = {'page': page}
    return render(request, 'main/registration/login.html', context)


def registerPage(request):
    page = 'registerPage'

    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.user.is_authenticated:
        return redirect('home')  


    context = {'form': form, 'page': page}
    return render(request, 'main/registration/login.html', context)

@login_required
def logoutUser(request):
    logout(request)
    return redirect('home')   



class InformationViewSet(viewsets.ModelViewSet):
    queryset = Info.objects.all()
    serializer_class = InformationSerializer

class PartyViewSet(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer