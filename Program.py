import tkinter as tk
import customtkinter as ck

import pandas as pd
import numpy as np
import pickle

import mediapipe as mp
import cv2
from PIL import Image, ImageTk

from landmarks import landmarks

pencere = tk.Tk()
pencere.geometry("480x700")
pencere.title("Vücut Dili Tanıma Uygulaması")
ck.set_appearance_mode("dark")

# Arayüzdeki etiketleri oluştur
sinifEtiketi = ck.CTkLabel(pencere, height=40, width=120, font=("Arial", 20), text_color="black", padx=10)
sinifEtiketi.place(x=10, y=1)
sinifEtiketi.configure(text='AŞAMA')  # Vücut dili sınıfı etiketi
tekrarEtiketi = ck.CTkLabel(pencere, height=40, width=120, font=("Arial", 20), text_color="black", padx=10)
tekrarEtiketi.place(x=160, y=1)
tekrarEtiketi.configure(text='TEKRAR')  # Tekrar sayısı etiketi
olasilikEtiketi = ck.CTkLabel(pencere, height=40, width=120, font=("Arial", 20), text_color="black", padx=10)
olasilikEtiketi.place(x=300, y=1)
olasilikEtiketi.configure(text='OLASILIK')  # Sınıflandırma olasılığı etiketi
sinifKutusu = ck.CTkLabel(pencere, height=40, width=120, font=("Arial", 20), text_color="white", fg_color="blue")
sinifKutusu.place(x=10, y=41)
sinifKutusu.configure(text='0')  # Vücut dili sınıfı kutusu
tekrarKutusu = ck.CTkLabel(pencere, height=40, width=120, font=("Arial", 20), text_color="white", fg_color="blue")
tekrarKutusu.place(x=160, y=41)
tekrarKutusu.configure(text='0')  # Tekrar sayısı kutusu
olasilikKutusu = ck.CTkLabel(pencere, height=40, width=120, font=("Arial", 20), text_color="white", fg_color="blue")
olasilikKutusu.place(x=300, y=41)
olasilikKutusu.configure(text='0')  # Sınıflandırma olasılığı kutusu

# Tekrar sayısını sıfırlamak için bir fonksiyon tanımla
def tekrari_sifirla():
    global tekrar_sayisi
    tekrar_sayisi = 0

# Tekrar sayısını sıfırlamak için bir düğme oluştur
sifirla_dugmesi = ck.CTkButton(pencere, text='SIFIRLA', command=tekrari_sifirla, height=40, width=120,
                               font=("Arial", 20), text_color="white", fg_color="blue")
sifirla_dugmesi.place(x=10, y=600)

# Kamera görüntüsünü göstermek için bir çerçeve oluştur
cerceve = tk.Frame(height=480, width=480)
cerceve.place(x=10, y=90)
lmain = tk.Label(cerceve)
lmain.place(x=0, y=0)

# Mediapipe kütüphanesini kullanarak vücut duruşunu çizmek için gerekli nesneleri tanımla
mp_cizim = mp.solutions.drawing_utils
mp_poz = mp.solutions.pose
poz = mp_poz.Pose(min_tracking_confidence=0.5, min_detection_confidence=0.5)

# Önceden eğitilmiş makine öğrenimi modelini yükle
with open('deadlift.pkl', 'rb') as f:
    model = pickle.load(f)

# Kamerayı aç
kamera = cv2.VideoCapture(0)
# Başlangıç değerlerini tanımla
mevcut_asama = ''
tekrar_sayisi = 0
vucut_dili_olasilik = np.array([0, 0])
vucut_dili_sinif = ''

# Vücut dili tanıma işlemini gerçekleştirmek için bir fonksiyon tanımla
def tani():
    global mevcut_asama
    global tekrar_sayisi
    global vucut_dili_sinif
    global vucut_dili_olasilik

    # Kameradan bir kare al
    ret, kare = kamera.read()
    # Kareyi RGB renk uzayına dönüştür
    goruntu = cv2.cvtColor(kare, cv2.COLOR_BGR2RGB)
    # Kareyi mediapipe kütüphanesine gönder ve sonuçları al
    sonuclar = poz.process(goruntu)
    # Sonuçlardaki vücut duruşu noktalarını ve bağlantılarını kare üzerine çiz
    mp_cizim.draw_landmarks(goruntu, sonuclar.pose_landmarks, mp_poz.POSE_CONNECTIONS,
                           mp_cizim.DrawingSpec(color=(106, 13, 173), thickness=4, circle_radius=5),
                           mp_cizim.DrawingSpec(color=(255, 102, 0), thickness=5, circle_radius=10))

    try:
        # Sonuçlardaki vücut duruşu noktalarının x, y, z ve görünürlük değerlerini bir liste haline getir
        satir = np.array([[son.x, son.y, son.z, son.visibility] for son in sonuclar.pose_landmarks.landmark]).flatten().tolist()
        # Listeyi bir pandas veri çerçevesine dönüştür ve sütun isimlerini landmarks dosyasından al
        X = pd.DataFrame([satir], columns=landmarks)
        # Veri çerçevesini makine öğrenimi modeline gönder ve sınıflandırma olasılıklarını ve sınıfı al
        vucut_dili_olasilik = model.predict_proba(X)[0]
        vucut_dili_sinif = model.predict(X)[0]

        # Eğer sınıf "down" ise ve olasılık 0.7'den büyük ise, mevcut aşamayı "down" olarak güncelle
        if vucut_dili_sinif == "down" and vucut_dili_olasilik[vucut_dili_olasilik.argmax()] > 0.7:
            mevcut_asama = "down"
        # Eğer mevcut aşama "down" ise ve sınıf "up" ise ve olasılık 0.7'den büyük ise, mevcut aşamayı "up" olarak güncelle ve tekrar sayısını artır
        elif mevcut_asama == "down" and vucut_dili_sinif == "up" and vucut_dili_olasilik[vucut_dili_olasilik.argmax()] > 0.7:
            mevcut_asama = "up"
            tekrar_sayisi += 1

    except Exception as hata:
        print(hata)

    # Kareyi kırp ve bir PIL görüntüsüne dönüştür
    img = goruntu[:, :460, :]
    imgarr = Image.fromarray(img)
    # PIL görüntüsünü tkinter uyumlu bir görüntüye dönüştür
    imgtk = ImageTk.PhotoImage(imgarr)
    lmain.imgtk = imgtk
    # Çerçeveyi tkinter uyumlu görüntü ile güncelle
    lmain.configure(image=imgtk)
    # Fonksiyonu tekrar çağır (sonsuz döngü)
    lmain.after(10, tani)

    # Arayüzdeki kutuları tekrar sayısı, olasılık ve aşama değerleri ile güncelle
    tekrarKutusu.configure(text=tekrar_sayisi)
    olasilikKutusu.configure(text=vucut_dili_olasilik[vucut_dili_olasilik.argmax()])
    sinifKutusu.configure(text=mevcut_asama)

# Vücut dili tanıma fonksiyonunu çağır
tani()
# Arayüzün çalışmasını sağla
pencere.mainloop()
