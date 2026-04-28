from parsing.execution_engine.sandbox.temp_workspace import TempWorkspace

ws = TempWorkspace()

path = ws.create_file("test.py", "print('hello')")
print("Created:", path)

ws.cleanup()