// ==============================================================
// Vivado(TM) HLS - High-Level Synthesis from C, C++ and SystemC v2019.2 (64-bit)
// Copyright 1986-2019 Xilinx, Inc. All Rights Reserved.
// ==============================================================
// cfg_bus
// 0x0000 : Control signals
//          bit 0  - ap_start (Read/Write/COH)
//          bit 1  - ap_done (Read/COR)
//          bit 2  - ap_idle (Read)
//          bit 3  - ap_ready (Read)
//          bit 7  - auto_restart (Read/Write)
//          others - reserved
// 0x0004 : Global Interrupt Enable Register
//          bit 0  - Global Interrupt Enable (Read/Write)
//          others - reserved
// 0x0008 : IP Interrupt Enable Register (Read/Write)
//          bit 0  - Channel 0 (ap_done)
//          bit 1  - Channel 1 (ap_ready)
//          others - reserved
// 0x000c : IP Interrupt Status Register (Read/TOW)
//          bit 0  - Channel 0 (ap_done)
//          bit 1  - Channel 1 (ap_ready)
//          others - reserved
// 0x0010 : Data signal of cfg_pulse_sequence_start_stop_indexes
//          bit 31~0 - cfg_pulse_sequence_start_stop_indexes[31:0] (Read/Write)
// 0x0014 : reserved
// 0x0018 : Data signal of cfg_num_pulses_to_execute
//          bit 31~0 - cfg_num_pulses_to_execute[31:0] (Read/Write)
// 0x001c : reserved
// 0x0030 : Data signal of status_sequence_index
//          bit 31~0 - status_sequence_index[31:0] (Read)
// 0x0034 : Control signal of status_sequence_index
//          bit 0  - status_sequence_index_ap_vld (Read/COR)
//          others - reserved
// 0x0038 : Data signal of status_pulse_counter
//          bit 31~0 - status_pulse_counter[31:0] (Read)
// 0x003c : Control signal of status_pulse_counter
//          bit 0  - status_pulse_counter_ap_vld (Read/COR)
//          others - reserved
// 0x0080 ~
// 0x00ff : Memory 'cfg_pulse_sequence_prt' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_prt[n]
// 0x0100 ~
// 0x017f : Memory 'cfg_pulse_sequence_num_pulses' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_num_pulses[n]
// 0x0180 ~
// 0x01ff : Memory 'cfg_pulse_sequence_num_offline_pulses' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_num_offline_pulses[n]
// 0x0200 ~
// 0x027f : Memory 'cfg_pulse_sequence_num_online_pulses' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_num_online_pulses[n]
// 0x0280 ~
// 0x02ff : Memory 'cfg_pulse_sequence_block_post_time' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_block_post_time[n]
// 0x0300 ~
// 0x037f : Memory 'cfg_pulse_sequence_control_flags' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_control_flags[n]
// 0x0380 ~
// 0x03ff : Memory 'cfg_pulse_sequence_timer_offset_0' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_offset_0[n]
// 0x0400 ~
// 0x047f : Memory 'cfg_pulse_sequence_timer_offset_1' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_offset_1[n]
// 0x0480 ~
// 0x04ff : Memory 'cfg_pulse_sequence_timer_offset_2' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_offset_2[n]
// 0x0500 ~
// 0x057f : Memory 'cfg_pulse_sequence_timer_offset_3' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_offset_3[n]
// 0x0580 ~
// 0x05ff : Memory 'cfg_pulse_sequence_timer_offset_4' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_offset_4[n]
// 0x0600 ~
// 0x067f : Memory 'cfg_pulse_sequence_timer_offset_5' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_offset_5[n]
// 0x0680 ~
// 0x06ff : Memory 'cfg_pulse_sequence_timer_offset_6' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_offset_6[n]
// 0x0700 ~
// 0x077f : Memory 'cfg_pulse_sequence_timer_offset_7' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_offset_7[n]
// 0x0780 ~
// 0x07ff : Memory 'cfg_pulse_sequence_timer_offset_8' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_offset_8[n]
// 0x0800 ~
// 0x087f : Memory 'cfg_pulse_sequence_timer_offset_9' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_offset_9[n]
// 0x0880 ~
// 0x08ff : Memory 'cfg_pulse_sequence_timer_offset_10' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_offset_10[n]
// 0x0900 ~
// 0x097f : Memory 'cfg_pulse_sequence_timer_offset_11' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_offset_11[n]
// 0x0980 ~
// 0x09ff : Memory 'cfg_pulse_sequence_timer_offset_12' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_offset_12[n]
// 0x0a00 ~
// 0x0a7f : Memory 'cfg_pulse_sequence_timer_offset_13' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_offset_13[n]
// 0x0a80 ~
// 0x0aff : Memory 'cfg_pulse_sequence_timer_offset_14' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_offset_14[n]
// 0x0b00 ~
// 0x0b7f : Memory 'cfg_pulse_sequence_timer_offset_15' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_offset_15[n]
// 0x0b80 ~
// 0x0bff : Memory 'cfg_pulse_sequence_timer_width_0' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_width_0[n]
// 0x0c00 ~
// 0x0c7f : Memory 'cfg_pulse_sequence_timer_width_1' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_width_1[n]
// 0x0c80 ~
// 0x0cff : Memory 'cfg_pulse_sequence_timer_width_2' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_width_2[n]
// 0x0d00 ~
// 0x0d7f : Memory 'cfg_pulse_sequence_timer_width_3' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_width_3[n]
// 0x0d80 ~
// 0x0dff : Memory 'cfg_pulse_sequence_timer_width_4' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_width_4[n]
// 0x0e00 ~
// 0x0e7f : Memory 'cfg_pulse_sequence_timer_width_5' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_width_5[n]
// 0x0e80 ~
// 0x0eff : Memory 'cfg_pulse_sequence_timer_width_6' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_width_6[n]
// 0x0f00 ~
// 0x0f7f : Memory 'cfg_pulse_sequence_timer_width_7' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_width_7[n]
// 0x0f80 ~
// 0x0fff : Memory 'cfg_pulse_sequence_timer_width_8' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_width_8[n]
// 0x1000 ~
// 0x107f : Memory 'cfg_pulse_sequence_timer_width_9' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_width_9[n]
// 0x1080 ~
// 0x10ff : Memory 'cfg_pulse_sequence_timer_width_10' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_width_10[n]
// 0x1100 ~
// 0x117f : Memory 'cfg_pulse_sequence_timer_width_11' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_width_11[n]
// 0x1180 ~
// 0x11ff : Memory 'cfg_pulse_sequence_timer_width_12' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_width_12[n]
// 0x1200 ~
// 0x127f : Memory 'cfg_pulse_sequence_timer_width_13' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_width_13[n]
// 0x1280 ~
// 0x12ff : Memory 'cfg_pulse_sequence_timer_width_14' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_width_14[n]
// 0x1300 ~
// 0x137f : Memory 'cfg_pulse_sequence_timer_width_15' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_timer_width_15[n]
// 0x1380 ~
// 0x13ff : Memory 'cfg_pulse_sequence_ook_sequence_0' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_ook_sequence_0[n]
// 0x1400 ~
// 0x147f : Memory 'cfg_pulse_sequence_ook_sequence_1' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_ook_sequence_1[n]
// 0x1480 ~
// 0x14ff : Memory 'cfg_pulse_sequence_ook_sequence_2' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_ook_sequence_2[n]
// 0x1500 ~
// 0x157f : Memory 'cfg_pulse_sequence_ook_sequence_3' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_ook_sequence_3[n]
// 0x1580 ~
// 0x15ff : Memory 'cfg_pulse_sequence_ook_sequence_4' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_ook_sequence_4[n]
// 0x1600 ~
// 0x167f : Memory 'cfg_pulse_sequence_ook_sequence_5' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_ook_sequence_5[n]
// 0x1680 ~
// 0x16ff : Memory 'cfg_pulse_sequence_ook_sequence_6' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_ook_sequence_6[n]
// 0x1700 ~
// 0x177f : Memory 'cfg_pulse_sequence_ook_sequence_7' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_ook_sequence_7[n]
// 0x1780 ~
// 0x17ff : Memory 'cfg_pulse_sequence_ook_sequence_8' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_ook_sequence_8[n]
// 0x1800 ~
// 0x187f : Memory 'cfg_pulse_sequence_ook_sequence_9' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_ook_sequence_9[n]
// 0x1880 ~
// 0x18ff : Memory 'cfg_pulse_sequence_ook_sequence_10' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_ook_sequence_10[n]
// 0x1900 ~
// 0x197f : Memory 'cfg_pulse_sequence_ook_sequence_11' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_ook_sequence_11[n]
// 0x1980 ~
// 0x19ff : Memory 'cfg_pulse_sequence_ook_sequence_12' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_ook_sequence_12[n]
// 0x1a00 ~
// 0x1a7f : Memory 'cfg_pulse_sequence_ook_sequence_13' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_ook_sequence_13[n]
// 0x1a80 ~
// 0x1aff : Memory 'cfg_pulse_sequence_ook_sequence_14' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_ook_sequence_14[n]
// 0x1b00 ~
// 0x1b7f : Memory 'cfg_pulse_sequence_ook_sequence_15' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_ook_sequence_15[n]
// 0x1b80 ~
// 0x1bff : Memory 'cfg_pulse_sequence_dac' (32 * 32b)
//          Word n : bit [31:0] - cfg_pulse_sequence_dac[n]
// (SC = Self Clear, COR = Clear on Read, TOW = Toggle on Write, COH = Clear on Handshake)

