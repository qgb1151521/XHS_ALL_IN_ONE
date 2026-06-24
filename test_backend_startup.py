import subprocess
import sys
import time

result = subprocess.run(
    [sys.executable, '-c', '''
import sys
try:
    from backend.app.main import app
    print("SUCCESS: Backend app created successfully")
except Exception as e:
    print(f"ERROR: Failed to create app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
'''],
    cwd='e:\\linewell\\program\\qgb1151521\\XHS_ALL_IN_ONE',
    capture_output=True,
    text=True,
    timeout=30
)

print("STDOUT:")
print(result.stdout)
print("\nSTDERR:")
print(result.stderr)
print("\nReturn code:", result.returncode)