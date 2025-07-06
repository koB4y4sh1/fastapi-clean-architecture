class DomainException(Exception):
    """全ドメイン例外のベースクラス"""

class LLMServiceError(DomainException):
    """LLM処理に失敗したことを表す"""

class CustomAppException(DomainException):
    """アプリケーションレイヤーで発生した例外を表す"""