import os, glob
for f in glob.glob('/app/working/shared/showcase/append_part*.py'):
    os.remove(f)
for f in glob.glob('/app/working/shared/showcase/build_report.py'):
    os.remove(f)
for f in glob.glob('/app/working/shared/showcase/validate.py'):
    os.remove(f)
print("Cleanup done")
