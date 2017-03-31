import pandas as pd
import numpy as np
import sys
import re

OUTPUT_FILE = 'sample.proto'

# DictNameID dict()
# DictFanType dict()
# DictMode dict()

def init_file():
    file = open(OUTPUT_FILE, 'wb')
    file.write('syntax = "proto3";\n')
    file.write('syntax = "package asus.fan;"\n\n')
    file.close
    
    
def find_control_position(df):
    tmp = df['Main Table'] == 'EX.'
    first = np.where(tmp)[0] + 1
    tmp = df['Main Table'] == 'End Table'    
    last = np.where(tmp)[0] - 1
    return (int(first), int(last))

def generate_enum_items(df, col_title, enum_name):
    text = df[col_title][0]
    items = [s.strip('.').split(': ') for s in text.splitlines()]
    
    with open(OUTPUT_FILE, "a") as f:
        f.write('\nenum ' + enum_name + '\n{\n')
        for index, item in enumerate(items):
            f.write('\t')
            f.write(re.sub('[\s+|\.]', '_', items[index][1]).upper())
            f.write(' = ')
            f.write(items[index][0])
            f.write(';\n')
        f.write('}\n')
        f.close
    
def generate_fan_contorl_rpm_mode(df, first, last):
    for index in range(first, last + 1):
        version = df['Version'][index]
        id = df['ID'][index]
        name = df['NAME'][index]
        name_id = df['NAME ID'][index]
        sio = df['fan type & SIO mapping'][index]
        ec =  df['EC mapping reg'][index]
        with open(OUTPUT_FILE, "a") as f:
            f.write('\nmessage Fan_Control_RPM_Mode\n{\n')
            f.write('\tstring	Version = ' + str(version) + ';\n')
            f.write('\tint32	Control_id = ' + str(id) + ';\n')
            f.write('\tstring	Fanname = ' + str(name) + ';\n')
            f.write('\tNameId	Fannameid = ' + str(name_id) + ';\n')
            f.write('\tuint64	Fantype_SIOMapping = ' + str(sio) + ';\n')
            f.write('\tint32	EC_BANK = ' + str(ec) + ';\n')
            f.write('\tuint64	Reg_High = ' + '?' + ';\n')
            f.write('\tuint64	Reg_Low = ' + '?' + ';\n')
            f.write('\tuint64	EC_Mapping = ' + '?' + ';\n')
            f.write('\tint32	ControlSupport = ' + '?' + ';\n')                
            f.write('}\n')
            f.close
    
