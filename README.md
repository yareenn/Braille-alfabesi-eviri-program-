# Braille-alfabesi-eviri-program-
# Braille Alfabesi Görüntü Tanıma ve Çeviri Programı

Bu proje, Braille yazılarını bir görüntüdan alıp okunabilir metne çevirmeyi amaçlayan bir yazılımdır. Görüntüdaki Braille karakterleri, görüntü işleme teknikleri ve makine öğrenmesi algoritmalarını kullanarak tespit edilir ve karşılık geldiği harfler ile metne dönüştürülür.

## Proje Hakkında

Braille Görüntü Tanıma ve Çevirici, görme engelli bireyler için yazılı içeriklerin dijital ortamda daha erişilebilir hale gelmesini sağlamak amacıyla geliştirilmiştir. Proje, görsel materyallerdeki Braille yazılarını analiz ederek, bu yazıları karşılık gelen harflerle bir metne dönüştürür. Bu araç, özellikle Braille alfabesini öğrenmeye çalışanlar ve Braille ile yazılmış materyalleri dijital ortamda okumak isteyen kişiler için faydalıdır.

## Özellikler

- Görseldeki Braille karakterlerini tespit etme.
- Tespit edilen Braille karakterlerini metne çevirme.
- Türkçe Braille harflerini destekleme.
- Gelişmiş görüntü işleme teknikleri (büyütme, bulanıklaştırma, ikili dönüştürme, morfolojik işlemler) kullanarak doğru sonuç elde etme.
- Hata ayıklama modu, kullanıcıya her adımda görsel çıktı sağlar.

## Kurulum

### Gereksinimler

- Python 3.x
- OpenCV
- NumPy
- Tkinter (GUI desteği için)

### Adımlar

1. Python'un yüklü olduğundan emin olun. Yüklemek için [Python resmi web sitesi](https://www.python.org/)ne gidin.

2. Gerekli Python paketlerini yüklemek için terminal veya komut istemcisine aşağıdaki komutu yazın:

   ```bash
   pip install opencv-python numpy
   ```

3. Tkinter, Python'un varsayılan kütüphanesidir. Ancak, bazı sistemlerde ayrıca yüklenmesi gerekebilir:

   ```bash
   sudo apt-get install python3-tk  # Linux
   brew install python-tk          # macOS
   ```

4. Proje dosyalarını indirin veya klonlayın:

   ```bash
   git clone https://github.com/kullaniciadi/braille-image-to-text.git
   ```

5. Ana Python dosyasını çalıştırmak için aşağıdaki komutu kullanın:

   ```bash
   python braille_image_to_text.py
   ```

## Kullanım

1. Programı başlattığınızda bir dosya seçme penceresi açılacaktır.
2. Braille yazısını içeren bir görüntü dosyası (.jpg, .jpeg, .png) seçin.
3. Seçilen görüntü, arka planda işlenerek Braille harfleri okunabilir metne dönüştürülür.
4. Çevrilen metin, kullanıcıya bir pop-up mesajında gösterilecektir.

## Algoritma ve İşlem Adımları

Proje, aşağıdaki algoritmayı takip eder:

1. **Görüntü İşleme**

   - **Büyütme**: Görüntüdaki Braille noktalarının daha iyi tespit edilebilmesi için orijinal boyutlar üç katına çıkarılır.
   - **Bulanıklaştırma**: Görüntüdaki gürültülerin azaltılması için Gaussian blur uygulanır.
   - **İkili Görüntüleme**: Görüntü, ikili (binary) hale getirilir. Bu adımda adaptif eşikleme kullanılarak kontrast artırılır.

2. **Braille Noktalarının Tespiti**

   - İkili görüntüdaki konturlar analiz edilir.
   - Noktalar, belirli boyut ve dairesellik kriterlerine göre filtrelenir.

3. **Noktaların Gruplandırılması**

   - Gruplama için ortalama karakter genişliği hesaplanır.
   - Noktalar, x-koordinatları arasındaki mesafeye göre gruplandırılır.

4. **Braille Deseni Oluşturma**

   - Gruplanan noktalar, Braille'in 3x2'lik grid yapısına yerleştirilir. Her bir grid, bir karakteri temsil eder.

5. **Metne Dönüştürme**

   - Desenler, tanımlı bir Braille sözlüğüne karşılık gelen harflerle eşleştirilir.

## Desteklenen Braille Karakterleri

Bu proje, Türkçe Braille alfabesinde bulunan temel harfleri destekler:

- **Harfler**: a, b, c, ç, d, e, f, g, ğ, h, ı, i, j, k, l, m, n, o, ö, p, r, s, ş, t, u, v, y, z
- Proje şimdilik a, c, k, l, m, n, o, p, r, t, u, v, y, z harflerini tanımlıyor.

## Dikkat Edilmesi Gerekenler

- **Henüz Tam Desteklenmeyen Karakterler**: Proje, şu an için yalnızca temel Braille harflerini tanıyabilmektedir. Bazı karakterler (noktalama işaretleri gibi) doğru bir şekilde tanınamayabilir veya atlanabilir.

- **Hatalı Tanıma Durumları**: Algoritma bazı durumlarda, özellikle karmaşık veya düşük kaliteli görüntülerde Braille noktalarını doğru tespit edemeyebilir. Bu sorunların çözülmesi için güncellemeler yapılmaktadır.

- **Geliştirme Aşaması**: Yazılım, hala geliştirilme aşamasındadır. Özellikle çeviride yaşanan eksikliklerin giderilmesi ve daha geniş bir karakter yelpazesinin desteklenmesi için çalışmalar sürmektedir.

## Katkıda Bulunma

1. Bu projeyi kendi bilgisayarınıza klonlayın.
2. Geliştirmek veya hata düzeltmek için kodu inceleyin.
3. Değişikliklerinizi **feature-branch** olarak ekleyin.
4. Pull request göndermek için ana projeye katkıda bulunun.

Proje hakkında herhangi bir öneriniz veya hata bildirimleriniz varsa, lütfen bir issue açın veya pull request gönderin.

## Lisans

Bu proje, MIT Lisansı ile lisanslanmıştır. Lisans metni için [Lisans Dosyası](./LICENSE)'na bakın.

## Sorumluluk Reddi

Bu yazılım, sadece eğitim ve kişisel kullanım amaçlarıyla sağlanmaktadır. Hala eksikleri var ve geliştime aşamasındadır. Gerçek dünyada kullanılmadan önce doğruluğu ve güvenilirliği iyice test edilmelidir. Proje, Braille yazılarını dijital ortama çevirmede yardımcı olmayı amaçlamakta olup, gerçek hayatta kullanılan Braille sistemlerinin doğruluğu uzmanlar tarafından onaylanmalıdır.

