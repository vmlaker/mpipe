import mpipe

def echo(value):
    print(value)

stage = mpipe.OrderedStage(echo)
pipe = mpipe.Pipeline(stage)

for val in (0, 1, 2, 3):
    pipe.put(val)

pipe.put(None)  # Stop the pipeline.
