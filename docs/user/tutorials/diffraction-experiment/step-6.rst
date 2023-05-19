Bluesky and Documents
=====================

From the previous page, you should have gotten some bluesky documents printed
to the terminal::
    {'doc': {'detectors': ['lunchbox'],
            'hints': {'dimensions': [(('time',), 'primary')]},
            'num_intervals': 0,
            'num_points': 1,
            'plan_args': {'detectors': ["LunchBox(prefix='', name='lunchbox', "
                                        "read_attrs=['camera', 'servo', 'led'], "
                                        'configuration_attrs=[])'],
                        'num': 1},
            'plan_name': 'count',
            'plan_type': 'generator',
            'scan_id': 2,
            'time': 1684422165.3099,
            'uid': '944e6388-934d-461e-94ec-21bdea397f87',
            'versions': {'bluesky': '1.10.0', 'ophyd': '1.7.0'}},
    'name': 'start'}
    {'doc': {'configuration': {'lunchbox': {'data': {},
                                            'data_keys': OrderedDict(),
                                            'timestamps': {}}},
            'data_keys': {'value': {'dtype': 'array',
                                    'object_name': 'lunchbox',
                                    'shape': [],
                                    'source': 'cv2 camera'}},
            'hints': {'lunchbox': {'fields': []}},
            'name': 'primary',
            'object_keys': {'lunchbox': ['value']},
            'run_start': '944e6388-934d-461e-94ec-21bdea397f87',
            'time': 1684422165.9069111,
            'uid': '9fbd795a-e94c-475b-b933-acb1465d31d9'},
    'name': 'descriptor'}
    {'doc': {'data': {'value': array([[[54, 58, 52], ...], ...], dtype=uint8)},
            'descriptor': '9fbd795a-e94c-475b-b933-acb1465d31d9',
            'filled': {},
            'seq_num': 1,
            'time': 1684422165.9224374,
            'timestamps': {'value': 1684422165.0},
            'uid': '6d0cc360-4655-418f-8021-b3e22736f2df'},
    'name': 'event'}
    {'doc': {'exit_status': 'success',
            'num_events': {'primary': 1},
            'reason': '',
            'run_start': '944e6388-934d-461e-94ec-21bdea397f87',
            'time': 1684422165.9394093,
            'uid': '0ee8edfd-a7b6-4db4-9aa4-7c21b81d68e8'},
    'name': 'stop'}

In the above, we have several kinds of documents emitted; start, descriptor,
event and stop documents. There is only one event document because our 
experiment in the previous step involved a `bluesky.plans.count` with `num=1`.

For this tutorial, we would like to run an experiment that turns on the laser,
shifts the angle of the diffraction grating, and takes a picture. We would like
to scan from 0 degrees to 45, taking pictures continuously.

This time, instead of just outputting the entire picture array in the event 
document, we can store this information in a hdf5 file and produce a resource
document specifying where this hdf5 file is stored. Each event document will
then contain a reference to a datum document uid, which will specify where in
the hdf5 file the results of this particular event are stored.

now, modify the lunchbox ophyd device so that it writes to a hdf5 file. To
do this, you will want to open the file for writing in the stage() method,
and close it in the unstage() method. Make this device a Triggerable and
add datum/resource factories...

modify the ophyd device previously so it emits the right kind of document.
Explain the event model briefly. Doesn't have to be up to date...

Then, write a bluesky plan.

This takes us to the next commit.

Checkout the next commit
------------------------

Type the following into a normal terminal::
    git checkout 8302cdf

(you'll need to pip install -e .[dev] again...)

You should now be able to, start the IOC, and then run the bluesky plan::
        python src/lunchbox/ioc.py

And in another terminal::
        python src/lunchbox/plan.py

You should see some bluesky event documents being emitted, and a "test.h5"
file appear in the root directory of the repository. Let's inspect it to see
the images::
        import numpy as np
        import matplotlib.pyplot as plt
        from h5py import File

        file = File("test.h5", "r")
        plt.imshow(np.array(file["/1"]))
        plt.show()

        file.close()

Ta-da!