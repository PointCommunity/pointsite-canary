"""Extract only the exact reviewed public baseline for the initial Canary deployment."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import tarfile

root = Path(__file__).resolve().parent.parent
manifest = json.loads((root / "publication-baseline/manifest.json").read_text())
assert manifest["artifactDigest"] == "45562c9e111136f631c901892d2f1058e45050e93fa8d507f5beb0858eb68894"
files = manifest["files"]
assert len(files) == 97 and sum(item["bytes"] for item in files) == 2_792_441
assert [item["path"] for item in files] == sorted(set(item["path"] for item in files))
assert hashlib.sha256(json.dumps(files, sort_keys=True, separators=(",", ":")).encode()).hexdigest() == manifest["artifactDigest"]
packed = root / "publication-baseline/site.tar.gz"
assert hashlib.sha256(packed.read_bytes()).hexdigest() == "127a452216dde00aff67242db127cd1ec6c8807dce4e023a5b23f51365e41322"
output = root / "out"
output.mkdir(exist_ok=False)
with tarfile.open(packed, "r:gz") as archive:
    members = archive.getmembers()
    assert len(members) == len(files)
    for member, expected in zip(members, files):
        path = PurePosixPath(member.name)
        assert member.isfile() and not path.is_absolute() and ".." not in path.parts
        assert str(path) == member.name == expected["path"] and member.size == expected["bytes"]
        content = archive.extractfile(member).read(member.size + 1)
        assert len(content) == member.size and hashlib.sha256(content).hexdigest() == expected["sha256"]
        target = output.joinpath(*path.parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as destination:
            destination.write(content)
print(json.dumps({"filesVerified": len(files), "artifactDigest": manifest["artifactDigest"]}))
