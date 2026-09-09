# -*- coding: utf-8 -*-
import json
import os
import sys

# ให้แสดงผลภาษาไทยในคอนโซลถูกต้อง
sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')

CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "user_config.json")

# ค่าเริ่มต้นเริ่มต้น
defaults = {
    "ENABLE_DRINK": True,
    "DRINK_INTERVAL_MIN": 150.0,
    "ENABLE_EAT": True,
    "EAT_INTERVAL_MIN": 150.0,
    "DEPOSIT_MODE": "discard",
    "CHECK_INTERVAL": 2.0,
    "CAPTURE_MODE": "screen",
    "PARK_GAME_OFFSCREEN": False,
    "TRUNK_FULL_MEMORY_MIN": 10.0,
    "SPEED_PERCENT": 100.0,
    "DIALOG_OPEN_DELAY": 0.6,
    "CLICK_DELAY": 0.25,
    "DRAG_DURATION": 0.35,
    "DRAG_GRAB_DELAY": 0.10,
    "AFTER_DEPOSIT_DELAY": 0.8
}


def ask_speed(config):
    """ปรับความไวตอนลากของ / กด Max / กด O"""
    print()
    print("  กด Enter ผ่านไปเลย = ใช้ค่าเดิม")
    for key, label in (("DRAG_DURATION", "เวลาลากไอเทม"),
                       ("DRAG_GRAB_DELAY", "รอตอนจับ/ปล่อยของ"),
                       ("DIALOG_OPEN_DELAY", "รอ dialog เด้งหลังลาก"),
                       ("CLICK_DELAY", "รอระหว่างกด Max กับ O"),
                       ("AFTER_DEPOSIT_DELAY", "รอหลังยืนยันฝากของ")):
        try:
            val = input(f"  {label} (วิ) [เดิม {config[key]:.2f}]: ").strip()
            if val:
                config[key] = float(val)
        except ValueError:
            input("  ค่าไม่ถูกต้อง ใส่ตัวเลขเท่านั้น (กด Enter เพื่อไปต่อ)")


def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                user_conf = json.load(f)
                # รวมค่าที่โหลดเข้ากับ defaults เผื่อมีบางค่าหายไป
                merged = defaults.copy()
                for k, v in user_conf.items():
                    merged[k] = v
                return merged
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการโหลดไฟล์ตั้งค่าเดิม: {e}")
    return defaults.copy()


