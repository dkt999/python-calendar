import sys
import urllib.request
import json
import re
from PyQt6.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout,
                             QLabel, QFrame, QGridLayout, QSizePolicy, QLCDNumber)

from PyQt6.QtCore import Qt, QRect, QTimer, QTime
from PyQt6.QtGui import QFont, QPixmap, QImage, QPainter, QColor
from datetime import datetime

class ImageOverlayWidget(QWidget):
    def __init__(self, img_url, parent=None):
        super().__init__(parent)
        self.pixmap = QPixmap()
        self.load_image_from_url(img_url)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.addStretch()

        self.events_frame = QFrame()
        self.events_frame.setStyleSheet("background-color: rgba(0, 0, 0, 160); border-radius: 12px;")
        self.events_layout = QVBoxLayout(self.events_frame)
        self.events_layout.setSpacing(8)

        title_event = QLabel("Sự Kiện Sắp Tới")
        title_event.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        title_event.setStyleSheet("color: white; background: transparent;")
        self.events_layout.addWidget(title_event)

        mock_events = [
            {"date": "Hôm nay", "name": "Deploy hệ thống", "desc": "Cập nhật phiên bản mới lên production."},
            {"date": "Ngày mai", "name": "Báo cáo tiến độ", "desc": "Tổng hợp task và báo cáo khách hàng."},
            {"date": "Ngày mốt", "name": "Review Code", "desc": "Review merge requests của team."}
        ]

        for ev in mock_events:
            ev_label = QLabel(f"<span style='color: #64B5F6; font-size: 14px;'><b>{ev['date']} - {ev['name']}</b></span><br>"
                              f"<span style='color: #E0E0E0;'>{ev['desc']}</span>")
            ev_label.setStyleSheet("padding: 8px; background: rgba(255, 255, 255, 20); border-left: 4px solid #64B5F6; border-radius: 4px;")
            ev_label.setWordWrap(True)
            self.events_layout.addWidget(ev_label)

        self.layout.addWidget(self.events_frame)

    def load_image_from_url(self, url):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            data = urllib.request.urlopen(req).read()
            image = QImage()
            image.loadFromData(data)
            self.pixmap = QPixmap.fromImage(image)
        except Exception as e:
            print("Lỗi tải ảnh:", e)

    def paintEvent(self, event):
        if self.pixmap.isNull(): return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        rect = self.rect()

        # Blur background
        small_pix = self.pixmap.scaled(rect.width() // 15, rect.height() // 15, 
                                       Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
                                       Qt.TransformationMode.SmoothTransformation)
        bg_pixmap = small_pix.scaled(rect.width(), rect.height(), 
                                     Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
                                     Qt.TransformationMode.SmoothTransformation)
        
        crop_x = (bg_pixmap.width() - rect.width()) // 2
        crop_y = (bg_pixmap.height() - rect.height()) // 2
        painter.drawPixmap(rect, bg_pixmap, QRect(crop_x, crop_y, rect.width(), rect.height()))
        painter.fillRect(rect, QColor(0, 0, 0, 100))

        # Foreground contain
        fg_pixmap = self.pixmap.scaled(rect.size(), 
                                       Qt.AspectRatioMode.KeepAspectRatio, 
                                       Qt.TransformationMode.SmoothTransformation)
        draw_x = (rect.width() - fg_pixmap.width()) // 2
        draw_y = (rect.height() - fg_pixmap.height()) // 2
        painter.drawPixmap(draw_x, draw_y, fg_pixmap)


