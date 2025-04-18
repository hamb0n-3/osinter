class OSINTERError(Exception):
    pass


class ScanError(OSINTERError):
    pass


class ValidationError(OSINTERError):
    pass


class ConfigLoadError(OSINTERError):
    pass


class HttpCompareError(OSINTERError):
    pass


class DirectoryCreationError(OSINTERError):
    pass


class DirectoryDeletionError(OSINTERError):
    pass


class NTLMError(OSINTERError):
    pass


class InteractshError(OSINTERError):
    pass


class WordlistError(OSINTERError):
    pass


class CurlError(OSINTERError):
    pass


class PresetNotFoundError(OSINTERError):
    pass


class EnableModuleError(OSINTERError):
    pass


class EnableFlagError(OSINTERError):
    pass


class OSINTERArgumentError(OSINTERError):
    pass


class PresetConditionError(OSINTERError):
    pass


class PresetAbortError(PresetConditionError):
    pass


class OSINTEREngineError(OSINTERError):
    pass


class WebError(OSINTEREngineError):
    pass


class DNSError(OSINTEREngineError):
    pass


class ExcavateError(OSINTERError):
    pass
