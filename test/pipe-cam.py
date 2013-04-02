#!/usr/bin/env python

import multiprocessing
import sharedmem
import numpy
import cv2
import gst

import datetime
import time
import sys

import mpipe

import util

# Retrieve command line arguments.
try:
    DEVICE   = sys.argv[1]
    WIDTH    = int(sys.argv[2])
    HEIGHT   = int(sys.argv[3])
    DEPTH    = int(sys.argv[4])
    DURATION = float(sys.argv[5])
    try:
        HOST = sys.argv[6]
        PORT = int(sys.argv[7])
    except:
        HOST = None
        PORT = None
except:
    print('Usage:  %s device width height depth duration [ host port ]'%sys.argv[0])
    sys.exit(1)


# Create process-shared tables, 
# one holding allocated memories keyed on timestamp,
# another holding other common process-shared values.
manager = multiprocessing.Manager()
memories = manager.dict()
common = manager.dict()

# Initialize the common accumulated image to None, 
# indicating that analysis hasn't started yet.
common['image_acc'] = None


class Allocator(mpipe.OrderedWorker):
    """Allocates shared memory to be used in the remainder of pipeline."""
    def doTask(self, task):
        try:
            tstamp = datetime.datetime.now()

            # Allocate shared memory for
            #   a copy of the input image,
            #   the preprocessed image,
            #   the diff image,
            #   the postprocessed image,
            #   the resulting output image.
            shape = numpy.shape(task['image_in'])
            dtype = task['image_in'].dtype
            image_in   = sharedmem.empty(shape,     dtype)
            image_pre  = sharedmem.empty(shape[:2], dtype)
            image_diff = sharedmem.empty(shape[:2], dtype)
            image_post = sharedmem.empty(shape[:2], dtype)
            image_out  = sharedmem.empty(shape,     dtype)

            # Copy the input image to it's shared memory version,
            # and also to the eventual output image memory.
            image_in[:] = task['image_in'].copy()
            image_out[:] = task['image_in'].copy()

            # Store all allocated memory in the table because
            # we will later explicitly deallocate the memory.
            index = task['tstamp_onbuffer1']
            memories[index] = (
                image_in, 
                image_pre, 
                image_diff, 
                image_post,
                image_out,
                )

            # Retrieve the common accumulated image.
            image_acc = common['image_acc']

            # If this is the first task through the pipeline 
            # (indicated by the accumulated image being None),
            # then allocate shared memory for accumulated image
            # and set the accumulation alpha value to 100%.
            if image_acc is None:
                # Allocate shared memory for the accumulator image.
                image_acc = sharedmem.zeros(numpy.shape(image_pre))
                cv2.accumulateWeighted(image_pre, image_acc, 1.000)
                common['image_acc'] = image_acc
                alpha = 1.0  # Initially transparency is zero.

            # Otherwise compute accumulation alpha value based 
            # on time elapsed since the previous task.
            else:
                tdelta = task['tstamp_onbuffer1'] - common['prev_tstamp']
                alpha = tdelta.total_seconds()
                alpha *= 0.50  # 1/2.

            common['prev_tstamp'] = task['tstamp_onbuffer1']

            # Prepare the task for the next stage.
            task['image_in'] = image_in
            task['image_pre'] = image_pre
            task['image_diff'] = image_diff
            task['image_post'] = image_post
            task['image_out'] = image_out
            task['alpha'] = alpha

            task['tstamp_alloc1'] = tstamp
            task['tstamp_alloc2'] = datetime.datetime.now()

        except:
            print('error running allocator !!!')

        self.putResult(task)


class Preprocessor(mpipe.OrderedWorker):
    """Filters the given image."""
    def doTask(self, task):
        try:
            tstamp = datetime.datetime.now()
            cv2.cvtColor(
                task['image_in'], 
                cv2.COLOR_BGR2GRAY, 
                task['image_pre'],
                )
            cv2.equalizeHist(
                task['image_pre'],
                task['image_pre'],
                )
            task['tstamp_pre1'] = tstamp
            task['tstamp_pre2'] = datetime.datetime.now()
        except:
            print('error running preprocessor !!!')

        return task


class DiffAndAccumulator(mpipe.OrderedWorker):
    """Performs diff and accumulation."""
    def doTask(self, task):
        try:
            tstamp = datetime.datetime.now()

            # Compute the difference.
            cv2.absdiff(
                common['image_acc'].astype(task['image_pre'].dtype), 
                task['image_pre'],
                task['image_diff'],
                )

            task['tstamp_diff1'] = tstamp
            task['tstamp_diff2'] = datetime.datetime.now()

            # Allow the next stage in the pipeline to begin work on the result.
            self.putResult(task)

            # Accumulate images.
            hello = cv2.accumulateWeighted(
                task['image_pre'],
                common['image_acc'],
                task['alpha'],
                )
        except:
            print('error running accumulator !!!')


