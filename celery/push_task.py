from celery import group
from task import scan

g = group(scan.s(i, i) for i in range(10).apply_async(queue='test1'))
print(g.get())