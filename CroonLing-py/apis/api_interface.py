from abc import ABC, abstractmethod

# 공통 인터페이스 정의
class APIInterface(ABC):
    @abstractmethod
    def request(self, *args, **kwargs):
        """API 요청을 처리하는 메서드 (추상 메서드)"""
        pass
