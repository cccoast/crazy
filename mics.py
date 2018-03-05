import collections
import numpy as np
a = collections.OrderedDict(zip(map(str,np.random.randint(0,100,10)),range(10)))
for i in a:
    print a[i]