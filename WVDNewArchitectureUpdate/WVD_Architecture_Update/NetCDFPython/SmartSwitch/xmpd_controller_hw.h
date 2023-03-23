// ==============================================================
// Vivado(TM) HLS - High-Level Synthesis from C, C++ and SystemC v2019.2 (64-bit)
// Copyright 1986-2019 Xilinx, Inc. All Rights Reserved.
// ==============================================================
// cfg_bus
// 0x000 : Control signals
//         bit 0  - ap_start (Read/Write/COH)
//         bit 1  - ap_done (Read/COR)
//         bit 2  - ap_idle (Read)
//         bit 3  - ap_ready (Read)
//         bit 7  - auto_restart (Read/Write)
//         others - reserved
// 0x004 : Global Interrupt Enable Register
//         bit 0  - Global Interrupt Enable (Read/Write)
//         others - reserved
// 0x008 : IP Interrupt Enable Register (Read/Write)
//         bit 0  - Channel 0 (ap_done)
//         bit 1  - Channel 1 (ap_ready)
//         others - reserved
// 0x00c : IP Interrupt Status Register (Read/TOW)
//         bit 0  - Channel 0 (ap_done)
//         bit 1  - Channel 1 (ap_ready)
//         others - reserved
// 0x010 : Data signal of cfg_pulse_sequence_start_stop_indexes
//         bit 31~0 - cfg_pulse_sequence_start_stop_indexes[31:0] (Read/Write)
// 0x014 : reserved
// 0x018 : Data signal of cfg_num_pulses_to_execute
//         bit 31~0 - cfg_num_pulses_to_execute[31:0] (Read/Write)
// 0x01c : reserved
// 0x020 : Data signal of cfg_watchdog
//         bit 31~0 - cfg_watchdog[31:0] (Read/Write)
// 0x024 : reserved
// 0x028 : Data signal of cfg_disable_watchdog
//         bit 31~0 - cfg_disable_watchdog[31:0] (Read/Write)
// 0x02c : reserved
// 0x030 : Data signal of status_sequence_index
//         bit 31~0 - status_sequence_index[31:0] (Read)
// 0x034 : Control signal of status_sequence_index
//         bit 0  - status_sequence_index_ap_vld (Read/COR)
//         others - reserved
// 0x038 : Data signal of status_pulse_counter
//         bit 31~0 - status_pulse_counter[31:0] (Read)
// 0x03c : Control signal of status_pulse_counter
//         bit 0  - status_pulse_counter_ap_vld (Read/COR)
//         others - reserved
// 0x040 : Data signal of status_watchdog_expired
//         bit 31~0 - status_watchdog_expired[31:0] (Read)
// 0x044 : Control signal of status_watchdog_expired
//         bit 0  - status_watchdog_expired_ap_vld (Read/COR)
//         others - reserved
// 0x080 ~
// 0x0ff : Memory 'cfg_pulse_sequence_prt' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_prt[n]
// 0x100 ~
// 0x17f : Memory 'cfg_pulse_sequence_num_pulses' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_num_pulses[n]
// 0x180 ~
// 0x1ff : Memory 'cfg_pulse_sequence_num_offline_pulses' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_num_offline_pulses[n]
// 0x200 ~
// 0x27f : Memory 'cfg_pulse_sequence_num_online_pulses' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_num_online_pulses[n]
// 0x280 ~
// 0x2ff : Memory 'cfg_pulse_sequence_block_post_time' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_block_post_time[n]
// 0x300 ~
// 0x37f : Memory 'cfg_pulse_sequence_control_flags' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_control_flags[n]
// 0x380 ~
// 0x3ff : Memory 'cfg_pulse_sequence_timer_offset_0' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_timer_offset_0[n]
// 0x400 ~
// 0x47f : Memory 'cfg_pulse_sequence_timer_offset_1' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_timer_offset_1[n]
// 0x480 ~
// 0x4ff : Memory 'cfg_pulse_sequence_timer_offset_2' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_timer_offset_2[n]
// 0x500 ~
// 0x57f : Memory 'cfg_pulse_sequence_timer_offset_3' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_timer_offset_3[n]
// 0x580 ~
// 0x5ff : Memory 'cfg_pulse_sequence_timer_offset_4' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_timer_offset_4[n]
// 0x600 ~
// 0x67f : Memory 'cfg_pulse_sequence_timer_offset_5' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_timer_offset_5[n]
// 0x680 ~
// 0x6ff : Memory 'cfg_pulse_sequence_timer_offset_6' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_timer_offset_6[n]
// 0x700 ~
// 0x77f : Memory 'cfg_pulse_sequence_timer_offset_7' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_timer_offset_7[n]
// 0x780 ~
// 0x7ff : Memory 'cfg_pulse_sequence_timer_width_0' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_timer_width_0[n]
// 0x800 ~
// 0x87f : Memory 'cfg_pulse_sequence_timer_width_1' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_timer_width_1[n]
// 0x880 ~
// 0x8ff : Memory 'cfg_pulse_sequence_timer_width_2' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_timer_width_2[n]
// 0x900 ~
// 0x97f : Memory 'cfg_pulse_sequence_timer_width_3' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_timer_width_3[n]
// 0x980 ~
// 0x9ff : Memory 'cfg_pulse_sequence_timer_width_4' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_timer_width_4[n]
// 0xa00 ~
// 0xa7f : Memory 'cfg_pulse_sequence_timer_width_5' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_timer_width_5[n]
// 0xa80 ~
// 0xaff : Memory 'cfg_pulse_sequence_timer_width_6' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_timer_width_6[n]
// 0xb00 ~
// 0xb7f : Memory 'cfg_pulse_sequence_timer_width_7' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_timer_width_7[n]
// 0xb80 ~
// 0xbff : Memory 'cfg_pulse_sequence_ook_sequence_0' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_ook_sequence_0[n]
// 0xc00 ~
// 0xc7f : Memory 'cfg_pulse_sequence_ook_sequence_1' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_ook_sequence_1[n]
// 0xc80 ~
// 0xcff : Memory 'cfg_pulse_sequence_ook_sequence_2' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_ook_sequence_2[n]
// 0xd00 ~
// 0xd7f : Memory 'cfg_pulse_sequence_ook_sequence_3' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_ook_sequence_3[n]
// 0xd80 ~
// 0xdff : Memory 'cfg_pulse_sequence_ook_sequence_4' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_ook_sequence_4[n]
// 0xe00 ~
// 0xe7f : Memory 'cfg_pulse_sequence_ook_sequence_5' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_ook_sequence_5[n]
// 0xe80 ~
// 0xeff : Memory 'cfg_pulse_sequence_ook_sequence_6' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_ook_sequence_6[n]
// 0xf00 ~
// 0xf7f : Memory 'cfg_pulse_sequence_ook_sequence_7' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_ook_sequence_7[n]
// 0xf80 ~
// 0xfff : Memory 'cfg_pulse_sequence_dac' (32 * 32b)
//         Word n : bit [31:0] - cfg_pulse_sequence_dac[n]
// (SC = Self Clear, COR = Clear on Read, TOW = Toggle on Write, COH = Clear on Handshake)

