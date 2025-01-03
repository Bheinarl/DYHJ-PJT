from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.conf import settings

from .models import CurrencyAlert, CustomUser
from .serializers import CustomUserDetailsSerializer, CustomRegisterSerializer

import json
import requests

from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@csrf_exempt
def set_alert(request):  # 알림 설정 API
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            
            # CurrencyAlert 모델에 알림 정보 저장
            CurrencyAlert.objects.create(
                user=request.user if request.user.is_authenticated else None,  # 로그인하지 않은 사용자는 None으로 설정
                currency=data['currency'],
                target_rate=data['target_rate']
            )
            return JsonResponse({'status': 'success'})
        
        return JsonResponse({'status': 'fail'}, status=400)
    
    except Exception as e:
        print(f"알림 설정 중 오류 발생: {e}")
        return JsonResponse({'error': '알림 설정 중 오류가 발생했습니다.'}, status=500)

def check_exchange_rate(request):  
    print("check_exchange_rate 함수 호출됨")
    print(f'리퀘스트 : {request.GET}')
    currency = request.GET.get('currency')
    api_url = f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={settings.EXCHANGE_RATE_API_KEY}&data=AP01"

    # 현재 날짜 시간 수신
    now = datetime.now()
    # 주말이라면 금요일 데이터 사용
    if now.weekday() == 5: 
        able_day = datetime.now() - timedelta(days=1)
    elif now.weekday() == 6:
        able_day = datetime.now() - timedelta(days=2)
    # 오전 11시 이전이라면 오늘을 기준으로 어제(월요일 오전 11시라면 지난 금요일) 데이터 사용
    elif now.weekday() == 0 and datetime.now().hour < 11:
        able_day = datetime.now() - timedelta(days=3)
    elif datetime.now().hour < 11:
        able_day = datetime.now() - timedelta(days=1)
    else: 
        able_day = datetime.now()
    api_url += f"&searchdate={able_day.strftime('%Y%m%d')}"
    
    try:
        response = requests.get(api_url, verify=False)  # SSL 검증 비활성화
        response.raise_for_status()
        
        data = response.json()
        print(currency)
        # 환율 데이터 추출
        currency_data = next((item for item in data if item['cur_unit'] == currency), None)
        if not currency_data:
            return JsonResponse({'error': '환율 데이터를 찾을 수 없습니다.'}, status=500)

        # 현재 환율
        current_rate = float(currency_data['deal_bas_r'].replace(',', ''))
        print(f"현재 {currency} 환율: {current_rate}")

        # 가장 최근에 설정된 알림을 기준으로 목표 환율 확인
        alert = CurrencyAlert.objects.filter(currency=currency).order_by('-created_at').first()
        print(f"알림 설정: {alert}")

        # 알림 설정이 있고, 현재 환율이 목표 환율 이하인 경우 알림 반환
        if alert and current_rate <= alert.target_rate:
            return JsonResponse({'alert': True, 'current_rate': current_rate})
        else:
            return JsonResponse({'alert': False, 'current_rate': current_rate})

    except Exception as e:
        print(f"기타 오류 발생: {e}")
        return JsonResponse({'error': '알 수 없는 오류가 발생했습니다.'}, status=500)

