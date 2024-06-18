class CustomLogger:
    def __init__(self, logger):
        self._logger = logger
        self.success = True
        self.errors = []
        self.logs = []

    def log_error(self, error: str):
        self.success = False
        self.errors.append(error)
        self.logs.append(f"Error {error}")
        self._logger.error(error)

    def log_info(self, info: str):
        self.logs.append(info)
        self._logger.info(info)

    def get_result_dict(self):
        return {"success": self.success, "errors": self.errors, "logs": self.logs}
