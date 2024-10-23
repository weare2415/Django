● 백엔드와 프론트엔드 통합
Django Framework: Django를 활용해 Python 기반의 웹 애플리케이션 백엔드를 구축
웹 애플리케이션의 비즈니스 로직과 데이터베이스, 템플릿을 효과적으로 연결
views.py에서 사용자 요청을 처리하고, HTML 템플릿을 렌더링해 사용자 인터페이스와 서버 측 데이터 간의 원활한 통합을 구현

● URL 라우팅: Django의 URL Configuration(urls.py)을 사용해 RESTful URL을 구성하고, 각 URL을 특정 뷰 함수와 매핑하여 회원가입 및 로그인 요청을 처리

● HTML 및 CSS 연동: Django 템플릿 엔진을 사용해 사용자 인터페이스와 백엔드 데이터를 효과적으로 연결
사용자로부터 입력된 데이터를 POST 요청을 통해 백엔드로 전송하고, Django의 csrf_token을 사용해 CSRF 보안을 강화했습니다.

● 데이터베이스: MySQL - Django ORM을 통해 관계형 데이터베이스를 관리하며, 사용자 정보 저장 및 조회

● Django Messages 프레임워크를 사용해 사용자에게 회원가입 성공 및 실패 메시지를 제공
