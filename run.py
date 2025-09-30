#!/usr/bin/env python3
"""
RAG 시스템 실행 스크립트 (간소화 버전)
"""
import os
import sys
import subprocess
import webbrowser
import time
import signal
from pathlib import Path

def print_banner():
    """시작 배너 출력"""
    print("=" * 60)
    print("🤖 RAG 질의응답 시스템")
    print("=" * 60)
    print("📋 기능:")
    print("   - AI 기반 질의응답")
    print("   - 문서 기반 검색 (Supabase + Vector DB)")
    print("   - 현대적인 웹 UI")
    print("=" * 60)

def check_requirements():
    """필수 요구사항 확인"""
    print("\n🔍 요구사항 확인 중...")
    
    missing_files = []
    
    # 필수 파일 확인
    required_files = {
        '.env': '.env 파일 (API 키 설정)',
        'requirements.txt': 'requirements.txt (Python 패키지 목록)',
        'main.py': 'main.py (백엔드 서버)',
        'index.html': 'index.html (프론트엔드 UI)'
    }
    
    for file, description in required_files.items():
        if not os.path.exists(file):
            missing_files.append(f"❌ {file} - {description}")
        else:
            print(f"✅ {file}")
    
    if missing_files:
        print("\n❌ 다음 파일들이 없습니다:")
        for file in missing_files:
            print(f"   {file}")
        return False
    
    # .env 파일 내용 확인
    try:
        with open('.env', 'r') as f:
            env_content = f.read()
            required_keys = ['SUPABASE_URL', 'SUPABASE_KEY', 'GEMINI_API_KEY']
            missing_keys = []
            
            for key in required_keys:
                if f"{key}=" not in env_content:
                    missing_keys.append(key)
            
            if missing_keys:
                print(f"\n⚠️  .env 파일에 다음 설정이 없습니다:")
                for key in missing_keys:
                    print(f"   {key}=your_value_here")
                print("\n📝 .env 파일 예시:")
                print("SUPABASE_URL=https://your-project.supabase.co")
                print("SUPABASE_KEY=your_supabase_anon_key")
                print("GEMINI_API_KEY=your_gemini_api_key")
                return False
            else:
                print("✅ .env 파일 설정 완료")
    except Exception as e:
        print(f"❌ .env 파일 읽기 오류: {e}")
        return False
    
    print("✅ 모든 필수 파일이 준비되었습니다!")
    return True

def check_python_version():
    """Python 버전 확인"""
    version = sys.version_info
    print(f"🐍 Python 버전: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 이상이 필요합니다.")
        return False
    
    print("✅ Python 버전 호환")
    return True

def install_packages():
    """패키지 설치"""
    print("\n📦 Python 패키지 설치 중...")
    try:
        # pip 업그레이드
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=False, capture_output=True)
        
        # requirements 설치
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                               check=True, capture_output=True, text=True)
        
        print("✅ 패키지 설치 완료")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 패키지 설치 실패:")
        print(f"   오류 메시지: {e.stderr}")
        print("\n💡 해결 방법:")
        print("   1. 가상환경을 사용하고 계신지 확인")
        print("   2. pip install -r requirements.txt 를 직접 실행")
        print("   3. Python 버전 확인 (3.8+ 필요)")
        return False
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        return False

def start_server():
    """백엔드 서버 시작"""
    print("\n🚀 백엔드 서버 시작 중...")
    try:
        # 서버 프로세스 시작
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 서버 시작 대기
        print("⏳ 서버 초기화 중... (5초 대기)")
        time.sleep(5)
        
        # 프로세스가 여전히 실행 중인지 확인
        if process.poll() is None:
            print("✅ 백엔드 서버가 성공적으로 시작되었습니다!")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ 서버 시작 실패:")
            if stderr:
                print(f"   오류: {stderr}")
            if stdout:
                print(f"   출력: {stdout}")
            return None
            
    except Exception as e:
        print(f"❌ 서버 시작 실패: {e}")
        return None

def open_browser():
    """브라우저에서 웹사이트 열기"""
    try:
        html_file = Path("index.html").resolve()
        file_url = f"file://{html_file}"
        
        print(f"🌐 브라우저에서 열기: {html_file}")
        webbrowser.open(file_url)
        print("✅ 브라우저에서 웹사이트를 열었습니다!")
        
    except Exception as e:
        print(f"⚠️  브라우저 자동 열기 실패: {e}")
        print("💡 수동으로 index.html 파일을 브라우저에서 열어주세요.")

def print_usage_info():
    """사용법 안내"""
    print("\n" + "=" * 60)
    print("✅ RAG 시스템이 성공적으로 실행되었습니다!")
    print("=" * 60)
    print("📍 접속 정보:")
    print("   - 백엔드 API: http://localhost:8000")
    print("   - 프론트엔드: index.html (브라우저에서 자동 열림)")
    print("   - API 문서: http://localhost:8000/docs")
    print("\n🔧 사용법:")
    print("   1. 브라우저에서 웹사이트가 자동으로 열립니다")
    print("   2. AI 어시스턴트와 대화를 시작하세요")
    print("   3. 질문을 입력하고 Enter를 누르세요")
    print("\n🛑 종료:")
    print("   - Ctrl+C를 누르면 서버가 종료됩니다")
    print("=" * 60)

def signal_handler(sig, frame):
    """시그널 핸들러 (Ctrl+C)"""
    print("\n\n🛑 종료 신호를 받았습니다...")
    sys.exit(0)

def main():
    """메인 함수"""
    # 시그널 핸들러 등록
    signal.signal(signal.SIGINT, signal_handler)
    
    # 배너 출력
    print_banner()
    
    # Python 버전 확인
    if not check_python_version():
        print("\n❌ 실행을 중단합니다.")
        return 1
    
    # 요구사항 확인
    if not check_requirements():
        print("\n❌ 실행을 중단합니다.")
        print("\n💡 도움말:")
        print("   1. 모든 필수 파일이 현재 디렉토리에 있는지 확인")
        print("   2. .env 파일에 올바른 API 키가 설정되어 있는지 확인")
        return 1
    
    # 패키지 설치
    print("\n📦 의존성 패키지를 확인하고 설치합니다...")
    user_input = input("계속하시겠습니까? (y/N): ").lower().strip()
    if user_input not in ['y', 'yes']:
        print("❌ 사용자가 취소했습니다.")
        return 1
    
    if not install_packages():
        print("\n❌ 실행을 중단합니다.")
        return 1
    
    # 서버 시작
    server_process = start_server()
    if not server_process:
        print("\n❌ 실행을 중단합니다.")
        return 1
    
    # 브라우저 열기
    time.sleep(1)  # 잠깐 대기
    open_browser()
    
    # 사용법 안내
    print_usage_info()
    
    try:
        # 서버 프로세스 대기
        print("\n⏳ 서버가 실행 중입니다. 종료하려면 Ctrl+C를 누르세요...\n")
        server_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 서버를 종료합니다...")
        try:
            server_process.terminate()
            server_process.wait(timeout=5)
        except:
            server_process.kill()
        print("✅ 서버가 정상적으로 종료되었습니다.")
        return 0
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류가 발생했습니다: {e}")
        try:
            server_process.terminate()
        except:
            pass
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)