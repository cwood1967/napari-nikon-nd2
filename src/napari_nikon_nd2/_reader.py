"""
This module is an import plugin for napari to read Nikon nd2 files.

It implements the ``napari_get_reader`` hook specification, (to create
a reader plugin). 
see: https://napari.org/docs/dev/plugins/hook_specifications.html
"""
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import os

import numpy as np
from nd2reader import ND2Reader
from napari_plugin_engine import napari_hook_implementation

PathLike = Union[str, List[str]]
LayerData = Union[Tuple[Any], Tuple[Any, Dict], Tuple[Any, Dict, str]]
ReaderFunction = Callable[[PathLike], List[LayerData]]

@napari_hook_implementation
def napari_get_reader(path: Union[str, List[str]]) -> Optional[ReaderFunction]:
    """A basic implementation of the napari_get_reader hook specification.

    Parameters
    ----------
    path : str or list of str
        Path to file, or list of paths.

    Returns
    -------
    function or None
        If the path is a recognized format, return a function that accepts the
        same path or list of paths, and returns a list of layer data tuples.
    """
    if isinstance(path, list) and path.endswith('.nd2'):
        path = path[0] 

    # if we know we cannot read the file, we immediately return None.
    if not path.endswith(".nd2"):
        return None

    # otherwise we return the *function* that can read ``path``.
    return reader_function


def reader_function(path):

    '''Read a Nikon ND2 file
    
    Parameters
    ----------
    path : str
        Path to the image to open
        
    Returns
    -------
    layer_data : list of tuples
        A list of LayerData tuples where each tuple in the list contains
        (data, metadata, layer_type), where data is a numpy array, metadata is
        a dict of keyword arguments for the corresponding viewer.add_* method
        in napari, and layer_type is a lower-case string naming the type of layer.
    '''

    ndx = ND2Reader(path)
    name = os.path.basename(path)[:-4]
    sizes = ndx.sizes
    
    if 't' not in sizes:
        sizes['t'] = 1
    if 'z' not in sizes:
        sizes['z'] = 1
    if 'c' not in sizes:
        sizes['c'] = 1

    ndx.bundle_axes = 'zcyx'
    ndx.iter_axes = 't'
    n = len(ndx)

    shape = (sizes['t'], sizes['z'], sizes['c'], sizes['y'], sizes['x'])
    image  = np.zeros(shape, dtype=np.float32)

    for i in range(n):
        image[i] = ndx.get_frame(i)

    image = np.squeeze(image)
    
    if sizes['c'] > 1:
        channel_axis = len(image.shape) - 3
    else:
        channel_axis = None 
    params = {
        "channel_axis":channel_axis,
        "name":name,
    }
    layer_type = "image"  # optional, default is "image"

    return [(image, params, layer_type)]