#define XMPD_CONTROLLER_CFG_BUS_ADDR_AP_CTRL                                    0x0000
#define XMPD_CONTROLLER_CFG_BUS_ADDR_GIE                                        0x0004
#define XMPD_CONTROLLER_CFG_BUS_ADDR_IER                                        0x0008
#define XMPD_CONTROLLER_CFG_BUS_ADDR_ISR                                        0x000c
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_START_STOP_INDEXES_DATA 0x0010
#define XMPD_CONTROLLER_CFG_BUS_BITS_CFG_PULSE_SEQUENCE_START_STOP_INDEXES_DATA 32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_NUM_PULSES_TO_EXECUTE_DATA             0x0018
#define XMPD_CONTROLLER_CFG_BUS_BITS_CFG_NUM_PULSES_TO_EXECUTE_DATA             32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_STATUS_SEQUENCE_INDEX_DATA                 0x0030
#define XMPD_CONTROLLER_CFG_BUS_BITS_STATUS_SEQUENCE_INDEX_DATA                 32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_STATUS_SEQUENCE_INDEX_CTRL                 0x0034
#define XMPD_CONTROLLER_CFG_BUS_ADDR_STATUS_PULSE_COUNTER_DATA                  0x0038
#define XMPD_CONTROLLER_CFG_BUS_BITS_STATUS_PULSE_COUNTER_DATA                  32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_STATUS_PULSE_COUNTER_CTRL                  0x003c
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_PRT_BASE                0x0080
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_PRT_HIGH                0x00ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_PRT                    32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_PRT                    32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_NUM_PULSES_BASE         0x0100
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_NUM_PULSES_HIGH         0x017f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_NUM_PULSES             32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_NUM_PULSES             32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_NUM_OFFLINE_PULSES_BASE 0x0180
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_NUM_OFFLINE_PULSES_HIGH 0x01ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_NUM_OFFLINE_PULSES     32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_NUM_OFFLINE_PULSES     32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_NUM_ONLINE_PULSES_BASE  0x0200
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_NUM_ONLINE_PULSES_HIGH  0x027f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_NUM_ONLINE_PULSES      32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_NUM_ONLINE_PULSES      32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_BLOCK_POST_TIME_BASE    0x0280
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_BLOCK_POST_TIME_HIGH    0x02ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_BLOCK_POST_TIME        32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_BLOCK_POST_TIME        32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_CONTROL_FLAGS_BASE      0x0300
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_CONTROL_FLAGS_HIGH      0x037f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_CONTROL_FLAGS          32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_CONTROL_FLAGS          32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_0_BASE     0x0380
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_0_HIGH     0x03ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_0         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_0         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_1_BASE     0x0400
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_1_HIGH     0x047f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_1         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_1         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_2_BASE     0x0480
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_2_HIGH     0x04ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_2         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_2         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_3_BASE     0x0500
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_3_HIGH     0x057f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_3         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_3         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_4_BASE     0x0580
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_4_HIGH     0x05ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_4         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_4         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_5_BASE     0x0600
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_5_HIGH     0x067f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_5         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_5         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_6_BASE     0x0680
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_6_HIGH     0x06ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_6         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_6         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_7_BASE     0x0700
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_7_HIGH     0x077f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_7         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_7         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_8_BASE     0x0780
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_8_HIGH     0x07ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_8         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_8         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_9_BASE     0x0800
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_9_HIGH     0x087f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_9         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_9         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_10_BASE    0x0880
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_10_HIGH    0x08ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_10        32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_10        32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_11_BASE    0x0900
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_11_HIGH    0x097f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_11        32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_11        32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_12_BASE    0x0980
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_12_HIGH    0x09ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_12        32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_12        32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_13_BASE    0x0a00
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_13_HIGH    0x0a7f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_13        32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_13        32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_14_BASE    0x0a80
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_14_HIGH    0x0aff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_14        32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_14        32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_15_BASE    0x0b00
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_15_HIGH    0x0b7f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_15        32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_15        32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_0_BASE      0x0b80
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_0_HIGH      0x0bff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_0          32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_0          32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_1_BASE      0x0c00
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_1_HIGH      0x0c7f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_1          32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_1          32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_2_BASE      0x0c80
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_2_HIGH      0x0cff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_2          32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_2          32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_3_BASE      0x0d00
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_3_HIGH      0x0d7f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_3          32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_3          32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_4_BASE      0x0d80
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_4_HIGH      0x0dff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_4          32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_4          32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_5_BASE      0x0e00
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_5_HIGH      0x0e7f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_5          32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_5          32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_6_BASE      0x0e80
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_6_HIGH      0x0eff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_6          32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_6          32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_7_BASE      0x0f00
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_7_HIGH      0x0f7f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_7          32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_7          32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_8_BASE      0x0f80
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_8_HIGH      0x0fff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_8          32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_8          32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_9_BASE      0x1000
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_9_HIGH      0x107f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_9          32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_9          32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_10_BASE     0x1080
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_10_HIGH     0x10ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_10         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_10         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_11_BASE     0x1100
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_11_HIGH     0x117f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_11         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_11         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_12_BASE     0x1180
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_12_HIGH     0x11ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_12         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_12         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_13_BASE     0x1200
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_13_HIGH     0x127f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_13         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_13         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_14_BASE     0x1280
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_14_HIGH     0x12ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_14         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_14         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_15_BASE     0x1300
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_15_HIGH     0x137f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_15         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_15         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_0_BASE     0x1380
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_0_HIGH     0x13ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_0         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_0         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_1_BASE     0x1400
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_1_HIGH     0x147f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_1         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_1         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_2_BASE     0x1480
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_2_HIGH     0x14ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_2         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_2         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_3_BASE     0x1500
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_3_HIGH     0x157f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_3         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_3         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_4_BASE     0x1580
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_4_HIGH     0x15ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_4         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_4         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_5_BASE     0x1600
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_5_HIGH     0x167f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_5         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_5         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_6_BASE     0x1680
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_6_HIGH     0x16ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_6         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_6         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_7_BASE     0x1700
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_7_HIGH     0x177f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_7         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_7         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_8_BASE     0x1780
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_8_HIGH     0x17ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_8         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_8         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_9_BASE     0x1800
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_9_HIGH     0x187f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_9         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_9         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_10_BASE    0x1880
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_10_HIGH    0x18ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_10        32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_10        32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_11_BASE    0x1900
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_11_HIGH    0x197f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_11        32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_11        32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_12_BASE    0x1980
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_12_HIGH    0x19ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_12        32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_12        32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_13_BASE    0x1a00
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_13_HIGH    0x1a7f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_13        32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_13        32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_14_BASE    0x1a80
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_14_HIGH    0x1aff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_14        32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_14        32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_15_BASE    0x1b00
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_15_HIGH    0x1b7f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_15        32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_15        32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_DAC_BASE                0x1b80
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_DAC_HIGH                0x1bff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_DAC                    32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_DAC                    32

