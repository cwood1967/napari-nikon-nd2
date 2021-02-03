import numpy as np
from napari_nikon_nd2 import napari_get_reader


# tmp_path is a pytest fixture
def test_reader():

    tmp_path = "tmpData"
    # write some fake data using your supported file format
    my_test_file = "/".join([tmp_path, "test.nd2"])

    reader = napari_get_reader(my_test_file)
    assert callable(reader)

    # make sure we're delivering the right format
    layer_data_list = reader(my_test_file)
    assert isinstance(layer_data_list, list) and len(layer_data_list) > 0
    layer_data_tuple = layer_data_list[0]
    assert isinstance(layer_data_tuple, tuple) and len(layer_data_tuple) > 0

    # check for 3 channels
    assert layer_data_tuple[0].shape[0] == 3
    # check for 3-dimensions
    assert len(layer_data_tuple[0].shape) == 3
    print(len(layer_data_tuple))
    
def test_get_reader_pass():
    reader = napari_get_reader("fake.file")
    assert reader is None
