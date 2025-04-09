from choon import datacache

class Animation(object):

    def __init__(self, duration, frames):
        self.frames = frames
        self.frame_duration = duration / len(frames)
        self.color = None
        self.current_frame = 0
        self.interval = 0
        self.loops = 0
        self.callback = None
        return

    def update(self, interval):
        if self.loops != 0:
            self.interval += interval
            if self.interval >= self.frame_duration:
                if self.current_frame == len(self.frames) - 1:
                    self.current_frame = 0
                    self.loops -= 1
                    if self.loops == 0:
                        self.callback()
                else:
                    self.current_frame += 1
                self.interval -= self.frame_duration

    def play(self, loops, callback=None):
        self.current_frame = 0
        self.interval = 0
        self.loops = loops
        self.callback = callback

    @property
    def frame(self):
        if self.color:
            return datacache.get_image((self.frames[self.current_frame], self.color))
        else:
            return datacache.get_image(self.frames[self.current_frame])
