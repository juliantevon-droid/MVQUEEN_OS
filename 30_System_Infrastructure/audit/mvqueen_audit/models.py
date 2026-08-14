from dataclasses import dataclass


@dataclass
class Finding:
    severity: str
    code: str
    message: str

    def format(self):
        return f"[{self.severity}] {self.code}: {self.message}"
