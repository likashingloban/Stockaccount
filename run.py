#!/usr/bin/env python3
"""
Quick start script: Deploy frontend and start Flask application
"""

import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).parent.absolute()

def main():
    print("=" * 60)
    print("🚀 Stock Watch & Alert System - Quick Start")
    print("=" * 60)
    print("")

    # 1. Deploy frontend
    print("📦 Step 1/2: Deploy frontend to backend...")
    try:
        subprocess.run([sys.executable, str(ROOT_DIR / "deploy.py")], check=True)
    except subprocess.CalledProcessError:
        print("❌ Deployment failed!")
        return 1

    print("")
    print("=" * 60)

    # 2. Start Flask application
    print("🚀 Step 2/2: Start Flask application...")
    print("=" * 60)
    print("")

    try:
        subprocess.run(
            [sys.executable, str(ROOT_DIR / "backend" / "app.py")],
            cwd=str(ROOT_DIR / "backend")
        )
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped")
        return 0

if __name__ == "__main__":
    sys.exit(main())
