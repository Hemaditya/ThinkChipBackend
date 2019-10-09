from widgets.EyeBlink.EyeBlink import EyeBlink
import config

config.reset_filter_states()
mod = EyeBlink('./test_data',trails=20)
mod.collect()
