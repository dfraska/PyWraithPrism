from typing import List

from colour import Color


class ChannelValues:
    def __init__(self, values: List[int]):
        self._values = values
    
    @property
    def channel(self): return self._values[4]
    
    @property
    def speed(self): return self._values[5]
    
    @property
    def color_source(self): return self._values[6]

    @property
    def mode(self): return self._values[7]
    
    @property
    def brightness(self): return self._values[9]
    
    @property
    def color(self): return Color(rgb=(self._values[10]/255, self._values[11]/255, self._values[12]/255))
