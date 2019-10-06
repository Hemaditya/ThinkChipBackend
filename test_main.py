import widgets
import pathlib
path = pathlib.Path('./test_data/ENG')
ENG = widgets.ENG.ENG('ENG',path)
ENG.test_start_session('test',read_length=3)
