def envelope(success: bool, data=None, error=None, message: str = ""):
    if not success:
        primero = error[0] if isinstance(error, list) and error else {}
        return {"error": {"code": primero.get("code", "APPLICATION_ERROR"),
                          "message": message,
                          "details": error or []}}
    return {"success": True, "data": data, "error": None, "message": message}
