from abc import ABC, abstractmethod


class GpuBuilder(ABC):
    """Abstract base class for all device builders"""


    @abstractmethod
    def get_gpu_temperature(self):
        """Collect GPU temperature from the device"""
        pass


    @abstractmethod
    def get_gpu_frequency(self):
        """Collect GPU frequency from device"""
        pass
    #
    # @abstractmethod
    # def get_throttle_reason(self):
    #     """Collect throttle reason from device"""
    #     pass
    #
    #
    # @abstractmethod
    # def get_gpu_memory(self):
    #     """Collect information on GPU VRAM"""
    #     pass