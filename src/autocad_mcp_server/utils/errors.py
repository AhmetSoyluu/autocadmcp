class AutoCADMCPError(Exception):
    pass


class SandboxViolation(AutoCADMCPError):
    pass


class PolicyViolation(AutoCADMCPError):
    pass


class ExecutableNotFound(AutoCADMCPError):
    pass


class AutoCADUnavailable(AutoCADMCPError):
    pass


class AutoCADHung(AutoCADMCPError):
    pass


class CoreConsoleTimeout(AutoCADMCPError):
    pass


class ToolExecutionFailure(AutoCADMCPError):
    pass
