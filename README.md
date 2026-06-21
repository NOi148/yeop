"""
app.py
------
Flask 백엔드 본체.
- '/'           : 메인 대시보드 UI (index.html) 렌더링
- '/api/simulate' POST : 물리 계산 + DB 로그 저장
- '/api/history'  GET  : 최근 시뮬레이션 5개 조회
"""
from flask import Flask, render_template, request, jsonify
from database import init_db, insert_log, fetch_recent

app = Flask(__name__)

# --- 물리 상수 (간략화된 모델에서 사용) ---
B = 0.8   # 자기장 세기 (T)  - 영구자석 가정
L = 0.25  # 도선 유효 길이 (m)


@app.route("/")
def index():
    """메인 대시보드 페이지(SPA)를 반환."""
    return render_template("index.html")


@app.route("/api/simulate", methods=["POST"])
def simulate():
    """
    [주석 요구사항 ①] Flask 가 슬라이더 값을 JSON 으로 수신 → 물리식 계산.

    프론트에서 fetch('/api/simulate', {method:'POST', body: JSON})로 보낸
    파라미터를 request.get_json() 으로 dict 형태로 추출한다.
    그 후 Faraday 의 전자기 유도 법칙과 Joule 발열식을 Python 으로 계산한다.
    """
    data = request.get_json(force=True) or {}

    # ----- JSON 파라미터 추출 (슬라이더/토글 값) -----
    mode = data.get("mode", "Conventional")          # 모드: Conventional / Nano-Buffer
    v    = float(data.get("v", 1.0))                  # 서스펜션 피스톤 속도 (m/s)
    N    = int(data.get("N", 100))                    # 코일 턴 수
    R    = float(data.get("R", 1.0))                  # 내부 저항 (Ω)

    # ----- 물리 계산 ① 패러데이 유도 기전력 V = N · B · L · v -----
    voltage = N * B * L * v

    # ----- 물리 계산 ② 회로 전류 I = V / R, 줄 발열 P = I^2 · R -----
    current = voltage / R if R > 0 else 0.0
    loss    = (current ** 2) * R                     # Joule heating (W)

    # ----- 모드 보정: Nano-Buffer HESS 는 MOSFET 스위칭으로 손실 35% 저감 -----
    if mode == "Nano-Buffer":
        loss *= 0.65

    # ----- 발전량(가상): V · I  → 효율 = (발전 - 손실) / 발전 * 100 -----
    generated = voltage * current if current > 0 else 1e-9
    efficiency = max(0.0, (generated - loss) / generated * 100)

    # ----- DB 로그 자동 저장 -----
    insert_log(mode, v, N, R, voltage, loss, efficiency)

    return jsonify({
        "mode": mode,
        "voltage": round(voltage, 3),
        "current": round(current, 3),
        "loss": round(loss, 3),
        "efficiency": round(efficiency, 2),
    })


@app.route("/api/history", methods=["GET"])
def history():
    """최근 5개의 시뮬레이션 로그 반환 → 프론트 테이블에 표시."""
    return jsonify(fetch_recent(5))


if __name__ == "__main__":
    init_db()                       # 서버 시작 시 DB/테이블 보장
    app.run(debug=True, port=5000)