def generate_fan_contorl_auto_mode(df, first, last):
    for index in range(first, last + 1):
        version = df['Version'][index]
        id = df['ID'][index]
        name = df['NAME'][index]
        name_id = df['NAME ID'][index]
        sio = df['fan type & SIO mapping'][index]
        ec =  df['EC mapping reg'][index]
        group = df['F6 Group NO'][index]
        default_mode = df['Default mode'][index]
        mode_pin_type = df['ModePinType'][index]
        mode_pin_pch_gpio_group = df['ModePin PCH GPIO Group'][index]        
        pch_or_sio_mode_pin = df['PCH ModePin/ SIO_ModePin'][index]
        mode_pin_ec_bank = df['ModePin_EC_bank'][index]
        mode_pin_ec_reg = df['ModePin_EC_Reg'][index]
        mode_pin_ec_reg_bit = df['ModePin_EC_Reg_Bit'][index]
        auto_detect_support = df['AutoDetectSupport'][index]
        detect_pin_type = df['DetectPinType'][index]
        detect_pin_pch_gpio_group = df['DetectPin PCH GPIO Group'][index]
        pch_detect_pin_sio_detect_pin = df['PCH_DetectPin/ SIO_DetectPin'][index]
        detect_pin_ec_bank = df['DetectPin_EC_bank'][index]
        detect_pin_ec_reg = df['DetectPin_EC_Reg'][index]
        detect_pin_ec_reg_bit = df['DetectPin_EC_Reg_Bit'][index]
        eq_mode_support = df['EQModeSupport'][index]
        dual_mode_pin_type = df['DualModePinType'][index]
        daul_mode_pin_pch_gpip_group = df['DualModePin PCH GPIO Group'][index]
        pch_dual_mode_pin_sio_dual_mode_pin = df['PCH_DualModePin/ SIO_DualModePin'][index]
        dual_mode_pin_ec_bank = df['DualModePin_EC_bank'][index]
        dual_mode_pin_ec_reg = df['DualModePin_EC_Reg'][index]
        dual_mode_pin_ec_reg_bit = df['DualModePin_EC_Reg_Bit'][index]
        multi_source_support = df['MultiSource Support'][index]
        temperature_source_enable_0 = df['TEMPERATURE_SOURCE_ENABLE_0'][index]
        temperature_source_enable_1 = df['TEMPERATURE_SOURCE_ENABLE_1'][index]
        temperature_source_enable_2 = df['TEMPERATURE_SOURCE_ENABLE_2'][index]
        temperature_source_enable_3 = df['TEMPERATURE_SOURCE_ENABLE_3'][index]
        fan_over_time_support = df['Fan Over Time Support'][index]
        fan_inverse_support = df['Fan Inverse Support'][index]
        fan_off_support = df['FanOffSupport'][index]

        step_up_down_support = df['StepUp/downSupport'][index]
        step_up = df['StepUp'][index]
        step_down = df['StepDown'][index]
        dc_upper_temperature = df['DCUpper Temperature'][index]
        dc_max_duty_cycle = df['DCMax DutyCycle'][index]
        dc_middle_temperature = df['DCMiddle Temperature'][index]
        dc_middle_duty_cycle = df['DCMiddle DutyCycle'][index]
        dc_lower_temperature = df['DCLower Temperature'][index]
        dc_min_duty_cycle = df['DCMin DutyCycle'][index]
        pwm_upper_temperature = df['PWMUpper Temperature'][index]
        pwm_max_duty_cycle = df['PWMMax DutyCycle'][index]
        pwm_middle_temperature = df['PWMMiddle Temperature'][index]
        pwm_middle_duty_cycle = df['PWMMiddle DutyCycle'][index]
        pwm_lower_temperature = df['PWMLower Temperature'][index]
        pwm_min_duty_cycle = df['PWMMin DutyCycle'][index]
        speed_low_limit = df['SpeedLowLimit'][index]
        qfan_tuning_suport = df['Q-Fan Turning Support'][index]

        with open(OUTPUT_FILE, "a") as f:
            f.write('\nmessage Fan_Control_Auto_Mode\n{\n')
            f.write('\tstring	Version = ' + str(version) + ';\n')
            f.write('\tint32	Control_id = ' + str(id) + ';\n')  
            f.write('\tstring	Fanname = ' + str(name) + ';\n')
            f.write('\tNameId	Fannameid = ' + str(name_id) + ';\n')
            f.write('\tuint64	Fantype_SIOMapping = ' + str(sio) + ';\n')
            f.write('\tuint64	ECMappingReg = ' + str(ec) + ';\n')
            f.write('\tint32	F6GroupNO = ' + str(group) + ';\n')
            f.write('\tFANControl_Mode			Defaultmode = ' + str(default_mode) + ';\n')
            f.write('\tFANModePin_Type			ModePintype = ' + str(mode_pin_type) + ';\n')	
            f.write('\tModePin_PCH_GPIO_Group	ModePinPCHGPIO_group = ' + str(mode_pin_pch_gpio_group) + ';\n')
            f.write('\tint32	PCH_or_SIO_ModePin = ' + str(pch_or_sio_mode_pin) + ';\n')
            f.write('\tint32	ModePin_EC_bank = ' + str(mode_pin_ec_bank) + ';\n')
            f.write('\tint32	ModePin_EC_Reg = ' + str(mode_pin_ec_reg) + ';\n') 
            f.write('\tint32	ModePin_EC_Reg_Bit = ' + str(mode_pin_ec_reg_bit) + ';\n')
            f.write('\tbool	AutoDetectSupport = ' + str(auto_detect_support) + ';\n')
            f.write('\tFANModePin_Type			DetectPintype = ' + str(detect_pin_type) + ';\n')	
            f.write('\tModePin_PCH_GPIO_Group	DetectPinPCHGPIO_group = ' + str(detect_pin_pch_gpio_group) + ';\n')
            f.write('\tint32	PCH_or_SIO_DetectPin = ' + str(pch_detect_pin_sio_detect_pin) + ';\n')
            f.write('\tint32	DetectPin_EC_bank = ' + str(detect_pin_ec_bank) + ';\n')
            f.write('\tint32	DetectPin_EC_Reg = ' + str(detect_pin_ec_reg_bit) + ';\n') 
            f.write('\tint32	DetectPin_EC_Reg_Bit = ' + str(detect_pin_ec_reg_bit) + ';\n')
            f.write('\tEQ_Mode_ControlType		EQModeSupport = ' + str(eq_mode_support) + ';\n')
            f.write('\tFANModePin_Type			DualModePinType = ' + str(dual_mode_pin_type) + ';\n')
            f.write('\tModePin_PCH_GPIO_Group	DualModePinPCHGPIO_group = ' + str(daul_mode_pin_pch_gpip_group) + ';\n')
            f.write('\tint32	PCH_or_SIO_DualModePin = ' + str(pch_dual_mode_pin_sio_dual_mode_pin) + ';\n')
            f.write('\tint32	DualModePin_EC_bank = ' + str(dual_mode_pin_ec_bank) + ';\n')
            f.write('\tint32	DualModePin_EC_Reg = ' + str(dual_mode_pin_ec_reg) + ';\n') 
            f.write('\tint32	DualModePin_EC_Reg_Bit = ' + str(dual_mode_pin_ec_reg_bit) + ';\n')
            f.write('\tuint64	MultiSource_Support = ' + str(multi_source_support) + ';\n')
            f.write('\tuint64	TEMPERATURE_SOURCE_ENABLE_0 = ' + str(temperature_source_enable_0) + ';\n')
            f.write('\tuint64	TEMPERATURE_SOURCE_ENABLE_1 = ' + str(temperature_source_enable_1) + ';\n')
            f.write('\tuint64	TEMPERATURE_SOURCE_ENABLE_2 = ' + str(temperature_source_enable_2) + ';\n')
            f.write('\tuint64	TEMPERATURE_SOURCE_ENABLE_3 = ' + str(temperature_source_enable_3) + ';\n')
            f.write('\tbool	FanOverTimeSupport = ' + str(fan_over_time_support) + ';\n')
            f.write('\tbool	FanInverseSupport = ' + str(fan_inverse_support) + ';\n')
            f.write('\tbool	FanOffSupport = ' + str(fan_off_support) + ';\n')
            f.write('\tbool	FanStepUpDownSupport = ' + str(step_up_down_support) + ';\n')
            f.write('\tint32	StepUp = ' + str(step_up) + ';\n')
            f.write('\tint32	StepDown = ' + str(step_down) + ';\n')
            f.write('\tint32	DCUpper_Temperature = ' + str(int(dc_upper_temperature)) + ';\n')
            f.write('\tint32	DCMax_DutyCycle = ' + str(int(dc_max_duty_cycle)) + ';\n')
            f.write('\tint32	DCMiddle_Temperature = ' + str(int(dc_middle_temperature)) + ';\n')
            f.write('\tint32	DCMiddle_DutyCycle = ' + str(int(dc_middle_duty_cycle)) + ';\n')
            f.write('\tint32	DCLower_Temperature = ' + str(int(dc_lower_temperature)) + ';\n')
            f.write('\tint32	DCMin_DutyCycle = ' + str(int(dc_min_duty_cycle)) + ';\n')
            f.write('\tint32	PWMUpper_Temperature = ' + str(int(pwm_upper_temperature)) + ';\n')
            f.write('\tint32	PWMMax_DutyCycle = ' + str(int(pwm_max_duty_cycle)) + ';\n')
            f.write('\tint32	PWMMiddle_Temperature = ' + str(int(pwm_middle_temperature)) + ';\n')
            f.write('\tint32	PWMMiddle_DutyCycle = ' + str(int(pwm_middle_duty_cycle)) + ';\n')
            f.write('\tint32	PWMLower_Temperature = ' + str(int(pwm_lower_temperature)) + ';\n')
            f.write('\tint32	PWMMin_DutyCycle = ' + str(int(pwm_min_duty_cycle)) + ';\n')
            f.write('\tuint64	SpeedLowLimit = ' + str(speed_low_limit) + ';\n')
            f.write('\tbool	QFanTuningSupport = ' + str(qfan_tuning_suport) + ';\n')
            f.write('\tbool	Controlsupport = ' + '?' + ';\n')		# IS support this FANcontorl
            f.write('}\n')
            f.close

