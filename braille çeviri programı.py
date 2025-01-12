import os
import cv2
import numpy as np
from tkinter import Tk, filedialog, messagebox

# Braille karakter sözlüğü
BRAILLE_DICT = {
    '100000': 'a', '110000': 'b', '100100': 'c', '100110': 'd',
    '100010': 'e', '110100': 'f', '110110': 'g', '110010': 'h',
    '010100': 'i', '010110': 'j', '101000': 'k', '111000': 'l',
    '101100': 'm', '101110': 'n', '101010': 'o', '111100': 'p',
    '111110': 'q', '111010': 'r', '011100': 's', '011110': 't',
    '101001': 'u', '111001': 'v', '010111': 'w', '101101': 'x',
    '101111': 'y', '101011': 'z',
    '000011': 'ç', '001111': 'ğ', '001011': 'ı', '001101': 'ö',
    '001110': 'ş', '001100': 'ü'
}

def preprocess_image(image, debug=True):
    """
    Görüntüyü işlemek için ön hazırlık yapar
    
    Parametreler:
    image: İşlenecek görüntü
    debug: Hata ayıklama görüntülerini kaydetmek için bayrak
    """
    # Orijinal boyutu kaydet
    height, width = image.shape
    
    # Görüntüyü büyüt
    image = cv2.resize(image, (width * 3, height * 3))
    
    # Gürültüyü azalt
    image = cv2.GaussianBlur(image, (5, 5), 0)
    if debug:
        cv2.imwrite('debug_1_blurred.png', image)
    
    # İkili (binary) görüntüye dönüştür
    binary = cv2.adaptiveThreshold(
        image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )
    if debug:
        cv2.imwrite('debug_2_threshold.png', binary)
    
    # Morfolojik işlemler
    kernel = np.ones((3,3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    
    if debug:
        cv2.imwrite('debug_3_morphology.png', binary)
    
    return binary

def find_dots(binary_image, debug=True):
    """
    İkili görüntüde Braille noktalarını tespit eder
    
    Parametreler:
    binary_image: İkili görüntü
    debug: Hata ayıklama görüntülerini kaydetmek için bayrak
    """
    # Konturları bul
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    dots = []
    # Nokta boyut sınırları
    min_area = 40  # Minimum alan biraz düşürüldü
    max_area = 500  # Maximum alan biraz artırıldı
    
    debug_image = cv2.cvtColor(binary_image.copy(), cv2.COLOR_GRAY2BGR)
    
    for idx, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if min_area < area < max_area:
            perimeter = cv2.arcLength(contour, True)
            circularity = 4 * np.pi * area / (perimeter * perimeter)
            
            # Dairesellik kontrolü (0.6'ya düşürüldü - daha toleranslı)
            if circularity > 0.6:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    dots.append((cx, cy))
                    
                    # Hata ayıklama görüntüsüne nokta ve bilgileri ekle
                    if debug:
                        cv2.circle(debug_image, (cx, cy), 5, (0, 0, 255), -1)
                        cv2.putText(debug_image, f"{idx}:({cx},{cy})", (cx+10, cy),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
                        print(f"Nokta {idx}: Alan={area:.1f}, Dairesellik={circularity:.2f}")
    
    if debug:
        cv2.imwrite('debug_4_dots.png', debug_image)
        
    return sorted(dots, key=lambda p: (p[1], p[0]))

def group_dots_into_characters(dots, debug=True):
    """
    Noktaları karakterlere gruplar
    
    Parametreler:
    dots: Nokta koordinatları listesi
    debug: Hata ayıklama bilgilerini yazdırmak için bayrak
    """
    if not dots:
        return []
    
    # X koordinatlarını analiz et
    x_coords = [x for x, _ in dots]
    x_diffs = np.diff(sorted(x_coords))
    
    if len(x_diffs) > 0:
        # Ortalama karakter genişliğini hesapla
        avg_char_width = np.median([diff for diff in x_diffs if diff > 10])  # 10 piksel üstü farkları al
        
        # Karakterleri ayır
        characters = []
        current_char = []
        
        # Noktaları x koordinatlarına göre sırala
        sorted_dots = sorted(dots, key=lambda p: p[0])
        
        for i, dot in enumerate(sorted_dots):
            if i > 0:
                # Önceki nokta ile mesafeyi kontrol et
                prev_x = sorted_dots[i-1][0]
                curr_x = dot[0]
                if curr_x - prev_x > avg_char_width * 0.8:  # Karakter aralığı tespit edildi
                    if current_char:
                        characters.append(current_char)
                        current_char = []
            current_char.append(dot)
        
        # Son karakteri ekle
        if current_char:
            characters.append(current_char)
        
        if debug:
            print(f"\nGruplama analizi:")
            print(f"X koordinatları: {x_coords}")
            print(f"X farkları: {x_diffs}")
            print(f"Ortalama karakter genişliği: {avg_char_width:.1f}")
            print(f"Bulunan karakter sayısı: {len(characters)}")
            for i, char in enumerate(characters):
                print(f"Karakter {i}: {char}")
        
        return characters
    
    return [dots]

def dots_to_pattern(dots, debug=True):
    """
    Nokta grubunu Braille desenine çevirir
    """
    if not dots:
        return '000000'
    
    # Koordinatları ayır
    x_coords = np.array([x for x, _ in dots])
    y_coords = np.array([y for _, y in dots])
    
    # Referans noktaları
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    
    # Merkez noktayı bul
    center_x = (min_x + max_x) / 2
    
    # 3x2 grid oluştur
    grid = [[False] * 2 for _ in range(3)]
    
    # Her noktayı gride yerleştir
    for x, y in dots:
        # X pozisyonunu belirle (sol veya sağ)
        col = 1 if x > center_x else 0
        
        # Y pozisyonunu belirle (üst, orta, alt)
        relative_y = (y - min_y) / (max_y - min_y if max_y > min_y else 1)
        row = min(2, max(0, int(relative_y * 3)))
        
        grid[row][col] = True
    
    # Grid'i Braille desenine dönüştür
    pattern = ''
    for col in range(2):
        for row in range(3):
            pattern += '1' if grid[row][col] else '0'
    
    if debug:
        print(f"\nDesen analizi:")
        print(f"Grid düzeni:")
        for row in grid:
            print(row)
        print(f"Oluşturulan desen: {pattern}")
    
    return pattern
def process_braille(image_path, debug=True):
    """
    Braille görüntüsünü işler ve metne çevirir
    
    Parametreler:
    image_path: Görüntü dosyasının yolu
    debug: Hata ayıklama modunu açıp kapatmak için bayrak
    """
    # Görüntüyü yükle
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Görüntü yüklenemedi!")
    
    if debug:
        cv2.imwrite('debug_0_original.png', image)
    
    # Görüntüyü işle
    binary = preprocess_image(image, debug)
    dots = find_dots(binary, debug)
    characters = group_dots_into_characters(dots, debug)
    
    text = ""
    for char_dots in characters:
        pattern = dots_to_pattern(char_dots, debug)
        char = BRAILLE_DICT.get(pattern, '?')
        text += char
        
        if debug:
            print(f"\nKarakter analizi:")
            print(f"Nokta sayısı: {len(char_dots)}")
            print(f"Nokta konumları: {char_dots}")
            print(f"Oluşturulan desen: {pattern}")
            print(f"Eşleşen harf: {char}")
    
    return text

def upload_and_translate():
    """
    Dosya seçim penceresi açar ve seçilen Braille görüntüsünü işler
    """
    Tk().withdraw()
    file_path = filedialog.askopenfilename(
        title="Bir Braille görüntüsü seçin",
        filetypes=[("Görüntü dosyaları", ".jpg *.jpeg *.png"), ("Tüm dosyalar", ".*")]
    )
    
    if not file_path:
        messagebox.showinfo("Bilgi", "Görüntü seçmediniz!")
        return
    
    try:
        # Debug modunda işle
        translated_text = process_braille(file_path, debug=True)
        
        if not translated_text:
            messagebox.showwarning("Uyarı", "Metinde okunabilir karakter bulunamadı!")
            return
        
        # Sonucu göster
        messagebox.showinfo("Çeviri Sonucu", translated_text)
        print(f"\nÇevrilen metin: {translated_text}")
        
    except Exception as e:
        messagebox.showerror("Hata", f"Çeviri sırasında hata oluştu: {str(e)}")

if __name__ == "__main__":
    upload_and_translate()
