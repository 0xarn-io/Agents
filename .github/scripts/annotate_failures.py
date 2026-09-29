"""Turn unittest FAIL/ERROR blocks into GitHub Actions error annotations."""
import re
import sys

text = open(sys.argv[1], encoding="utf-8", errors="replace").read()
for block in re.split(r"\n={20,}\n", text)[1:]:
    head, _, body = block.partition("\n")
    lines = [line for line in body.strip().splitlines() if line.strip() and not line.startswith("---")]
    message = " | ".join(lines[-3:]).replace("%", "%25").replace("\r", "")
    print(f"::error title={head.strip()[:120]}::{message[:900]}")
