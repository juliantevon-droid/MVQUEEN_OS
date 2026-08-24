MODULE_NAME = "health_check"
MODULE_VERSION = "1.0.0"


def boot():
    return {
        "module": MODULE_NAME,
        "version": MODULE_VERSION,
        "status": "ready",
    }


if __name__ == "__main__":
    print(boot())
