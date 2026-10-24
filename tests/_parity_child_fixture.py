"""Child modes used only to exercise parity observer mechanics offline."""
import os
from pathlib import Path
import sys
import time


mode = sys.argv[1]
if mode == "exit-124":
    os.write(2, b"measured stderr")
    raise SystemExit(124)
if mode == "timeout":
    os.write(2, b"before controlled timeout")
    time.sleep(10)
if mode == "unexpected-write":
    Path("unexpected-child-write.txt").write_bytes(b"unexpected")
    raise SystemExit(0)
if mode == "rewrite-revert":
    target = Path(sys.argv[2])
    original = target.read_bytes()
    target.write_bytes(original + b"changed")
    target.write_bytes(original)
    raise SystemExit(0)
raise SystemExit("unknown parity child fixture mode")
