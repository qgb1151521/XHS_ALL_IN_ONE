import subprocess
import sys
import time

cmd = [
    sys.executable,
    '-c',
    '''
import asyncio
import sys

async def test_startup():
    print("Testing backend startup...")
    try:
        from backend.app.main import create_app, lifespan
        print("[OK] Imports OK")
        
        app = create_app()
        print("[OK] App created")
        
        async with lifespan(app):
            print("[OK] Lifespan started")
            await asyncio.sleep(1)
            print("[OK] Lifespan test completed")
            
    except Exception as e:
        print("[ERROR]", e)
        import traceback
        traceback.print_exc()
        sys.exit(1)

asyncio.run(test_startup())
'''
]

result = subprocess.run(
    cmd,
    cwd='e:\\linewell\\program\\qgb1151521\\XHS_ALL_IN_ONE',
    capture_output=True,
    text=True,
    timeout=60
)

print("="*50)
print("STDOUT:")
print("="*50)
print(result.stdout)
print("\n" + "="*50)
print("STDERR:")
print("="*50)
print(result.stderr)
print("\n" + "="*50)
print("Return code:", result.returncode)
print("="*50)