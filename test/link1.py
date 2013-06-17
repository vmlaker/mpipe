from mpipe import OrderedStage as OStage, Pipeline

def magnify(value):
    return value*10

p1 = Pipeline(
    OStage(magnify).link(
        OStage(magnify).link(
            OStage(magnify).link(
                OStage(magnify)
                )
            )
        )
    )
for val in list(range(10)) + [None]:
    p1.put(val)

for result in p1.results():
    print(result)
