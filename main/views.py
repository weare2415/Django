from django.shortcuts import render, redirect
from .models import User, Place, Stay, Search
from .modules import map
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.db.models import Q
import folium
import osmnx as ox
import networkx as nx
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

def index(request):
    places = Place.objects.filter(category = '명소').order_by('?')[:5]
    cafes = Place.objects.filter(category = '카페').order_by('?')[:5]
    restaurants = Place.objects.filter(category = '식당').order_by('?')[:5]
    
    try:
        user = request.user
        search_list = Search.objects.filter(user_id = user).values("pl_id_id")
        search_places = Place.objects.filter(id__in = search_list)
        
        return render(request, 'main/index.html', {'places' : places,
                                               'cafes' : cafes,
                                               'restaurants' : restaurants,
                                               'search_places' : search_places,
                                               'name' : user.username})
        
    except:
        return render(request, 'main/index.html', {'places' : places,
                                               'cafes' : cafes,
                                               'restaurants' : restaurants,})

def login_index(request):
    if request.method == 'POST':
        account = request.POST.get('account')

        if account == 'login':
            username = request.POST.get('username')
            password = request.POST.get('password')

            userObject = authenticate(request, username=username, password=password)

            if userObject is not None:
                login(request, userObject)
                return redirect('/')  # 로그인 성공 시 메인 페이지로 리다이렉트
            else:
                # 로그인 실패 시 오류 메시지를 전달하고 다시 로그인 페이지를 렌더링
                return render(request, 'user/login.html', {'error_msg': '아이디 또는 비밀번호가 올바르지 않습니다.'})

        else:
            # 회원가입 페이지로 리다이렉트
            return redirect('users:JoinUrl')

    # GET 요청인 경우 로그인 페이지를 렌더링
    return render(request, 'user/login.html', {})

def logout_index(request):
    logout(request)
    return redirect('users:LoginUrl')

