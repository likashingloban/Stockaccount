#!/usr/bin/env python3
"""
Deployment script: Mount frontend code to backend specified directory
For development and deployment environments
"""

import os
import shutil
from pathlib import Path

# Project root directory
ROOT_DIR = Path(__file__).parent.absolute()

# Frontend source directory
FRONTEND_SRC = ROOT_DIR / "frontend"
FRONTEND_TEMPLATES = FRONTEND_SRC / "templates"
FRONTEND_STATIC = FRONTEND_SRC / "static"

# Backend target directory
BACKEND_DIR = ROOT_DIR / "backend"
BACKEND_TEMPLATES = BACKEND_DIR / "templates"
BACKEND_STATIC = BACKEND_DIR / "static"


def clean_backend_dirs():
    """Clear backend templates and static directories"""
    print("🧹 Cleaning backend directories...")

    if BACKEND_TEMPLATES.exists():
        shutil.rmtree(BACKEND_TEMPLATES)
    if BACKEND_STATIC.exists():
        shutil.rmtree(BACKEND_STATIC)

    BACKEND_TEMPLATES.mkdir(parents=True, exist_ok=True)
    BACKEND_STATIC.mkdir(parents=True, exist_ok=True)

    print("✅ Backend directories cleaned")


def copy_templates():
    """Copy template files to backend"""
    print("📄 Copying template files...")

    if not FRONTEND_TEMPLATES.exists():
        print("⚠️  Warning: frontend_src/templates directory does not exist")
        return

    # Copy all HTML templates
    for template_file in FRONTEND_TEMPLATES.glob("**/*.html"):
        relative_path = template_file.relative_to(FRONTEND_TEMPLATES)
        target_file = BACKEND_TEMPLATES / relative_path

        target_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(template_file, target_file)
        print(f"  ✓ {relative_path}")

    print("✅ Template files copied")


def copy_static():
    """Copy static resources to backend"""
    print("📦 Copying static resources...")

    if not FRONTEND_STATIC.exists():
        print("⚠️  Warning: frontend_src/static directory does not exist")
        return

    # Copy all static files
    for static_file in FRONTEND_STATIC.glob("**/*"):
        if static_file.is_file():
            relative_path = static_file.relative_to(FRONTEND_STATIC)
            target_file = BACKEND_STATIC / relative_path

            target_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(static_file, target_file)
            print(f"  ✓ {relative_path}")

    print("✅ Static resources copied")


def deploy(clean=True):
    """
    Execute deployment

    Args:
        clean: Whether to clean target directories first
    """
    print("=" * 60)
    print("🚀 Starting to deploy frontend to backend")
    print("=" * 60)

    if clean:
        clean_backend_dirs()

    copy_templates()
    copy_static()

    print("=" * 60)
    print("✅ Deployment completed!")
    print("=" * 60)
    print(f"📁 Templates directory: {BACKEND_TEMPLATES}")
    print(f"📁 Static resources directory: {BACKEND_STATIC}")
    print("")
    print("💡 Tips:")
    print("  - You can now run Flask application: cd backend && python app.py")
    print("  - Frontend source code is saved in: frontend/")
    print("  - Re-run this script after modifying frontend to update")
    print("")


def watch_mode():
    """Watch mode: Automatically detect file changes and redeploy"""
    try:
        import time
        import hashlib

        print("👀 Watch mode started (Ctrl+C to exit)")
        print("   Watching directory:", FRONTEND_SRC)
        print("")

        last_hash = None

        while True:
            # Calculate hash of frontend directory
            current_hash = hashlib.md5()

            for file_path in sorted(FRONTEND_SRC.glob("**/*")):
                if file_path.is_file():
                    current_hash.update(file_path.read_bytes())

            current_hash = current_hash.hexdigest()

            # Changes detected
            if last_hash and current_hash != last_hash:
                print("\n🔄 File changes detected, redeploying...")
                deploy(clean=True)

            last_hash = current_hash
            time.sleep(2)  # Check every 2 seconds

    except KeyboardInterrupt:
        print("\n👋 Watch mode stopped")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--watch":
        # Deploy once first
        deploy(clean=True)
        # Enter watch mode
        watch_mode()
    else:
        # Single deployment
        deploy(clean=True)
