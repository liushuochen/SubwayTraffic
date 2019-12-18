import conductor.user
import traceback

if __name__ == '__main__':
    try:
        uuid = "wdf8wid9-qnd4-efb2-3rdqwj31"
        conductor.user.check_verify_code(uuid)
        print("check success")
    except Exception:
        print(traceback.format_exc())