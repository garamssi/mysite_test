import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite_test.mysite.settings')
import django
django.setup()

from django.utils import timezone
from django.contrib.auth.models import User
import requests
from django.core.files import File
from tempfile import NamedTemporaryFile

from blog.models import Post, Category, Tag

# 카테고리 가져오기
travel_category = Category.objects.get(name='여행')

# 태그 생성
tags = [
    '일본', '도쿄', '오사카', '교토', '먹방', '힐링', '자연', '문화', '쇼핑'
]

tag_objects = []
for tag_name in tags:
    tag, _ = Tag.objects.get_or_create(
        name=tag_name,
        slug=tag_name.lower()
    )
    tag_objects.append(tag)

# 대표 여행 컨텐츠용 태그 추가
main_tags = ['대표', '에피소드', '실패담', '먹방', '맛집', '랜선여행', '세계일주', '도전', '액티비티', '힐링', '자연', '로컬', '체험']
for tag_name in main_tags:
    Tag.objects.get_or_create(name=tag_name, slug=tag_name.lower())

# 게시글 데이터
posts_data = [
    {
        'title': '도쿄 3박 4일 완벽 가이드',
        'hook_text': '도쿄의 핫플레이스부터 숨은 맛집까지!',
        'content': '''
# 도쿄 3박 4일 완벽 가이드

## 1일차: 시부야 & 하라주쿠
- 시부야 스크램블 교차로
- 하라주쿠 타케시타 거리
- 메이지 신궁

## 2일차: 아사쿠사 & 스카이트리
- 아사쿠사 센소지
- 도쿄 스카이트리
- 스미다 강 유람선

## 3일차: 시나가와 & 오다이바
- 시나가와 아쿠아파크
- 오다이바 자유의 여신상
- 다이버시티 도쿄 플라자

## 4일차: 긴자 & 도쿄역
- 긴자 쇼핑
- 도쿄역 야마노테선
- 황궁 외원

## 맛집 추천
1. 츠키지 시장의 초밥
2. 시부야의 라멘
3. 긴자의 스키야키
''',
        'tags': ['일본', '도쿄', '먹방', '쇼핑']
    },
    {
        'title': '교토의 숨겨진 절집 탐방기',
        'hook_text': '관광객이 적은 교토의 아름다운 절집들을 소개합니다',
        'content': '''
# 교토의 숨겨진 절집 탐방기

## 1. 아다시노넨부츠지
- 8000개의 작은 석불이 있는 독특한 절
- 아침 안개 속에서 더욱 신비로운 분위기
- 입장료: 500엔

## 2. 코다이지
- 밤에 열리는 특별한 야간 관람
- 반영된 단풍의 아름다움
- 입장료: 600엔

## 3. 산젠인
- 아라시야마의 숨겨진 보석
- 아름다운 정원과 고요한 분위기
- 입장료: 500엔

## 방문 팁
- 아침 일찍 방문하면 사람이 적음
- 사진 촬영은 허용되지만 플래시 사용 금지
- 절집 내에서는 조용히 해야 함
''',
        'tags': ['일본', '교토', '문화', '힐링']
    },
    {
        'title': '오사카 먹방 투어 가이드',
        'hook_text': '오사카의 맛있는 음식들을 소개합니다',
        'content': '''
# 오사카 먹방 투어 가이드

## 도톤보리 맛집
1. 타코야키
   - 크리미한 속과 바삭한 겉
   - 추천: 크리미 타코야키

2. 오코노미야키
   - 오사카 스타일의 특별한 맛
   - 추천: 고기 오코노미야키

3. 쿠시카츠
   - 바삭한 튀김의 향연
   - 추천: 다양한 종류의 쿠시카츠 세트

## 신사이바시 맛집
1. 라멘
   - 진한 육수의 맛
   - 추천: 차슈 라멘

2. 스시
   - 신선한 회의 맛
   - 추천: 오마카세 코스

## 방문 팁
- 점심시간대는 피하는 것이 좋음
- 현금을 충분히 준비
- 줄이 긴 가게가 맛집의 증거
''',
        'tags': ['일본', '오사카', '먹방']
    }
]