def save_config(config):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        print("\n[✓] บันทึกการตั้งค่าลงใน user_config.json เรียบร้อยแล้ว!")
        return True
    except Exception as e:
        print(f"\n[✗] เกิดข้อผิดพลาดในการบันทึกไฟล์: {e}")
        return False


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    config = load_config()

    while True:
        clear_screen()
        print("=" * 60)
        print("         🤖  Item Farming Bot Configurator (ตั้งค่าบอท)  🤖")
        print("=" * 60)
        
        drink_enable_str = "เปิด (ON)" if config["ENABLE_DRINK"] else "ปิด (OFF)"
        eat_enable_str = "เปิด (ON)" if config["ENABLE_EAT"] else "ปิด (OFF)"
        
        mode_str = "ทิ้งของ (discard)" if config["DEPOSIT_MODE"] == "discard" else "ฝากท้ายรถ (trunk)"

        if config.get("CAPTURE_MODE", "screen") == "window":
            cap_str = "จับหน้าต่างเกม (window) — เอาหน้าต่างอื่นทับได้"
        else:
            cap_str = "จับหน้าจอ (screen) — เกมต้องอยู่บนจอ"

        if config.get("PARK_GAME_OFFSCREEN", False):
            park_str = "เปิด (ON) — เกมหายจากจอระหว่างฟาร์ม"
        else:
            park_str = "ปิด (OFF)"
        
        print(f"  [1] ระบบกินน้ำ (ปุ่ม 1)       : {drink_enable_str}")
        print(f"  [2] เวลากินน้ำ (นาที)         : {config['DRINK_INTERVAL_MIN']:.1f} นาที")
        print(f"  [3] ระบบกินข้าว (ปุ่ม 2)       : {eat_enable_str}")
        print(f"  [4] เวลากินข้าว (นาที)         : {config['EAT_INTERVAL_MIN']:.1f} นาที")
        print(f"  [5] โหมดเมื่อของเต็ม          : {mode_str}")
        print(f"  [6] ความถี่ในการสแกนภาพ (วิ)   : {config['CHECK_INTERVAL']:.1f} วินาที")
        print(f"  [7] วิธีจับภาพ                : {cap_str}")
        print(f"  [8] จอดเกมไว้นอกจอ            : {park_str}")
        print(f"  [t] จำว่าท้ายรถเต็มนานแค่ไหน   : {config.get('TRUNK_FULL_MEMORY_MIN', 10.0):.1f} นาที")
        pct = float(config.get("SPEED_PERCENT", 100.0))
        k = 100.0 / max(25.0, min(400.0, pct))
        move_secs = (config["DRAG_DURATION"] + config["DRAG_GRAB_DELAY"] * 3
                     + config["DIALOG_OPEN_DELAY"] + config["CLICK_DELAY"]
                     + config["AFTER_DEPOSIT_DELAY"]) * k
        print(f"  [%] ความเร็วรวม                : {pct:.0f}%  "
              f"(ฝาก 1 ครั้ง ~{move_secs:.1f} วิ)")
        print("      มากกว่า 100 = เร็วขึ้น / น้อยกว่า 100 = ช้าลง ปลอดภัยขึ้น")
        print(f"  [v] ปรับทีละค่าเอง             : ลาก {config['DRAG_DURATION']:.2f} วิ ฯลฯ")
        print(f"      ลาก {config['DRAG_DURATION']:.2f} | dialog {config['DIALOG_OPEN_DELAY']:.2f} | "
              f"Max->O {config['CLICK_DELAY']:.2f} | หลังยืนยัน {config['AFTER_DEPOSIT_DELAY']:.2f}")
        print("      * ไวไปแล้วลากพลาดบ่อย ให้เพิ่มค่ากลับขึ้น")
        print("-" * 60)
        print("  [9] บันทึกและออก (Save & Exit)")
        print("  [0] ยกเลิกและออก (Exit without saving)")
        print("=" * 60)

        choice = input("กรุณาเลือกเมนู (0-9, t, v, %): ").strip().lower()

        if choice == "1":
            config["ENABLE_DRINK"] = not config["ENABLE_DRINK"]
        elif choice == "2":
            try:
                val = input(f"ใส่เวลากินน้ำใหม่ (นาที) [เดิม {config['DRINK_INTERVAL_MIN']:.1f}]: ").strip()
                if val:
                    config["DRINK_INTERVAL_MIN"] = float(val)
            except ValueError:
                input("ค่าไม่ถูกต้อง! กรุณาใส่ตัวเลขเท่านั้น (กด Enter เพื่อลองใหม่)")
        elif choice == "3":
            config["ENABLE_EAT"] = not config["ENABLE_EAT"]
        elif choice == "4":
            try:
                val = input(f"ใส่เวลากินข้าวใหม่ (นาที) [เดิม {config['EAT_INTERVAL_MIN']:.1f}]: ").strip()
                if val:
                    config["EAT_INTERVAL_MIN"] = float(val)
            except ValueError:
                input("ค่าไม่ถูกต้อง! กรุณาใส่ตัวเลขเท่านั้น (กด Enter เพื่อลองใหม่)")
        elif choice == "5":
            if config["DEPOSIT_MODE"] == "discard":
                config["DEPOSIT_MODE"] = "trunk"
            else:
                config["DEPOSIT_MODE"] = "discard"
        elif choice == "6":
            try:
                val = input(f"ใส่ความถี่การสแกนใหม่ (วินาที) [เดิม {config['CHECK_INTERVAL']:.1f}]: ").strip()
                if val:
                    config["CHECK_INTERVAL"] = float(val)
            except ValueError:
                input("ค่าไม่ถูกต้อง! กรุณาใส่ตัวเลขเท่านั้น (กด Enter เพื่อลองใหม่)")
        elif choice == "%":
            try:
                val = input("ความเร็วรวม % (100 = ปกติ, 200 = เร็วขึ้น 2 เท่า, "
                            f"50 = ช้าลงครึ่ง) [เดิม {pct:.0f}]: ").strip()
                if val:
                    config["SPEED_PERCENT"] = float(val)
            except ValueError:
                input("ค่าไม่ถูกต้อง! ใส่ตัวเลขเท่านั้น (กด Enter เพื่อลองใหม่)")
        elif choice == "v":
            ask_speed(config)
        elif choice == "7":
            if config.get("CAPTURE_MODE", "screen") == "window":
                config["CAPTURE_MODE"] = "screen"
            else:
                config["CAPTURE_MODE"] = "window"
                print()
                print("  หมายเหตุ: โหมดนี้ต้องลง  pip install windows-capture")
                print("  ย่อ (minimize) เกมยังไม่ได้ — Windows หยุดวาดหน้าต่างที่ย่อ")
                input("  กด Enter เพื่อไปต่อ...")
        elif choice == "8":
            config["PARK_GAME_OFFSCREEN"] = not config.get("PARK_GAME_OFFSCREEN", False)
            if config["PARK_GAME_OFFSCREEN"] and config.get("CAPTURE_MODE") != "window":
                print()
                print("  ต้องตั้ง [7] เป็น window ก่อน ไม่งั้นจอดแล้วอ่าน counter ไม่ได้")
                input("  กด Enter เพื่อไปต่อ...")
        elif choice == "t":
            try:
                val = input(f"จำว่าท้ายรถเต็มกี่นาที [เดิม {config.get('TRUNK_FULL_MEMORY_MIN', 10.0):.1f}]: ").strip()
                if val:
                    config["TRUNK_FULL_MEMORY_MIN"] = float(val)
            except ValueError:
                input("ค่าไม่ถูกต้อง! กรุณาใส่ตัวเลขเท่านั้น (กด Enter เพื่อลองใหม่)")
        elif choice == "9":
            if save_config(config):
                print()
                input("กด Enter เพื่อปิดหน้าต่าง...")
                break
        elif choice == "0":
            print()
            print("ยกเลิกการตั้งค่า")
            break
        else:
            input("เลือกเมนูไม่ถูกต้อง! (กด Enter เพื่อลองใหม่)")


if __name__ == "__main__":
    main()