def generate_fan_info():
    with open(OUTPUT_FILE, "a") as f:
        f.write('\nmessage Fan_Info \n{\n')
        f.write('	string model_name = 1;\n')
        f.write('	uint32 chip_id = 2;\n')
        f.write('	string app_name = 3;\n')
        f.write('    message Fan_Control\n')
        f.write('	{\n')
        f.write('		Fan_Control_Auto_Mode	FANControlAutoMode = 1;\n')
        f.write('		Fan_Control_RPM_Mode	FANControlRPMMode = 2;\n')
        f.write('	}\n')
        f.write('	repeated Fan_Control fanctrl = 20;\n')
        f.write('}\n')        
        f.close
    
    
def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')

    init_file()

    df = pd.read_excel('Fan_table.xlsx', 'Fan Control', na_values=['-1'])
    df = df.fillna(-1)
    (first, last) = find_control_position(df)
    
    generate_enum_items(df, 'NAME ID', 'NameId')
    generate_enum_items(df, 'ModePinType', 'FANModePin_Type')
    #generate_enum_items(df, 'ModePin PCH GPIO Group', 'ModePin_PCH_GPIO_Group')
    generate_enum_items(df, 'Default mode', 'FANControl_Mode')
    
    generate_fan_contorl_rpm_mode(df, first, last)
    generate_fan_contorl_auto_mode(df, first, last)
    generate_fan_info()

main()