# 게시글 생성
admin_user = User.objects.get(username='rami')  # 관리자 계정 사용

for post_data in posts_data:
    post = Post.objects.create(
        title=post_data['title'],
        hook_text=post_data['hook_text'],
        content=post_data['content'],
        category=travel_category,
        author=admin_user,
        created_at=timezone.now()
    )
    
    # 태그 추가
    for tag_name in post_data['tags']:
        tag = Tag.objects.get(name=tag_name)
        post.tags.add(tag)

# 대표 여행 컨텐츠 추가
main_contents = [
    {
        'title': '망했다 여행',
        'hook_text': '비행기 놓치고, 숙소는 오버부킹! 여행이 망해도 영상은 터진다?!',
        'content': '여행 중 만난 각종 실패담과 에피소드, 그리고 그 속에서 얻은 깨달음과 웃음!',
        'tags': ['대표', '에피소드', '실패담'],
        'image': 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=600&q=80'
    },
    {
        'title': '먹방 투어',
        'hook_text': '"이 맛은 못 참지!" 현지인도 놀란 폭풍 먹방, 위장은 늘 준비 완료!',
        'content': '세계 각국의 맛집을 찾아 떠나는 먹방 여행. 현지 음식과 숨은 맛집 소개!',
        'tags': ['대표', '먹방', '맛집'],
        'image': 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=600&q=80'
    },
    {
        'title': '랜선 세계일주',
        'hook_text': '비행기값 아끼고, 집에서 세계일주! 랜선으로 떠나는 글로벌 여행.',
        'content': '여행을 떠나지 못하는 이들을 위한 랜선 세계일주! 각국의 명소와 문화를 집에서 즐기자.',
        'tags': ['대표', '랜선여행', '세계일주'],
        'image': 'https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=600&q=80'
    },
    {
        'title': '도전 여행',
        'hook_text': '"오늘은 무전여행, 내일은 번지점프!" 도전이 곧 여행의 맛!',
        'content': '무전여행, 번지점프, 스카이다이빙 등 다양한 액티비티에 도전하는 여행기.',
        'tags': ['대표', '도전', '액티비티'],
        'image': 'https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=600&q=80'
    },
    {
        'title': '힐링 여행',
        'hook_text': '"여행은 힐링이지!" 바다, 숲, 온천에서 충전하는 하루.',
        'content': '자연 속에서의 힐링, 바다와 숲, 온천에서의 여유로운 여행을 소개합니다.',
        'tags': ['대표', '힐링', '자연'],
        'image': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=600&q=80'
    },
    {
        'title': '로컬 여행',
        'hook_text': '관광지는 이제 그만! 현지인처럼 살아보는 진짜 여행.',
        'content': '관광지가 아닌 현지인의 삶을 체험하는 로컬 여행의 매력.',
        'tags': ['대표', '로컬', '체험'],
        'image': 'https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=600&q=80'
    },
]

def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(response.content)
        img_temp.flush()
        return File(img_temp, name=url.split('/')[-1])
    return None

for main in main_contents:
    post = Post.objects.create(
        title=main['title'],
        hook_text=main['hook_text'],
        content=main['content'],
        category=travel_category,
        author=admin_user,
        created_at=timezone.now(),
    )
    for tag_name in main['tags']:
        tag = Tag.objects.get(name=tag_name)
        post.tags.add(tag)
    # 대표 이미지 저장
    if hasattr(post, 'head_image') and main.get('image'):
        image_file = download_image(main['image'])
        if image_file:
            post.head_image.save(image_file.name, image_file, save=True)

print("게시글이 성공적으로 생성되었습니다!")
print("대표 여행 컨텐츠도 성공적으로 생성되었습니다!") 