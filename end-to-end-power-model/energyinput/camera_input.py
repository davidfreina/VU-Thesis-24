import psutil

from .generic_input import GenericInput

class CameraInput(GenericInput):
    # p_idle from https://doi.org/10.1145/2462456.2464448
    # p_coefficient, p_idle_enc, p_coefficient_enc from https://doi.org/10.1016/j.sysarc.2017.10.001
    def __init__(self, p_idle: float = 0.22, p_idle_enc: float = 0.5, p_coefficient: float = 0.000000065, p_coefficient_enc: float = 0.000000017, resolution_h: int = 720, resolution_w: int = 1280, fps: int = 5):
        super().__init__()
        self.p_idle = p_idle
        self.p_idle_enc = p_idle_enc
        self.p_coefficient_enc = p_coefficient_enc
        self.p_coefficient = p_coefficient
        self.res_h = resolution_h
        self.res_w = resolution_w
        self.fps = fps
        self.previous_energy = self.get_energy()
        self.active = False

    def __str__(self):
        return "CameraModel"

    def get_energy(self) -> float:
        cam_e = 0
        for proc in psutil.process_iter(["name", "username"]):
            if "publisher.py" in proc.cmdline():
                self.active = True
                pixel_per_second = self.res_w * self.res_h * self.fps
                cam_e = ((self.p_coefficient * pixel_per_second + self.p_idle) +
                         (self.p_coefficient_enc * pixel_per_second + self.p_idle_enc))
            else:
                self.active = False
        return cam_e

    def get_utilization(self) -> bool:
        return self.active
