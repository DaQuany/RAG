#!/usr/bin/env python3
"""
RAG System Execution Script (Simplified Version)
"""
import os
import sys
import subprocess
import webbrowser
import time
import signal
from pathlib import Path

def print_banner():
    """Prints the startup banner"""
    print("=" * 60)
    print("🤖 RAG Question-Answering System")
    print("=" * 60)
    print("📋 Features:")
    print("   - AI-based question answering")
    print("   - Document-based search (Supabase + Vector DB)")
    print("   - Modern web UI")
    print("=" * 60)

def check_requirements():
    """Checks for necessary requirements"""
    print("\n🔍 Checking requirements...")
    
    missing_files = []
    
    # Check for essential files
    required_files = {
        '.env': '.env file (API key settings)',
        'requirements.txt': 'requirements.txt (List of Python packages)',
        'main.py': 'main.py (Backend server)',
        'index.html': 'index.html (Frontend UI)'
    }
    
    for file, description in required_files.items():
        if not os.path.exists(file):
            missing_files.append(f"❌ {file} - {description}")
        else:
            print(f"✅ {file}")
    
    if missing_files:
        print("\n❌ The following files are missing:")
        for file in missing_files:
            print(f"   {file}")
        return False
    
    # Check the contents of the .env file
    try:
        with open('.env', 'r') as f:
            env_content = f.read()
            required_keys = ['SUPABASE_URL', 'SUPABASE_KEY', 'GEMINI_API_KEY']
            missing_keys = []
            
            for key in required_keys:
                if f"{key}=" not in env_content:
                    missing_keys.append(key)
            
            if missing_keys:
                print(f"\n⚠️  The following settings are missing in the .env file:")
                for key in missing_keys:
                    print(f"   {key}=your_value_here")
                print("\n📝 .env file example:")
                print("SUPABASE_URL=https://your-project.supabase.co")
                print("SUPABASE_KEY=your_supabase_anon_key")
                print("GEMINI_API_KEY=your_gemini_api_key")
                return False
            else:
                print("✅ .env file setup is complete")
    except Exception as e:
        print(f"❌ Error reading the .env file: {e}")
        return False
    
    print("✅ All required files are ready!")
    return True

def check_python_version():
    """Checks the Python version"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required.")
        return False
    
    print("✅ Python version is compatible")
    return True

def install_packages():
    """Installs packages"""
    print("\n📦 Installing Python packages...")
    try:
        # Upgrade pip
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=False, capture_output=True)
        
        # Install requirements
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                               check=True, capture_output=True, text=True)
        
        print("✅ Package installation complete")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Package installation failed:")
        print(f"   Error message: {e.stderr}")
        print("\n💡 How to solve:")
        print("   1. Check if you are using a virtual environment")
        print("   2. Run 'pip install -r requirements.txt' directly")
        print("   3. Check your Python version (3.8+ required)")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def start_server():
    """Starts the backend server"""
    print("\n🚀 Starting the backend server...")
    try:
        # Start the server process
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for the server to start
        print("⏳ Initializing server... (waiting 5 seconds)")
        time.sleep(5)
        
        # Check if the process is still running
        if process.poll() is None:
            print("✅ The backend server has started successfully!")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Server failed to start:")
            if stderr:
                print(f"   Error: {stderr}")
            if stdout:
                print(f"   Output: {stdout}")
            return None
            
    except Exception as e:
        print(f"❌ Failed to start the server: {e}")
        return None

def open_browser():
    """Opens the website in a browser"""
    try:
        html_file = Path("index.html").resolve()
        file_url = f"file://{html_file}"
        
        print(f"🌐 Opening in browser: {html_file}")
        webbrowser.open(file_url)
        print("✅ The website has been opened in your browser!")
        
    except Exception as e:
        print(f"⚠️  Failed to open the browser automatically: {e}")
        print("💡 Please open the index.html file in your browser manually.")

def print_usage_info():
    """Prints usage information"""
    print("\n" + "=" * 60)
    print("✅ RAG system is running successfully!")
    print("=" * 60)
    print("📍 Access Information:")
    print("   - Backend API: http://localhost:8000")
    print("   - Frontend: index.html (will open automatically in your browser)")
    print("   - API Documentation: http://localhost:8000/docs")
    print("\n🔧 How to Use:")
    print("   1. The website will open automatically in your browser")
    print("   2. Start a conversation with the AI assistant")
    print("   3. Enter your question and press Enter")
    print("\n🛑 To Stop:")
    print("   - Press Ctrl+C to stop the server")
    print("=" * 60)

def signal_handler(sig, frame):
    """Signal handler (Ctrl+C)"""
    print("\n\n🛑 Received termination signal...")
    sys.exit(0)

def main():
    """Main function"""
    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Print the banner
    print_banner()
    
    # Check the Python version
    if not check_python_version():
        print("\n❌ Aborting execution.")
        return 1
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Aborting execution.")
        print("\n💡 Help:")
        print("   1. Make sure all required files are in the current directory")
        print("   2. Make sure the correct API keys are set in the .env file")
        return 1
    
    # Install packages
    print("\n📦 Checking and installing dependencies...")
    user_input = input("Do you want to continue? (y/N): ").lower().strip()
    if user_input not in ['y', 'yes']:
        print("❌ Canceled by user.")
        return 1
    
    if not install_packages():
        print("\n❌ Aborting execution.")
        return 1
    
    # Start the server
    server_process = start_server()
    if not server_process:
        print("\n❌ Aborting execution.")
        return 1
    
    # Open the browser
    time.sleep(1)  # Brief pause
    open_browser()
    
    # Print usage information
    print_usage_info()
    
    try:
        # Wait for the server process
        print("\n⏳ The server is running. Press Ctrl+C to stop...\n")
        server_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping the server...")
        try:
            server_process.terminate()
            server_process.wait(timeout=5)
        except:
            server_process.kill()
        print("✅ The server has been stopped successfully.")
        return 0
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        try:
            server_process.terminate()
        except:
            pass
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)