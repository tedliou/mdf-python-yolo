# 導入設定檔工具
from tools.module import Config
from ultralytics import YOLO
from pythonosc import udp_client
import cv2
import time

def main():
    # 讀取設定檔
    cfg = Config()
    
    # 若沒有檔案，則建立新檔
    if cfg.is_new_file:
        cfg.set_name("YOLO Module")
        cfg.set_version("1.0.0")
        cfg.set_inputs(["camera"])
        cfg.set_input_params("camera_id", 0)
        cfg.set_outputs(["osc"])
        cfg.set_output_params("osc_address", "127.0.0.1")
        cfg.set_output_params("osc_port", 5005)
        cfg.set_output_params("osc_path", "/pose")
        cfg.set_process(["resize", "flip", "yolo-pose"])
        cfg.set_process_params("resize_size", [640, 640])
        cfg.set_process_params("flip_mode", "x")
        cfg.set_process_params("yolo_model", "yolo11n-pose.pt")

    # TODO: 取得輸入參數
    if "camera" in cfg.get_inputs():
        camera_id = cfg.get_input_params("camera_id")
    else:
        print("找不到可用的輸入方法")
        return

    # TODO: 取得輸出參數
    if "osc" in cfg.get_outputs():
        osc_address = cfg.get_output_params("osc_address")
        osc_port = cfg.get_output_params("osc_port")
        osc_path = cfg.get_output_params("osc_path")
    else:
        print("找不到可用的輸出方法")
        return
    
    # TODO: 取得處理參數
    process = cfg.get_process()
    if "resize" in process:
        resize_size = cfg.get_process_params("resize_size")
    if "flip" in process:
        flip_mode = cfg.get_process_params("flip_mode")

    # TODO: 初始化 YOLO
    if "yolo-pose" in process:
        model_name = cfg.get_process_params("yolo_model")
        model = YOLO(model_name)
    else:
        print("找不到可用的 YOLO 參數")
        return
    
    # TODO: 初始化 OSC
    osc_client = udp_client.SimpleUDPClient(osc_address, osc_port)

    # TODO: 主循環
    try:
        while True:
            # 啟動攝影機
            camera = cv2.VideoCapture(camera_id, cv2.CAP_ANY)
            if camera is None or not camera.isOpened():
                camera.release()
                print("攝影機連線失敗，將於 1 秒後重試")
                time.sleep(1)
                continue
            print("已連接攝影機")

            # 讀取攝影機影像
            while True:
                ret, frame = camera.read()
                if not ret:
                    # 失去攝影機連線，釋放資源並於 1 秒後嘗試重連
                    camera.release()
                    cv2.destroyAllWindows()
                    print("與攝影機失去連線，將於 1 秒後重試")
                    time.sleep(1)
                    break

                else:
                    # 影像尺寸調整
                    if "resize" in process:
                        frame = cv2.resize(frame, (resize_size[0], resize_size[1]))

                    # 影像翻轉
                    if "flip" in process:
                        if flip_mode == "x":
                            flip_code = 1
                        if flip_mode == "y":
                            flip_code = 0
                        if flip_mode == "xy":
                            flip_code = -1
                        frame = cv2.flip(frame, flip_code)

                    # YOLO 推論
                    yolo_res = model(frame)
                    for r in yolo_res:
                        # 轉換成 JSON 並以 OSC 傳送
                        res_json = r.to_json(normalize=True)
                        osc_client.send_message(osc_path, res_json)

                # 加入短暫延遲
                cv2.waitKey(1)

    except KeyboardInterrupt:
        print("停止 YOLO 模組")

    except Exception as e:
        print("發生未知錯誤")
        print(e)

    finally:
        if camera is not None:
            camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
