"""Helper code for pygst."""

# Import system modules.
import gst

# When using this module in a multi-thread/process program,
# need to initialize Python threading in gobject module first.
# Let's just do this always.
import gobject
gobject.threads_init()  


def create_gst_pipeline(specs):
    """Given a tuple or list of GStreamer specifications, each
    spec having three elements of format,
       (name, gst_element, properties)
    return three values:
       1) GStreamer pipeline
       2) dictionary of GStreamer elements
       3) string of GStreamer launch arguments
    """
    
    # Create pipeline and elements.
    pipeline = gst.Pipeline('hello')
    prev_element = None
    elements = dict()
    launch_args = ''
    for spec in specs:
        ekey = spec[0]
        etype = spec[1]
        eprops = spec[2]
        ename = '%s'%(ekey,)
        element = gst.element_factory_make(etype, ename)
        for prop in eprops:
            ptype = prop[0]
            pvalue = prop[1]
            if ptype == 'caps':
                pvalue = gst.Caps(pvalue)
            element.set_property(ptype, pvalue)
        pipeline.add(element)
        elements[ekey] = element

        # Link this element to the previous element.
        if prev_element:
            prev_element.link(element)
        prev_element = element

        # Append to the launch auguments string.
        if len(launch_args):
            launch_args += ' ! '
        launch_args += '%s '%etype
        for prop in eprops:
            launch_args += ' %s=%s '%(prop[0], prop[1])

    return (pipeline, elements, launch_args)

# The end.
