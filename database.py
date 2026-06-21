<!doctype html>
<!--
  =====================================================================
  index.html  ―  대시보드 SPA 셸 (Shell)
  ---------------------------------------------------------------------
  [HTML 주석 요구사항]
  • Flask 의 render_template("index.html") 으로 서빙되는 단일 페이지.
  • <div id="root"> 안에 React 가 마운트되어 모든 UI 를 그린다.
  • 빌드 도구 없이 동작하도록 React/ReactDOM/Recharts/Lucide/Tailwind/Babel 을
    전부 CDN 으로 불러온다. (수행평가 환경에서 npm 설치 없이 즉시 실행 가능)
  • Babel Standalone 이 <script type="text/babel"> 의 JSX 를 브라우저에서 컴파일.
  =====================================================================
-->
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <title>전자기 회생 서스펜션 시뮬레이터</title>
  <meta name="viewport" content="width=device-width,initial-scale=1" />

  <!-- ===== 외부 CDN 의존성 ===== -->
  <!-- Tailwind: 유틸리티 클래스로 다크 테마 / 그리드 / 반응형을 구성 -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- React 18 (UMD) + ReactDOM: 컴포넌트 트리 렌더링 -->
  <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <!-- Recharts: KPI 시계열 라인 차트 -->
  <script src="https://unpkg.com/prop-types@15/prop-types.min.js"></script>
  <script src="https://unpkg.com/recharts@2.12.7/umd/Recharts.js"></script>
  <!-- Lucide: 아이콘 -->
  <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
  <!-- Babel: JSX 를 브라우저에서 즉석 트랜스파일 -->
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

  <!-- 별도 CSS 파일 (네온/애니메이션 키프레임). Flask 의 static/ 경로에서 서빙 -->
  <link rel="stylesheet" href="/static/style.css" />
</head>
<body class="bg-slate-900 text-slate-100">
  <!-- React 가 그릴 마운트 포인트 (이 요소 하나만 비워두면 됨) -->
  <div id="root"></div>

  <!-- React 컴포넌트 본체. data-presets="react" 로 JSX 변환 활성화 -->
  <script type="text/babel" src="/static/app.jsx" data-presets="react"></script>
</body>
</html>