def get_exchange_rate(request):
    # 환율 API URL 및 API 키 (한국 수출입은행 API 사용)
    api_url = f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={settings.EXCHANGE_RATE_API_KEY}&data=AP01"
    # 오전 11시 이전이라면 오늘을 기준으로 어제 데이터 사용
    now = datetime.now()
    print(now.weekday())
    if now.weekday() == 5: 
        able_day = datetime.now() - timedelta(days=1)
    elif now.weekday() == 6:
        able_day = datetime.now() - timedelta(days=2)
    elif datetime.now().hour < 11 and now.weekday() != 0:
        able_day = datetime.now() - timedelta(days=3)
    else:
        able_day = datetime.now()
        api_url += f"&searchdate={able_day.strftime('%Y%m%d')}"
    
    try:
        # API 호출
        response = requests.get(api_url)
        response.raise_for_status()  # 오류 발생 시 예외 처리
        data = response.json()
        return JsonResponse(data, safe=False)  # 리스트 형태일 수 있으므로 safe=False 추가
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': '환율 데이터를 가져오는 중 오류가 발생했습니다.'}, status=500)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])  # Token 인증 사용
@permission_classes([IsAuthenticated]) 
def update_max_score(request):
    if request.method == 'POST':
        
        user = request.user
        max_score = request.data.get('max_score')
        my_investor_type = request.data.get('my_investor_type')

        print(max_score)
        print(user.max_score)
        if max_score is None:  
            return Response({'error': 'totalValue 필드가 전달되지 않았습니다.'}, status=400)
        if my_investor_type is None:
            return Response({'error': 'totalValue 필드가 전달되지 않았습니다.'}, status=400)
        
        user.my_investor_type = my_investor_type  # my_investor_type 업데이트
        user.save()

        if max_score > user.max_score:  # 최고 점수 업데이트
          user.max_score = max_score
          user.save()
          return Response({'message': 'Max score updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'max_score not provided'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):  # 회원가입 API
    username = request.data.get('username')
    password = request.data.get('password')
    nickname = request.data.get('nickname')
    age = request.data.get('age')
    my_investor_type = request.data.get('my_investor_type')

    if CustomUser.objects.filter(username=username).exists():
        return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = CustomUser.objects.create_user(
        username=username,
        password=password,
        nickname=nickname,  # nickname 필드 추가
        age=age,  # age 필드 추가
        my_investor_type=my_investor_type  # my_investor_type 필드 추가
    )
    token, created = Token.objects.get_or_create(user=user)  # Token 생성
    return Response({'token': token.key}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):

    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        # 이미 존재하는 Token을 반환
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# 프로필 조회 API
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user  # 인증된 사용자
    serializer = CustomUserDetailsSerializer(user)  # 사용자 데이터를 직렬화
    
    # 프로필 사진 경로 설정
    profile_data = serializer.data
    if not user.profile_picture:
        profile_data['profile_picture'] = f"https://dyhj2024.site/static/images/default-user.png"
    elif user.profile_picture.url.startswith('/media/'):
        profile_data['profile_picture'] = f"https://dyhj2024.site{user.profile_picture.url}"

    return Response(profile_data)



from rest_framework.parsers import MultiPartParser, FormParser
# 프로필 수정 API
@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user  # 인증된 사용자
    serializer = CustomUserDetailsSerializer(user, data=request.data, partial=True)  # 부분 업데이트

    print("요청 데이터:", request.data)
    print("요청 파일:", request.FILES)  # 파일 목록 출력

    if serializer.is_valid():
        # 파일이 전송되었는지 확인
        if 'profile_picture' in request.FILES:
            print("파일 업로드 확인:", request.FILES['profile_picture'])
            user.profile_picture = request.FILES['profile_picture']  # 프로필 사진 저장
            user.save()
        serializer.save()
        return Response(serializer.data)
    else:
        print("유효성 검사 실패:", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_profile_picture(request):
    user = request.user
    serializer = CustomUserDetailsSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        # 프로필 사진이 업로드된 경우 저장
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
            user.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# 현재 사용자 정보 조회 API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    return Response({
        'username': request.user.username,
        'email': request.user.email,
        'nickname': request.user.nickname,
        'age': request.user.age,
        'my_investor_type': request.user.my_investor_type,
        # 추가적인 사용자 정보도 반환 가능
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_leaderboard(request):
    # users = CustomUser.objects.all().order_by('-max_score')[:10]  # 상위 10명
    users = CustomUser.objects.all().order_by('-max_score') # 상위 10명이 아닌 전체 랭킹 볼 수 있도록 변경
    leaderboard = [
        {
            'username': user.username,
            'nickname': user.nickname,
            'max_score': user.max_score,
            "profile_picture": user.profile_picture.url if user.profile_picture else None,
        }
        for user in users
    ]
    return Response(leaderboard, status=status.HTTP_200_OK)




