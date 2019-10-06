import widgets
import pathlib
path = pathlib.Path('./test_data/ENG')
ENG = widgets.ENG.ENG('ENG',path)
ENG.test_start_session('test',channels=[0,1],read_length=5)