class Postprocessor(mpipe.OrderedWorker):
    """Pipeline element that augments original image."""
    def doTask(self, task):
        try:
            tstamp = datetime.datetime.now()

            cv2.threshold(
                task['image_diff'],
                thresh=35,
                maxval=255,
                type=cv2.THRESH_BINARY,
                dst=task['image_post'],
                )

            # Find contours.
            contours, hier = cv2.findContours(
                task['image_post'],
                #numpy.copy(image_diff),
                #mode=cv2.RETR_LIST,
                mode=cv2.RETR_EXTERNAL,
                method=cv2.CHAIN_APPROX_NONE,
                #method=cv2.CHAIN_APPROX_SIMPLE,
                )        

            # Sort and filter contours.
            area_threshold = task['image_post'].shape[0] * task['image_post'].shape[1]
            area_threshold *= 0.00005 /2
            contours = sorted(
                contours, 
                key=lambda x: cv2.contourArea(x), 
                reverse=True)
            contours_filt = []
            for contour in contours:
                area = cv2.contourArea(contour)

                # Since contours are sorted, we can safely break out 
                # of the loop once area falls below threshold.
                if area < area_threshold:
                    break

                # Add this contour to the collection.
                contours_filt.append(contour)

            # Augment output image with contours.
            cv2.drawContours(
                task['image_out'],
                contours_filt,
                -1,
                color=(0, 254, 254),  # Yellow.
                thickness=2,
                )

            # Augment output image with rectangles.
            if 0: #for contour in contours_filt:
                x,y,w,h = cv2.boundingRect(contour)
                cv2.rectangle(
                    task['image_out'],
                    (x,y),
                    (x+w,y+h),
                    color=(0, 254, 0),
                    thickness=2,
                    )
            task['tstamp_post1'] = tstamp
            task['tstamp_post2'] = datetime.datetime.now()
        except:
            print('error running postprocessor !!!')

        return task


class Sender(mpipe.OrderedWorker):
    """Sends processed image on a network socket."""
    def __init__(self, input_tube, output_tube):
        super(Sender, self).__init__(input_tube, output_tube)

        # Attempt to make a connection.
        try:
            print('connecting to %s:%s'%(HOST, PORT))
            self.client = multiprocessing.connection.Client((HOST, PORT))
            print('connected')
        except:
            self.client = None
            print('failed to connect, nevermind')

    def doTask(self, task):
        try:
            tstamp = datetime.datetime.now()
            if self.client is not None:
                shape = numpy.shape(task['image_out'])
                message = (
                    task['tstamp_onbuffer1'],
                    shape,
                    task['image_out'],
                    )
                self.client.send(message)
            task['tstamp_send1'] = tstamp
            task['tstamp_send2'] = datetime.datetime.now()
        except:            
            print('error running sender !!!')

        return task


class Printer(mpipe.OrderedWorker):
    """Prints some useful info to standard output."""
    def doTask(self, task):
        try:
            task['tstamp_print1'] = datetime.datetime.now()

            tworkers = 0.0
            tgaps = 0.0

            # Assemble the timings string.
            timings = ''
            specs = (
                ('tstamp_onbuffer1', 'tstamp_onbuffer2'),
                ('tstamp_onbuffer2', 'tstamp_alloc1'),
                ('tstamp_alloc1',    'tstamp_alloc2'),
                ('tstamp_alloc2',    'tstamp_pre1'),
                ('tstamp_pre1',      'tstamp_pre2'),
                ('tstamp_pre2',      'tstamp_diff1'),
                ('tstamp_diff1',     'tstamp_diff2'),
                ('tstamp_diff2',     'tstamp_post1'),
                ('tstamp_post1',     'tstamp_post2'),
                ('tstamp_post2',     'tstamp_print1'),
                )
            for element in specs:
                elapsed = -(task[element[0]] - task[ element[1]]).total_seconds()

                # Even indexes are for work in stages.
                if specs.index(element)%2 == 0:
                    timings += '(%0.3f) '%elapsed
                    tworkers += elapsed
                # Odd indexes are for gaps (i.e. communication) between stages.
                else:
                    timings += '%0.3f '%elapsed
                    tgaps += elapsed

            # Dump to standard output.
            print('%s  elapsed= %0.3f (%0.3f + %0.3f) pipe= %s fps= %s'%(
                task['tstamp_onbuffer1'], 
                tworkers + tgaps,
                tworkers,
                tgaps,
                timings,
                task['fps_onbuffer'],
                ))

        except:
            print('error running printer !!!')

        return task


class Viewer(mpipe.OrderedWorker):
    def doTask(self, task):
        try:
            name = self.getName()
            cv2.namedWindow(name, cv2.cv.CV_WINDOW_NORMAL)
            cv2.imshow(name, task[name])
            cv2.waitKey(1)
        except:
            print('error running viewer %s !!!'%self.getName())
        return task

class ViewerIn(Viewer):
    def getName(self):
        return 'image_in'
class ViewerPre(Viewer):
    def getName(self):
        return 'image_pre'