#define XMPD_CONTROLLER_CFG_BUS_ADDR_AP_CTRL                                    0x000
#define XMPD_CONTROLLER_CFG_BUS_ADDR_GIE                                        0x004
#define XMPD_CONTROLLER_CFG_BUS_ADDR_IER                                        0x008
#define XMPD_CONTROLLER_CFG_BUS_ADDR_ISR                                        0x00c
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_START_STOP_INDEXES_DATA 0x010
#define XMPD_CONTROLLER_CFG_BUS_BITS_CFG_PULSE_SEQUENCE_START_STOP_INDEXES_DATA 32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_NUM_PULSES_TO_EXECUTE_DATA             0x018
#define XMPD_CONTROLLER_CFG_BUS_BITS_CFG_NUM_PULSES_TO_EXECUTE_DATA             32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_WATCHDOG_DATA                          0x020
#define XMPD_CONTROLLER_CFG_BUS_BITS_CFG_WATCHDOG_DATA                          32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_DISABLE_WATCHDOG_DATA                  0x028
#define XMPD_CONTROLLER_CFG_BUS_BITS_CFG_DISABLE_WATCHDOG_DATA                  32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_STATUS_SEQUENCE_INDEX_DATA                 0x030
#define XMPD_CONTROLLER_CFG_BUS_BITS_STATUS_SEQUENCE_INDEX_DATA                 32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_STATUS_SEQUENCE_INDEX_CTRL                 0x034
#define XMPD_CONTROLLER_CFG_BUS_ADDR_STATUS_PULSE_COUNTER_DATA                  0x038
#define XMPD_CONTROLLER_CFG_BUS_BITS_STATUS_PULSE_COUNTER_DATA                  32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_STATUS_PULSE_COUNTER_CTRL                  0x03c
#define XMPD_CONTROLLER_CFG_BUS_ADDR_STATUS_WATCHDOG_EXPIRED_DATA               0x040
#define XMPD_CONTROLLER_CFG_BUS_BITS_STATUS_WATCHDOG_EXPIRED_DATA               32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_STATUS_WATCHDOG_EXPIRED_CTRL               0x044
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_PRT_BASE                0x080
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_PRT_HIGH                0x0ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_PRT                    32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_PRT                    32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_NUM_PULSES_BASE         0x100
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_NUM_PULSES_HIGH         0x17f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_NUM_PULSES             32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_NUM_PULSES             32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_NUM_OFFLINE_PULSES_BASE 0x180
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_NUM_OFFLINE_PULSES_HIGH 0x1ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_NUM_OFFLINE_PULSES     32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_NUM_OFFLINE_PULSES     32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_NUM_ONLINE_PULSES_BASE  0x200
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_NUM_ONLINE_PULSES_HIGH  0x27f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_NUM_ONLINE_PULSES      32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_NUM_ONLINE_PULSES      32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_BLOCK_POST_TIME_BASE    0x280
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_BLOCK_POST_TIME_HIGH    0x2ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_BLOCK_POST_TIME        32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_BLOCK_POST_TIME        32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_CONTROL_FLAGS_BASE      0x300
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_CONTROL_FLAGS_HIGH      0x37f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_CONTROL_FLAGS          32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_CONTROL_FLAGS          32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_0_BASE     0x380
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_0_HIGH     0x3ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_0         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_0         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_1_BASE     0x400
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_1_HIGH     0x47f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_1         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_1         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_2_BASE     0x480
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_2_HIGH     0x4ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_2         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_2         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_3_BASE     0x500
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_3_HIGH     0x57f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_3         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_3         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_4_BASE     0x580
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_4_HIGH     0x5ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_4         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_4         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_5_BASE     0x600
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_5_HIGH     0x67f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_5         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_5         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_6_BASE     0x680
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_6_HIGH     0x6ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_6         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_6         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_7_BASE     0x700
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_OFFSET_7_HIGH     0x77f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_7         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_OFFSET_7         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_0_BASE      0x780
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_0_HIGH      0x7ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_0          32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_0          32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_1_BASE      0x800
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_1_HIGH      0x87f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_1          32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_1          32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_2_BASE      0x880
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_2_HIGH      0x8ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_2          32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_2          32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_3_BASE      0x900
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_3_HIGH      0x97f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_3          32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_3          32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_4_BASE      0x980
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_4_HIGH      0x9ff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_4          32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_4          32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_5_BASE      0xa00
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_5_HIGH      0xa7f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_5          32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_5          32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_6_BASE      0xa80
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_6_HIGH      0xaff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_6          32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_6          32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_7_BASE      0xb00
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_TIMER_WIDTH_7_HIGH      0xb7f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_7          32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_TIMER_WIDTH_7          32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_0_BASE     0xb80
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_0_HIGH     0xbff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_0         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_0         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_1_BASE     0xc00
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_1_HIGH     0xc7f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_1         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_1         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_2_BASE     0xc80
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_2_HIGH     0xcff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_2         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_2         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_3_BASE     0xd00
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_3_HIGH     0xd7f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_3         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_3         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_4_BASE     0xd80
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_4_HIGH     0xdff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_4         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_4         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_5_BASE     0xe00
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_5_HIGH     0xe7f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_5         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_5         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_6_BASE     0xe80
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_6_HIGH     0xeff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_6         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_6         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_7_BASE     0xf00
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_7_HIGH     0xf7f
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_7         32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_OOK_SEQUENCE_7         32
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_DAC_BASE                0xf80
#define XMPD_CONTROLLER_CFG_BUS_ADDR_CFG_PULSE_SEQUENCE_DAC_HIGH                0xfff
#define XMPD_CONTROLLER_CFG_BUS_WIDTH_CFG_PULSE_SEQUENCE_DAC                    32
#define XMPD_CONTROLLER_CFG_BUS_DEPTH_CFG_PULSE_SEQUENCE_DAC                    32