class DesktopCalendar(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ứng dụng Lịch Desktop Pro (PyQt6)')
        self.resize(1150, 750)
        self.setStyleSheet("background-color: #ffffff; color: #333333;")

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        # ==========================================
        # 1. CỘT TRÁI
        # ==========================================
        img_url = "https://images.unsplash.com/photo-1549298240-0d8e60513026?q=80&w=600&auto=format&fit=crop"
        self.left_col = ImageOverlayWidget(img_url)
        self.left_col.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        main_layout.addWidget(self.left_col, 1)

        # ==========================================
        # 2. CỘT PHẢI
        # ==========================================
        right_col = QWidget()
        right_col.setFixedWidth(385) 
        right_layout = QVBoxLayout(right_col)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        now = datetime.now()
        #MONTH N YEAR
        main_calendar = QFrame()
        main_calendar.setStyleSheet("background-color: #3C3C3C")
        row1 = QHBoxLayout()
        vi_months = ["MỘT", "HAI", "BA", "TƯ", "NĂM", "SÁU", "BẢY", "TÁM", "CHÍN", "MƯỜI", "MƯỜT MỘT", "MƯỜI HAI"]
        lbl_month = QLabel(f"THÁNG {vi_months[now.month - 1]}")
        lbl_month.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        lbl_month.setStyleSheet("color: white;")
        lbl_year = QLabel(f"NĂM {now.year}")
        lbl_year.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        lbl_year.setStyleSheet("color: white;")
        lbl_year.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        row1.addWidget(lbl_month)
        row1.addWidget(lbl_year)
        main_calendar.setLayout(row1)
        right_layout.addWidget(main_calendar)
        #LINE
        line = QWidget()
        line.setFixedHeight(1)
        line.setStyleSheet("background-color: #FFCA95;")
        right_layout.addWidget(line)
        #CLOCK 
        clock_frame = QFrame()
        clock_frame.setStyleSheet("background-color: #212121")
        clock_frame.setFixedHeight(110)
        
        clock_layout = QHBoxLayout(clock_frame)
        clock_layout.setContentsMargins(15, 10, 15, 10)
        clock_layout.setSpacing(5) # Khoảng cách ngang giữa Giờ và Giây

        # Đẩy toàn bộ cụm vào giữa cột phải
        clock_layout.addStretch()

        # 1. LCD Giờ:Phút (Giữ nguyên cố định đáy)
        self.lcd_hm = QLCDNumber(5) 
        self.lcd_hm.setSegmentStyle(QLCDNumber.SegmentStyle.Flat) 
        self.lcd_hm.setStyleSheet("color: #ffffff; background: transparent; border: none;")
        self.lcd_hm.setFixedSize(170, 80) 
        clock_layout.addWidget(self.lcd_hm, 0, Qt.AlignmentFlag.AlignBottom)

        # 2. LCD Giây
        self.lcd_s = QLCDNumber(2) 
        self.lcd_s.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
        self.lcd_s.setStyleSheet("color: #ffffff; background: transparent; border: none;")
        self.lcd_s.setFixedSize(55, 40) 
        
        # Tạo layout dọc riêng cho Giây để căn chỉnh cao thấp
        sec_container = QVBoxLayout()
        sec_container.setContentsMargins(0, 0, 0, 0)
        sec_container.addStretch()  # Đẩy số giây xuống sát đáy trước
        sec_container.addWidget(self.lcd_s)
        
        # --- KHU VỰC TINH CHỈNH ĐỘ CAO ---
        # Thêm 10px khoảng trống ở đáy để nhấc số giây lên ngang hàng với số giờ
        # Nếu chạy lên vẫn thấy lệch, fen cứ tăng giảm số 10 này (ví dụ: 8, 12, 14) là chuẩn khít liền.
        sec_container.addSpacing(10) 

        # Thêm layout của Giây vào layout chính của đồng hồ
        clock_layout.addLayout(sec_container)

        # Đẩy toàn bộ cụm từ bên phải qua để cân giữa
        clock_layout.addStretch()

        right_layout.addWidget(clock_frame)
        #LINE
        line = QWidget()
        line.setFixedHeight(1)
        line.setStyleSheet("background-color: #FFCA95;")
        right_layout.addWidget(line)
        # Hàng 3 #DAY
        main_day = QFrame()
        main_day.setStyleSheet("QFrame {background-color: #3C3C3C;border: none;}")
        layout = QVBoxLayout(main_day)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        lbl_day_big = QLabel(f"{now.day}")
        lbl_day_big.setFont(QFont("Arial", 120, QFont.Weight.Bold))
        lbl_day_big.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_day_big.setStyleSheet("QLabel {color: #d32f2f;background: transparent;}")
        layout.addWidget(lbl_day_big)
        right_layout.addWidget(main_day) 
        line = QWidget()
        line.setFixedHeight(1)
        line.setStyleSheet("background-color: #FFCA95;")       
        right_layout.addWidget(line)

        now = datetime.now()
        wd = now.weekday() # 0: Thứ 2, ..., 6: Chủ Nhật
        day_num = now.day
        vi_days = ["THỨ HAI", "THỨ BA", "THỨ TƯ", "THỨ NĂM", "THỨ SÁU", "THỨ BẢY", "CHỦ NHẬT"]
        en_days = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURDAY", "FRIDAY", "STATURDAY", "SUNDAY"]
        jp_days = ["月", "火", "水", "木", "金", "土", "日"]
        # --- Hàng 3 ---
        row3_frame = QFrame()
        row3_frame.setStyleSheet("background-color: #3C3C3C;") 
        
        row3 = QHBoxLayout(row3_frame)
        row3.setContentsMargins(15, 8, 15, 8)
        row3.setSpacing(0)

        # Cột 1: Bên trái (Tiếng Việt)
        lbl_vi = QLabel(vi_days[wd])
        lbl_vi.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        lbl_vi.setStyleSheet("color: white; background: transparent;")
        lbl_vi.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # Cột 2: Ở giữa (Hình tròn chứa chữ Nhật và Ngày)
        circle_lbl = QLabel(f"{jp_days[wd]}")
        circle_lbl.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        circle_lbl.setFixedSize(34, 34)
        # Nền màu đỏ trầm làm điểm nhấn (fen có thể đổi mã màu tùy ý)
        circle_lbl.setStyleSheet("""
            background-color: #d32f2f; 
            color: white; 
            border-radius: 16px; 
            font-weight: bold;
        """)
        circle_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Cột 3: Bên phải (Tiếng Anh)
        lbl_en = QLabel(en_days[wd])
        lbl_en.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        lbl_en.setStyleSheet("color: white; background: transparent;")
        lbl_en.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        # Tham số stretch (1 - 0 - 1) giúp ép hình tròn vào chính giữa tâm một cách hoàn hảo
        row3.addWidget(lbl_vi, 1)
        row3.addWidget(circle_lbl, 0, Qt.AlignmentFlag.AlignCenter)
        row3.addWidget(lbl_en, 1)
        right_layout.addWidget(row3_frame)
        #LINE
        line = QWidget()
        line.setFixedHeight(1)
        line.setStyleSheet("background-color: #FFCA95;")
        right_layout.addWidget(line)

        lunar_data = self.fetch_lunar_data()
        # Hàng 4
        row4_frame = QFrame()
        row4_frame.setStyleSheet("background-color: #3C3C3C;")
        
        row4 = QHBoxLayout(row4_frame)
        row4.setContentsMargins(15, 12, 15, 12) 
        row4.setSpacing(0)

        if lunar_data:
            today_index = now.day - 1 
            
            if 0 <= today_index < len(lunar_data):
                today_data = lunar_data[today_index]
                lunar_info = today_data['am_lich']
                can_chi = today_data['can_chi']
                
                # ==========================================
                # CỘT TRÁI: THÔNG TIN ÂM LỊCH MỚI
                # ==========================================
                col_lunar = QVBoxLayout()
                col_lunar.setContentsMargins(0, 0, 0, 0) 
                col_lunar.setSpacing(2)
                
                # Từ điển chuyển đổi ngày âm sang chữ Trung Quốc
                lunar_day_val = int(lunar_info['ngay'])
                chinese_days = ["", "初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
                                "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
                                "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]
                cn_day_str = chinese_days[lunar_day_val] if 1 <= lunar_day_val <= 30 else str(lunar_day_val)
                
                # Hàng 1: Số ngày âm to lên 48px, canh giữa
                lbl_lunar_num = QLabel(str(lunar_day_val))
                lbl_lunar_num.setFont(QFont('Arial', 48, QFont.Weight.Bold))
                lbl_lunar_num.setStyleSheet("color: white; background: transparent;")
                lbl_lunar_num.setAlignment(Qt.AlignmentFlag.AlignCenter) 
                
                # Hàng 2: Số âm tiếng Trung canh giữa size 24px (Tô màu đỏ tươi cho giống lịch block)
                lbl_lunar_cn = QLabel(cn_day_str)
                lbl_lunar_cn.setFont(QFont('Arial', 24, QFont.Weight.Bold))
                lbl_lunar_cn.setStyleSheet("color: #FF5252; background: transparent;") 
                lbl_lunar_cn.setAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Hàng 3, 4, 5: Can chi bình thường (Canh trái)
                lbl_canchi_day = QLabel(f"Ngày {can_chi['ngay']}")
                lbl_canchi_month = QLabel(f"Tháng {can_chi['thang']}")
                lbl_canchi_year = QLabel(f"Năm {can_chi['nam']}")
                
                col_lunar.addWidget(lbl_lunar_num)
                col_lunar.addWidget(lbl_lunar_cn)
                
                for lbl in (lbl_canchi_day, lbl_canchi_month, lbl_canchi_year):
                    lbl.setFont(QFont('Arial', 12))
                    lbl.setStyleSheet("color: #cccccc; background: transparent;")
                    lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                    col_lunar.addWidget(lbl)
                    
                col_lunar.addStretch() 
                
                # Add cột Âm lịch vào hàng 4 (Tỷ lệ 50%)
                row4.addLayout(col_lunar, 1) 
                
                # ==========================================
                # BORDER RIGHT & CỘT PHẢI: GIỜ HOÀNG ĐẠO
                # ==========================================
                border_right = QFrame()
                border_right.setFixedWidth(1)
                border_right.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
                border_right.setStyleSheet("background-color: #666666; border: none;")
                
                row4.addWidget(border_right)
                row4.addSpacing(12) 
                
                col_zodiac = QVBoxLayout()
                col_zodiac.setContentsMargins(0, 0, 0, 0)
                col_zodiac.setSpacing(4)
                
                lbl_zodiac_title = QLabel("<b>GIỜ HOÀNG ĐẠO</b>")
                lbl_zodiac_title.setFont(QFont('Arial', 14, QFont.Weight.Normal))
                lbl_zodiac_title.setStyleSheet("color: white; background: transparent;") 
                lbl_zodiac_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
                col_zodiac.addWidget(lbl_zodiac_title)
                
                zodiac_grid = QGridLayout()
                zodiac_grid.setContentsMargins(0, 0, 0, 0)
                zodiac_grid.setSpacing(2) 
                
                for idx, g_item in enumerate(today_data['gio_hoang_dao']):
                    match = re.match(r"([^\s(]+)\s*\(([^)]+)\)", g_item)
                    if match:
                        name_part = match.group(1) 
                        time_part = match.group(2) 
                    else:
                        name_part = g_item
                        time_part = ""
                        
                    lbl_name = QLabel(name_part)
                    lbl_name.setFont(QFont('Arial', 14, QFont.Weight.Normal))
                    lbl_name.setStyleSheet("color: #90CAF9; background: transparent;") 
                    lbl_name.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                    
                    lbl_time = QLabel(time_part)
                    lbl_time.setFont(QFont('Arial', 14))
                    lbl_time.setStyleSheet("color: #cccccc; background: transparent;")
                    lbl_time.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    
                    zodiac_grid.addWidget(lbl_name, idx, 0)
                    zodiac_grid.addWidget(lbl_time, idx, 1)
                    
                col_zodiac.addLayout(zodiac_grid)
                col_zodiac.addStretch() 
                
                # Add cột Giờ Hoàng Đạo vào hàng 4 (Tỷ lệ 50%)
                row4.addLayout(col_zodiac, 1) 
        
        # Thêm cái frame vào layout bên phải
        right_layout.addWidget(row4_frame)
        #LINE
        line = QWidget()
        line.setFixedHeight(1)
        line.setStyleSheet("background-color: #FFCA95;")
        right_layout.addWidget(line)

        # Hàng 5 (Grid Lịch)
        cal_grid = QGridLayout()
        cal_grid.setSpacing(2)
        days_header = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
        for i, day in enumerate(days_header):
            lbl = QLabel(day)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setFont(QFont('Arial', 9, QFont.Weight.Bold))
            if i == 5: lbl.setStyleSheet("color: #1976D2;")
            elif i == 6: lbl.setStyleSheet("color: #D32F2F;")
            cal_grid.addWidget(lbl, 0, i)
        first_day_of_month = datetime(now.year, now.month, 1)
        start_col = first_day_of_month.weekday()
        day_count = 1
        for row in range(1, 7):
            for col in range(7):
                if row == 1 and col < start_col:
                    continue
                if day_count > len(lunar_data): break
                data = lunar_data[day_count - 1]
                cell = QFrame()
                cell.setFixedSize(45,70)
                if day_count == now.day:
                    cell.setStyleSheet("background-color: #ffebee; border: 1px solid #ffcdd2; border-radius: 4px;")
                else:
                    cell.setStyleSheet("background-color: #fafafa; border: 1px solid #eeeeee; border-radius: 4px;")

                cell_layout = QVBoxLayout(cell)
                cell_layout.setContentsMargins(2, 2, 2, 2)
                cell_layout.setSpacing(0)

                solar_lbl = QLabel(str(day_count))
                solar_lbl.setFont(QFont('Arial', 11, QFont.Weight.Bold))
                solar_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                if col == 5: solar_lbl.setStyleSheet("color: #1976D2; background: transparent; border: none;")
                elif col == 6: solar_lbl.setStyleSheet("color: #D32F2F; background: transparent; border: none;")
                else: solar_lbl.setStyleSheet("background: transparent; border: none;")
                lunar_txt = f"{data['am_lich']['ngay']}"
                if data['am_lich']['ngay'] == 1: # Highlight ngày mùng 1
                    lunar_txt = f"{data['am_lich']['ngay']}/{data['am_lich']['thang']}"
                lunar_lbl = QLabel(lunar_txt)
                lunar_lbl.setFont(QFont('Arial', 7))
                lunar_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
                lunar_lbl.setStyleSheet("color: #888888; background: transparent; border: none;")

                cell_layout.addWidget(solar_lbl)
                cell_layout.addWidget(lunar_lbl)
                cal_grid.addWidget(cell, row, col)
                day_count += 1
                
        right_layout.addLayout(cal_grid)

        # Hàng 6
        weather_frame = QFrame()
        weather_frame.setStyleSheet("background-color: #e3f2fd; border-radius: 6px;")
        weather_layout = QVBoxLayout(weather_frame)
        weather_lbl = QLabel("<b>Dự báo 5 ngày tới</b><br>Trời nắng, 28°C - 34°C, ít mây.")
        weather_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        weather_layout.addWidget(weather_lbl)
        right_layout.addWidget(weather_frame)

        right_layout.addStretch()
        main_layout.addWidget(right_col)

        # --- TIMER CẬP NHẬT ĐỒNG HỒ ---
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()
    def fetch_lunar_data(self):
        # Thay URL này bằng đường dẫn đến file PHP của bạn
        url = f"https://dinhkimthach.name.vn/public_api/api_v2.php"
        try:
            with urllib.request.urlopen(url) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            print("Lỗi API:", e)
            return None
    def update_time(self):
        current_time = QTime.currentTime()
        text_hm = current_time.toString("hh:mm")
        text_s = current_time.toString("ss")
        
        if current_time.second() % 2 == 0:
            text_hm = text_hm.replace(":", " ")
            
        self.lcd_hm.display(text_hm)
        self.lcd_s.display(text_s)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
            
        # 2. Nếu bấm tổ hợp Alt + F4 -> Đóng app
        elif event.key() == Qt.Key.Key_F4 and (event.modifiers() & Qt.KeyboardModifier.AltModifier):
            self.close()
            
        # Các phím khác để hệ thống tự xử lý
        else:
            super().keyPressEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DesktopCalendar()
    ex.showFullScreen()
    sys.exit(app.exec())