def join_index(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        print(account)

        if account == 'create':
            new_username = request.POST.get('username')
            new_password = request.POST.get('password')
            new_password_check = request.POST.get('password_check')
            print(new_username)
            print(new_password)

            if not new_username or not new_password:
                return render(request, 'user/join.html', {'error_msg' : '아이디 또는 비밀번호를 입력하세요.'})
            
            elif new_password != new_password_check:
                return render(request, 'user/join.html', {'error_msg':'비밀번호가 서로 같지 않습니다.'})
            
            elif User.objects.filter(username=new_username).exists():
                return render(request, 'user/join.html', {'error_msg':'이미 사용중인 아이디입니다.'})
            
            # 새로운 사용자 생성
            User.objects.create_user(username=new_username, password=new_password)

            return redirect('users:LoginUrl')  # 회원가입 완료 후 로그인 페이지로 리다이렉트
        
        else:
            # account가 'create'가 아닐 경우 처리
            return render(request, 'user/join.html', {'error_msg': '잘못된 요청입니다.'})

    # GET 요청일 때 회원가입 페이지 렌더링
    return render(request, 'user/join.html', {})

def update_index(request):
    if request.method == 'POST':
        account = request.POST.get('account')

        if account == 'update':
            # 현재 로그인된 사용자
            current_user = request.user
            password = request.POST.get('password')

            # 비밀번호 확인
            if current_user.check_password(password):
                new_username = request.POST.get('new_username')
                new_password = request.POST.get('new_password')
                new_password_confirm = request.POST.get('new_password_confirm')

                # 새 비밀번호와 확인 비밀번호가 일치하는지 확인
                if new_password == new_password_confirm:
                    # 아이디 업데이트
                    current_user.username = new_username if new_username else current_user.username
                    # 비밀번호 업데이트
                    if new_password:  # 새로운 비밀번호가 입력된 경우만 업데이트
                        current_user.set_password(new_password)

                    current_user.save()  # 변경 사항 저장

                    # 사용자 로그아웃 처리
                    logout(request)

                    # 로그아웃 후 로그인 페이지로 리다이렉트
                    return redirect('users:LoginUrl')
                else:
                    return render(request, 'user/update.html', {'error_msg': '새 비밀번호가 일치하지 않습니다.'})
            else:
                return render(request, 'user/update.html', {'error_msg': '현재 비밀번호가 올바르지 않습니다.'})
        else:
            return redirect('users:LoginUrl')
    else:
        return render(request, 'user/update.html')

def delete_index(request):
    if request.user.is_authenticated:
        user = request.user
        logout(request)  # 로그아웃 처리
        user.delete()    # 사용자 계정 삭제
        return redirect('index')  # 메인 페이지로 리다이렉트

def search_index(request):
    if request.method == 'GET':
        try:
            user = request.user
            search_list = Search.objects.filter(user_id = user).values("pl_id_id")
            search_places = Place.objects.filter(id__in = search_list)
            
            return render(request, 'main/search.html', {'search_places' : search_places,
                                                        'name' : user.username})
        except:
            return render(request, 'main/search.html')
    
    elif request.method == 'POST':
        
        search = request.POST.get('search')
        search_category = request.POST.get('search_category')
        
        search_text = request.POST.get('search_text')
        
        try:
            user = request.user
            search_list = Search.objects.filter(user_id = user).values("pl_id_id")
            search_places = Place.objects.filter(id__in = search_list)
            
            if not search_text.strip():
                return render(request, 'main/search.html', {'error_msg':'검색어를 입력하세요.',
                                               'search_places' : search_places,
                                               'name' : user.username})
                    
            if search == 'search' and search_category == 'None':
                q_filter = Q()
                for field in ["name", "location"]:
                    q_filter |= Q(**{f"{field}__icontains": search_text})
                    
                places = Place.objects.filter(q_filter, category = '명소')
                cafes = Place.objects.filter(q_filter, category = '카페')
                restaurants = Place.objects.filter(q_filter, category = '식당')
                
                return render(request, 'main/search.html', {'places' : places,
                                                            'cafes' : cafes,
                                                            'restaurants' : restaurants,
                                               'search_places' : search_places,
                                               'name' : user.username})
            
            elif search == 'search' and search_category == 'Name':
                    
                places = Place.objects.filter(name__contains = search_text, category = '명소')
                cafes = Place.objects.filter(name__contains = search_text, category = '카페')
                restaurants = Place.objects.filter(name__contains = search_text, category = '식당')
                
                return render(request, 'main/search.html', {'places' : places,
                                                            'cafes' : cafes,
                                                            'restaurants' : restaurants,
                                               'search_places' : search_places,
                                               'name' : user.username})
            
            elif search == 'search' and search_category == 'Location':
                    
                places = Place.objects.filter(location__contains = search_text, category = '명소')
                cafes = Place.objects.filter(location__contains = search_text, category = '카페')
                restaurants = Place.objects.filter(location__contains = search_text, category = '식당')
                
                return render(request, 'main/search.html', {'places' : places,
                                                            'cafes' : cafes,
                                                            'restaurants' : restaurants,
                                               'search_places' : search_places,
                                               'name' : user.username})
            
            return render(request, 'main/search.html', {'error_msg':'검색이 올바르지 않습니다.',
                                               'search_places' : search_places,
                                               'name' : user.username})
        except:
            if not search_text.strip():
                return render(request, 'main/search.html', {'error_msg':'검색어를 입력하세요.'})
                    
            if search == 'search' and search_category == 'None':
                q_filter = Q()
                for field in ["name", "location"]:
                    q_filter |= Q(**{f"{field}__icontains": search_text})
                    
                places = Place.objects.filter(q_filter, category = '명소')
                cafes = Place.objects.filter(q_filter, category = '카페')
                restaurants = Place.objects.filter(q_filter, category = '식당')
                
                return render(request, 'main/search.html', {'places' : places,
                                                            'cafes' : cafes,
                                                            'restaurants' : restaurants})
            
            elif search == 'search' and search_category == 'Name':
                    
                places = Place.objects.filter(name__contains = search_text, category = '명소')
                cafes = Place.objects.filter(name__contains = search_text, category = '카페')
                restaurants = Place.objects.filter(name__contains = search_text, category = '식당')
                
                return render(request, 'main/search.html', {'places' : places,
                                                            'cafes' : cafes,
                                                            'restaurants' : restaurants})
            
            elif search == 'search' and search_category == 'Location':
                    
                places = Place.objects.filter(location__contains = search_text, category = '명소')
                cafes = Place.objects.filter(location__contains = search_text, category = '카페')
                restaurants = Place.objects.filter(location__contains = search_text, category = '식당')
                
                return render(request, 'main/search.html', {'places' : places,
                                                            'cafes' : cafes,
                                                            'restaurants' : restaurants})
            
            return render(request, 'main/search.html', {'error_msg':'검색이 올바르지 않습니다.'})
    else:
        return render(request, 'main/search.html')
    
def mypage_view(request):
    # 로그인된 사용자의 정보를 마이페이지에 전달
    return render(request, 'user/mypage.html', {'user': request.user})


def location_index(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        user = request.user
        
        if location == 'get':
            lat, lng = map.get_location()
            return render(request, 'main/location.html', { 'lat' : lat, 'lng' : lng })
        
        if location == 'save':
            lat, lng = map.get_location()
            Stay.create(user, lat, lng)
            return render(request, 'main/location.html', { 'lat' : lat, 'lng' : lng })
        
        if location == 'visualization':
            try:
                stay = Stay.objects.get(user_id = user)
                org_lat = stay.lat
                org_lng = stay.lon
            except:
                return render(request, 'main/map.html', {'error_msg' : "현재 위치 등록이 되어있지 않습니다."})
            
            figure = folium.Map(location=[org_lat, org_lng], zoom_start=16)
            folium.Marker(location=[org_lat,org_lng], tooltip="현재 위치").add_to(figure)
            context = { 'map': figure._repr_html_() }
            return render(request, 'main/location.html', { 'lat' : org_lat, 'lng' : org_lng, 'context' : context})
            
    else:
        return render(request, 'main/location.html')
        
    return render(request, 'main/location.html')

def map_index(request):
    if request.method == 'POST':
        dst_location = request.POST.get('dest_location')
        user = request.user
    
        try:
            stay = Stay.objects.get(user_id = user)
            org_lat = float(stay.lat)
            org_lng = float(stay.lon)
        except:
            return render(request, 'main/map.html', {'error_msg' : "현재 위치 등록이 되어있지 않습니다."})
        
        try:
            place = Place.objects.get(location = dst_location)
            dst_lat = float(place.lat)
            dst_lng = float(place.lon)
            Search.create(user_id=user, pl_id=place)
        except:
            return render(request, 'main/map.html', {'error_msg' : "목적지가 잘못되었습니다."})
        
        try: 
            G_proj = ox.load_graphml('map/graph.osm')
        except:
            return render(request, 'main/map.html', {'error_msg' : "그래프를 불러오지 못했습니다."})
        orig_node = ox.nearest_nodes(G_proj, org_lng,org_lat)
        dest_node = ox.nearest_nodes(G_proj, dst_lng,dst_lat)
        
        route = nx.shortest_path(G_proj, orig_node, dest_node, weight='length')

        figure = folium.Map(location=[org_lat, org_lng], zoom_start=10)
        route_graph_map = ox.plot_route_folium(G_proj, route, route_map=figure)

        folium.Marker(location=[org_lat,org_lng], tooltip="출발지").add_to(route_graph_map)
        folium.Marker(location=[dst_lat,dst_lng], tooltip="목적지", icon=folium.Icon(color = 'red')).add_to(route_graph_map)
        
        context = { 'map': figure._repr_html_() }
        
        return render(request, 'main/map.html', {'context' : context})
    return render(request, 'main/map.html')