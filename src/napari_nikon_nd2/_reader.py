"""
This module is an import plugin for napari to read Nikon nd2 files.

"""
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import pathlib

import numpy as np
import nd2

PathLike = Union[str, List[str]]
LayerData = Union[Tuple[Any], Tuple[Any, Dict], Tuple[Any, Dict, str]]
ReaderFunction = Callable[[PathLike], List[LayerData]]

def get_reader(path: PathLike):
    
    if path.endswith(".nd2"):
        return reader_function
    
    return None


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

    ndx = nd2.ND2File(path)
    
    name = pathlib.Path(path).stem
    
    channel_axis=None
    for idx, s in enumerate(ndx.sizes.keys()):
        if s == "C":
            channel_axis=idx
            break
        
    vz = ndx.voxel_size().z
    vy = ndx.voxel_size().y
    vx = ndx.voxel_size().x
    
    if "Z" in ndx.sizes:
        scale = (vz, vy, vx)
    else:
        scale = (vy, vx)
    
    img = ndx.to_dask()
    
    if img.nbytes < 2_000_000_000:
        img = img.compute()
    
    ndx.close()
    
    params = {
        "channel_axis": channel_axis,
        "scale": scale,
        "name":name,
    }
    layer_type = "image"  # optional, default is "image"

    return [(img, params, layer_type)]
