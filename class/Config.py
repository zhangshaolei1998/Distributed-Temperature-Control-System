class Config:
    # 类属性
    mode = 0
    min_temp = 16
    max_temp = 30
    default_temp = 26
    min_speed = 0
    max_speed = 5
    default_speed = 1
    FeeRate_H = 2
    FeeRate_M = 1
    FeeRate_L = 0.5

    # 类方法
    @staticmethod
    def set_para(mode, min_temp, max_temp, default_temp, min_speed, max_speed, default_speed, rate_h, rate_m, rate_l):
        Config.mode = mode
        Config.min_temp = min_temp
        Config.max_temp = max_temp
        Config.default_temp = default_temp
        Config.min_speed = min_speed
        Config.max_speed = max_speed
        Config.default_speed = default_speed
        Config.FeeRate_H = rate_h
        Config.FeeRate_M = rate_m
        Config.FeeRate_L = rate_l
