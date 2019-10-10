from widgets.EyeBlink.EyeBlink import EyeBlink
import config

config.reset_filter_states()
mod = EyeBlink('./test_data',name="SingleBlinks",trails=60)
mod.collect(verbose=True)