class ViewerDiff(Viewer):
    def getName(self):
        return 'image_diff'
class ViewerPost(Viewer):
    def getName(self):
        return 'image_post'
class ViewerOut(Viewer):
    def getName(self):
        return 'image_out'


class ImageProcessor(mpipe.Pipeline):
    """Deletes shared memory upon get()."""
    def get(self):
        result = super(ImageProcessor, self).get()
        if result is None:
            return None
        
        # Deleting elements from the inter-process (shared) dictionary
        # eventually leads to deallocation of shared memory: 
        # once the dictionary is synced on the process that owns the memory, 
        # the owning process loses reference to the memory and 
        # deallocation is delegated to the garbage collector.
        index = result['tstamp_onbuffer1']
        del memories[index]

        return result


class Streamer(multiprocessing.Process):
    """Streams video, feeding the image processor with incoming frames."""

    def __init__(self, iprocessor):
        """Initialize the object with the given image processor."""
        super(Streamer, self).__init__()

        # Assemble the video stream pipeline.
        specs = [
            ('source','v4l2src'          ,[('device', DEVICE), ]),
            ('color' ,'ffmpegcolorspace' ,[] ),
            ('scale' ,'videoscale'       ,[] ),
            ('filter','capsfilter', [
                    ('caps', 'video/x-raw-rgb,width=%s,height=%s,bpp=%s'%(WIDTH, HEIGHT, DEPTH*8)),
                    ]),
            ('fake', 'fakesink', []),
            ]
        (self.vpipe,
         elements,
         launch_args,) = util.create_gst_pipeline(specs)

        # Add the buffer probe on the last element.
        pad = next(elements['fake'].sink_pads())
        pad.add_buffer_probe(self.onVideoBuffer, iprocessor)

        # Communication channel to signal the "stop" message.
        self._comm_tube = mpipe.TubeP()

        # Keep track of rates (i.e. frames per second)
        # during the past 1, 5 and 10 seconds.
        self.rticker = util.RateTicker((1,5,10))

    def run(self):
        """Start streaming, wait to receive the "stop" message 
        from client, then stop streaming."""
        self.vpipe.set_state(gst.STATE_PLAYING)
        self._comm_tube.get()
        self.vpipe.set_state(gst.STATE_NULL)

    def stop(self):
        """Send the "stop" message."""
        self._comm_tube.put(True)

    def onVideoBuffer(self, pad, idata, iprocessor):
        """Send incoming image data to the image processor."""
        tstamp = datetime.datetime.now()
        image = numpy.ndarray(
            shape=(HEIGHT, WIDTH, DEPTH), 
            dtype=numpy.uint8, 
            buffer=idata,
            )
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        task = {}
        task['image_in'] = image
        task['fps_onbuffer'] = '%05.3f, %05.3f, %05.3f'%self.rticker.tick()
        task['tstamp_onbuffer1'] = tstamp
        task['tstamp_onbuffer2'] = datetime.datetime.now()
        iprocessor.put(task)
        #time.sleep(0.100)
        return True


class Getter(multiprocessing.Process):
    """Pulls results from the image processor."""

    def __init__(self, iprocessor):
        """Initialize the object with the given image processor."""
        super(Getter, self).__init__()
        self._iprocessor = iprocessor

    def run(self):
        """Keep fetching the latest result from the image processor
        until the processor has quit."""
        while True:
            result = self._iprocessor.get()
            if result is None: break                


# Create stages of for the image processing pipeline.
NUM_WORKERS = 4
specs = (
    (Allocator          ,NUM_WORKERS),
    (Preprocessor       ,NUM_WORKERS),
    (DiffAndAccumulator ,1          ),
    (Postprocessor      ,NUM_WORKERS),
    (Printer            ,1          ),
    (ViewerIn           ,1          ),
    (ViewerPre          ,1          ),
    (ViewerDiff         ,1          ),
    (ViewerPost         ,1          ),
    (ViewerOut          ,1          ),
    )
stages = [mpipe.Stage(x,y) for x,y in specs]

# Link the stages.
stages[0].link(stages[1])
stages[1].link(stages[2])
stages[2].link(stages[3])
stages[3].link(stages[4])
#stages[0].link(stages[5])
#stages[1].link(stages[6])
#stages[2].link(stages[7])
#stages[3].link(stages[8])
stages[3].link(stages[9])

# Create the image processor.
iprocessor = ImageProcessor(stages[0])

# Create streamer and getter.
streamer = Streamer(iprocessor)
getter = Getter(iprocessor)

# Start the streamer and getter.
streamer.start()
getter.start()

# Run for designated duration period.
print('sleeping for %s seconds'%DURATION)
time.sleep(DURATION)

# Shutdown all the pieces.
print('stopping streamer')
streamer.stop()
print('joining streamer')
streamer.join()
print('stopping iprocessor')
iprocessor.put(None)
print('joining getter')
getter.join()

print('the end')

# The end.
