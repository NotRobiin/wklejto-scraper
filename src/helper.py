import helper_functions as hf


class Helper:
    def __init__(self, config) -> None:
        self.cfg = config
        self.failed = []
        self.protected = []

    def add_protected(self, site_id) -> None:
        if self.cfg.FRONT_END_TYPE == "disabled":
            return

        self.protected.append({"id": "site_id", "reason": "Password protected"})

    def add_fail(self, site_id, reason="") -> None:
        if self.cfg.FRONT_END_TYPE == "disabled":
            return

        self.failed.append({"id": site_id, "reason": reason})
