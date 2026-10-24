"""Child modes used only to exercise parity observer mechanics offline."""
import os
import sys
import time


mode = sys.argv[1]
if mode == "exit-124":
    os.write(2, b"measured stderr")
    raise SystemExit(124)
if mode == "timeout":
    os.write(2, b"before controlled timeout")
    time.sleep(10)
raise SystemExit("unknown parity child fixture mode")
