# 導入設定檔工具
from tools.module import Config

def main():
    # 讀取設定檔
    cfg = Config()
    
    # 若沒有檔案，則建立新檔
    if cfg.is_new_file:
        cfg.set_name("Default Module")
        cfg.set_version("1.0.0")
        cfg.set_inputs(["camera", "osc"])
        cfg.set_input_params("camera_id", 0)
        cfg.set_input_params("osc_address", "127.0.0.1")
        cfg.set_input_params("osc_port", "8000")
        cfg.set_outputs(["ndi"])
        cfg.set_output_params("ndi_name", "python_ndi")
        cfg.set_process(["resize", "binary"])
        cfg.set_process_params("resize_size", [640, 480])
        cfg.set_process_params("binary_threshold", 180)
    
    # 印出設定內容
    print(cfg.data)

    # TODO
    print("Hello from mdf-python!")
    print(cfg.get_inputs())
    print(cfg.get_input_params("camera_id"))
    print(cfg.get_input_params("osc_address"))
    print(cfg.get_input_params("osc_port"))
    print(cfg.get_outputs())
    print(cfg.get_output_params("ndi_name"))
    print(cfg.get_process())
    print(cfg.get_process_params("resize_size"))
    print(cfg.get_process_params("binary_threshold"))


if __name__ == "__main__":
    main()
