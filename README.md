# Vücut Dili Tanıma Uygulaması

Bu proje, vücut dili analizi kullanarak ölü kaldırma egzersizi sırasındaki aşamaları ve tekrar sayısını izlemek için geliştirilmiştir. Egzersiz yaparken doğru formun korunması önemlidir ve bu uygulama, kullanıcılara vücut duruşlarını izleme ve iyileştirme fırsatı sunar.

## Özellikler

- Kamera görüntüsünü kullanarak vücut duruşu analizi
- Aşama tespiti ve aşama değişikliklerinin izlenmesi
- Tekrar sayısının otomatik olarak hesaplanması
- Sınıflandırma olasılığının gösterilmesi
- Tekrar sayısının sıfırlanabilmesi

## Teknolojiler ve Kullanılan Kütüphaneler

Bu projede aşağıdaki teknolojiler ve kütüphaneler kullanılmıştır:

- Python 3.x
- Tkinter
- customtkinter
- pandas
- numpy
- mediapipe
- OpenCV
- scikit-learn
- Pillow (PIL)

## Projenin mantıksal açıklaması
- Tkinter penceresi ve arayüz etiketleri: Tkinter ile bir pencere oluşturulur ve arayüzün tasarımı için etiketler (`sinifEtiketi`, `tekrarEtiketi`, `olasilikEtiketi`) eklenir. Bu etiketler, aşama, tekrar sayısı ve sınıflandırma olasılığı hakkında bilgi vermek için kullanılır.

- Tekrar sayısını sıfırlama: `tekrari_sifirla` adlı bir fonksiyon tanımlanır. Bu fonksiyon, `"SIFIRLA"` düğmesine tıklandığında çağrılır ve `tekrar_sayisi` değişkenini sıfırlar.

- "SIFIRLA" düğmesi: "SIFIRLA" düğmesi, tekrari_sifirla fonksiyonunu çağırmak için kullanılır. Bu düğmeye tıklandığında, tekrar_sayisi sıfırlanır.

- Kamera görüntüsünü gösterme: Kameradan görüntü almak ve bu görüntüyü arayüzde göstermek için bir çerçeve `(cerceve)` ve bir etiket `(lmain)` oluşturulur. Görüntü işleme sonuçları, bu etiket aracılığıyla gösterilir.

- Vücut duruşunu tanıma işlemi: `tani` adlı bir fonksiyon, kameradan görüntü alır, vücut duruşunu tanır ve bu duruşu makine öğrenimi modeline gönderir. Sonuçlar kullanılarak mevcut aşama (örneğin, "up" veya "down"), tekrar sayısı ve sınıflandırma olasılığı belirlenir.

- Görüntü işleme ve çizim: Kameradan alınan görüntü, RGB renk uzayına dönüştürülür ve vücut duruşu noktaları üzerine Mediapipe kullanılarak çizim yapılır.

- Veri çerçevesi ve model: Vücut duruşunu analiz etmek için önceden eğitilmiş bir makine öğrenimi modeli kullanılır. Model, vücut duruşu verilerini alır, sınıflandırma yapar ve sonuçları `vucut_dili_olasilik` ve `vucut_dili_sinif` değişkenlerinde saklar.

- Sürekli güncelleme: tani fonksiyonu sürekli olarak kendisini çağırarak, kameradan alınan görüntüyü işler, sonuçları günceller ve arayüzde gösterir.

- Arayüz güncellemeleri: tani fonksiyonu içinde, tekrar sayısı, olasılık ve mevcut aşama bilgileri arayüzdeki metin kutularında (`tekrarKutusu`, `olasilikKutusu`, `sinifKutusu`) sürekli olarak güncellenir.
