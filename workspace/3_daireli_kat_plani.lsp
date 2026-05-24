(defun c:3_DAIRELI_KAT ()
  ;; ============================================================
  ;; 3 DAİRELİ KAT PLANI - AutoCAD MCP ile Çizim
  ;; Layout: 3 Apartments + Corridor + Stairs + Elevator
  ;; ============================================================

  ;; --- LAYER (KATMAN) TANIMLARI ---
  (command "._-layer" "M" "DIS_DUVAR" "C" "7" "" 
           "M" "ICI_DUVAR" "C" "3" "" 
           "M" "MERDIVEN" "C" "2" "" 
           "M" "ASANSOR" "C" "4" "" 
           "M" "KAPI" "C" "1" "" 
           "M" "PENCERE" "C" "5" "" 
           "M" "YAZI" "C" "7" "" 
           "M" "BALKON" "C" "6" "" 
           "M" "KORIDOR" "C" "8" "" 
           "M" "KOLON" "C" "2" "" 
           "M" "OLCU" "C" "1" "" "")

  ;; ============================================================
  ;; ANA DIS DUVARLAR - Bina Kaba Yapısı (30m x 16m)
  ;; ============================================================
  (setvar "CLAYER" "DIS_DUVAR")
  
  ;; Dış duvar - ana dikdörtgen (30000 x 16000 mm)
  (command "._rectang" "0,0" "30000,16000")
  
  ;; İç kopya (duvar kalınlığı 200mm)
  (command "._offset" "200" (entlast) "100,100")

  ;; ============================================================
  ;; KOLONLAR (40x40 cm)
  ;; ============================================================
  (setvar "CLAYER" "KOLON")
  (command "._rectang" "0,0" "400,400")
  (command "._rectang" "29600,0" "30000,400")
  (command "._rectang" "0,15600" "400,16000")
  (command "._rectang" "29600,15600" "30000,16000")
  
  ;; Orta kolonlar
  (command "._rectang" "9800,0" "10200,400")
  (command "._rectang" "19800,0" "20200,400")
  (command "._rectang" "9800,15600" "10200,16000")
  (command "._rectang" "19800,15600" "20200,16000")

  ;; ============================================================
  ;; KORİDOR (Merkezi yatay koridor - 2000mm genişlik)
  ;; ============================================================
  (setvar "CLAYER" "KORIDOR")
  ;; Koridor duvarları - yatay
  (command "._line" "0,7000" "30000,7000" "")
  (command "._line" "0,9000" "30000,9000" "")
  
  ;; Koridor giriş kapısı (sağ taraftan)
  (command "._break" (entlast) "28000,9000" "29500,9000")

  ;; ============================================================
  ;; DUVAR BÖLMELERİ - 3 Daire
  ;; ============================================================
  (setvar "CLAYER" "ICI_DUVAR")
  
  ;; Daire 1 (Sol) - Dikey bölme duvarı (x=10000)
  (command "._line" "10000,0" "10000,7000" "")
  (command "._line" "10000,9000" "10000,16000" "")
  
  ;; Daire 2 (Orta) - Dikey bölme duvarı (x=20000)
  (command "._line" "20000,0" "20000,7000" "")
  (command "._line" "20000,9000" "20000,16000" "")

  ;; ============================================================
  ;; DAİRE 1 - İÇ DUVARLAR (Sol, Alt: 0-10000, 0-7000)
  ;; ============================================================
  ;; Salon (sol alt)
  (command "._line" "0,3500" "5000,3500" "")
  (command "._line" "5000,0" "5000,3500" "")
  
  ;; Mutfak (sağ alt)
  (command "._line" "5000,3500" "10000,3500" "")
  
  ;; Yatak Odası 1 (sol üst)
  (command "._line" "0,3500" "5000,3500" "")
  
  ;; Yatak Odası 2 (orta üst)
  (command "._line" "5000,3500" "10000,3500" "")
  
  ;; Banyo (sağ üst köşe)
  (command "._line" "7000,5000" "10000,5000" "")
  (command "._line" "7000,5000" "7000,7000" "")

  ;; ============================================================
  ;; DAİRE 1 - ÜST KISIM (0-10000, 9000-16000)
  ;; ============================================================
  ;; Salon (sol üst)
  (command "._line" "0,12500" "5000,12500" "")
  (command "._line" "5000,9000" "5000,12500" "")
  
  ;; Mutfak (sağ üst)
  (command "._line" "5000,12500" "10000,12500" "")
  
  ;; Yatak Odası 1 (sol alt)
  (command "._line" "0,12500" "5000,12500" "")
  
  ;; Yatak Odası 2 (orta alt)
  (command "._line" "5000,12500" "10000,12500" "")
  
  ;; Banyo (sağ alt köşe)
  (command "._line" "7000,11000" "10000,11000" "")
  (command "._line" "7000,11000" "7000,9000" "")

  ;; ============================================================
  ;; DAİRE 2 - İÇ DUVARLAR (Orta, Alt: 10000-20000, 0-7000)
  ;; ============================================================
  ;; Salon (sol alt)
  (command "._line" "10000,3500" "15000,3500" "")
  (command "._line" "15000,0" "15000,3500" "")
  
  ;; Mutfak (sağ alt)
  (command "._line" "15000,3500" "20000,3500" "")
  
  ;; Yatak Odası 1 (sol üst)
  (command "._line" "10000,3500" "15000,3500" "")
  
  ;; Yatak Odası 2 (orta üst)
  (command "._line" "15000,3500" "20000,3500" "")
  
  ;; Banyo (sağ üst köşe)
  (command "._line" "17000,5000" "20000,5000" "")
  (command "._line" "17000,5000" "17000,7000" "")

  ;; ============================================================
  ;; DAİRE 2 - ÜST KISIM (10000-20000, 9000-16000)
  ;; ============================================================
  ;; Salon (sol üst)
  (command "._line" "10000,12500" "15000,12500" "")
  (command "._line" "15000,9000" "15000,12500" "")
  
  ;; Mutfak (sağ üst)
  (command "._line" "15000,12500" "20000,12500" "")
  
  ;; Yatak Odası 1 (sol alt)
  (command "._line" "10000,12500" "15000,12500" "")
  
  ;; Yatak Odası 2 (orta alt)
  (command "._line" "15000,12500" "20000,12500" "")
  
  ;; Banyo (sağ alt köşe)
  (command "._line" "17000,11000" "20000,11000" "")
  (command "._line" "17000,11000" "17000,9000" "")

  ;; ============================================================
  ;; DAİRE 3 - İÇ DUVARLAR (Sağ, Alt: 20000-30000, 0-7000)
  ;; ============================================================
  ;; Salon (sol alt)
  (command "._line" "20000,3500" "25000,3500" "")
  (command "._line" "25000,0" "25000,3500" "")
  
  ;; Mutfak (sağ alt)
  (command "._line" "25000,3500" "30000,3500" "")
  
  ;; Yatak Odası 1 (sol üst)
  (command "._line" "20000,3500" "25000,3500" "")
  
  ;; Yatak Odası 2 (orta üst)
  (command "._line" "25000,3500" "30000,3500" "")
  
  ;; Banyo (sağ üst köşe)
  (command "._line" "27000,5000" "30000,5000" "")
  (command "._line" "27000,5000" "27000,7000" "")

  ;; ============================================================
  ;; DAİRE 3 - ÜST KISIM (20000-30000, 9000-16000)
  ;; ============================================================
  ;; Salon (sol üst)
  (command "._line" "20000,12500" "25000,12500" "")
  (command "._line" "25000,9000" "25000,12500" "")
  
  ;; Mutfak (sağ üst)
  (command "._line" "25000,12500" "30000,12500" "")
  
  ;; Yatak Odası 1 (sol alt)
  (command "._line" "20000,12500" "25000,12500" "")
  
  ;; Yatak Odası 2 (orta alt)
  (command "._line" "25000,12500" "30000,12500" "")
  
  ;; Banyo (sağ alt köşe)
  (command "._line" "27000,11000" "30000,11000" "")
  (command "._line" "27000,11000" "27000,9000" "")

  ;; ============================================================
  ;; MERDİVEN (Koridor ortasında - x: 13000-15500, y: 7000-9000)
  ;; ============================================================
  (setvar "CLAYER" "MERDIVEN")
  
  ;; Merdiven boşluğu duvarları
  (command "._line" "13000,7000" "13000,9000" "")
  (command "._line" "15500,7000" "15500,9000" "")
  (command "._line" "13000,7000" "15500,7000" "")
  (command "._line" "13000,9000" "15500,9000" "")
  
  ;; Merdiven basamakları (10 basamak)
  (setq i 1)
  (while (<= i 9)
    (setq y (+ 7000 (* i 200)))
    (command "._line" "13000,y" "15500,y" "")
    (setq i (1+ i))
  )
  
  ;; Merdiven okları (yön göstergesi)
  (command "._pline" "14250,7100" "14250,8900" "")
  (command "._pline" "14250,8900" "14000,8700" "")
  (command "._pline" "14250,8900" "14500,8700" "")

  ;; ============================================================
  ;; ASANSÖR (Koridor solunda - x: 10500-12500, y: 7000-9000)
  ;; ============================================================
  (setvar "CLAYER" "ASANSOR")
  
  ;; Asansör boşluğu
  (command "._line" "10500,7000" "10500,9000" "")
  (command "._line" "12500,7000" "12500,9000" "")
  (command "._line" "10500,7000" "12500,7000" "")
  (command "._line" "10500,9000" "12500,9000" "")
  
  ;; Asansör kapısı (koridora bakan)
  (command "._line" "11000,7000" "12000,7000" "")
  
  ;; Asansör sembolü - iç kare
  (command "._rectang" "10800,7400" "12200,8600")
  
  ;; Asansör çarpı işareti
  (command "._line" "10800,7400" "12200,8600" "")
  (command "._line" "12200,7400" "10800,8600" "")
  
  ;; Asansör yazısı
  (setvar "CLAYER" "YAZI")
  (command "._text" "J" "MC" "11500,6800" "300" "0" "ASANSÖR")

  ;; ============================================================
  ;; KAPILAR
  ;; ============================================================
  (setvar "CLAYER" "KAPI")
  
  ;; Daire giriş kapıları (koridordan)
  ;; Daire 1 giriş (alt)
  (command "._line" "4500,7000" "4500,7500" "")
  (command "._arc" "4500,7000" "5000,7250" "4500,7500")
  
  ;; Daire 1 giriş (üst)
  (command "._line" "4500,9000" "4500,8500" "")
  (command "._arc" "4500,9000" "5000,8750" "4500,8500")
  
  ;; Daire 2 giriş (alt)
  (command "._line" "14500,7000" "14500,7500" "")
  (command "._arc" "14500,7000" "15000,7250" "14500,7500")
  
  ;; Daire 2 giriş (üst)
  (command "._line" "14500,9000" "14500,8500" "")
  (command "._arc" "14500,9000" "15000,8750" "14500,8500")
  
  ;; Daire 3 giriş (alt)
  (command "._line" "24500,7000" "24500,7500" "")
  (command "._arc" "24500,7000" "25000,7250" "24500,7500")
  
  ;; Daire 3 giriş (üst)
  (command "._line" "24500,9000" "24500,8500" "")
  (command "._arc" "24500,9000" "25000,8750" "24500,8500")

  ;; İç kapılar - Daire 1 Alt
  (command "._line" "5000,2000" "5500,2000" "")
  (command "._arc" "5000,2000" "5250,1500" "5500,2000")
  
  (command "._line" "2000,3500" "2000,4000" "")
  (command "._arc" "2000,3500" "2500,3750" "2000,4000")
  
  (command "._line" "7000,5000" "7500,5000" "")
  (command "._arc" "7000,5000" "7250,4500" "7500,5000")

  ;; İç kapılar - Daire 1 Üst
  (command "._line" "5000,14000" "5500,14000" "")
  (command "._arc" "5000,14000" "5250,13500" "5500,14000")
  
  (command "._line" "2000,12500" "2000,12000" "")
  (command "._arc" "2000,12500" "2500,12250" "2000,12000")
  
  (command "._line" "7000,11000" "7500,11000" "")
  (command "._arc" "7000,11000" "7250,10500" "7500,11000")

  ;; ============================================================
  ;; PENCERELER
  ;; ============================================================
  (setvar "CLAYER" "PENCERE")
  
  ;; Daire 1 - Alt pencere (sol)
  (command "._line" "1000,0" "1000,0" "")
  (command "._line" "1000,-200" "4000,-200" "")
  (command "._line" "1000,0" "1000,-200" "")
  (command "._line" "4000,0" "4000,-200" "")
  
  ;; Daire 1 - Üst pencere (sol)
  (command "._line" "1000,16000" "1000,16200" "")
  (command "._line" "1000,16200" "4000,16200" "")
  (command "._line" "4000,16000" "4000,16200" "")

  ;; Daire 2 - Alt pencere (sol)
  (command "._line" "11000,0" "11000,-200" "")
  (command "._line" "11000,-200" "14000,-200" "")
  (command "._line" "14000,0" "14000,-200" "")
  
  ;; Daire 2 - Üst pencere (sol)
  (command "._line" "11000,16000" "11000,16200" "")
  (command "._line" "11000,16200" "14000,16200" "")
  (command "._line" "14000,16000" "14000,16200" "")

  ;; Daire 3 - Alt pencere (sol)
  (command "._line" "21000,0" "21000,-200" "")
  (command "._line" "21000,-200" "24000,-200" "")
  (command "._line" "24000,0" "24000,-200" "")
  
  ;; Daire 3 - Üst pencere (sol)
  (command "._line" "21000,16000" "21000,16200" "")
  (command "._line" "21000,16200" "24000,16200" "")
  (command "._line" "24000,16000" "24000,16200" "")

  ;; ============================================================
  ;; BALKONLAR
  ;; ============================================================
  (setvar "CLAYER" "BALKON")
  
  ;; Daire 1 - Balkon (sağ alt)
  (command "._rectang" "8000,-2000" "10000,-500")
  
  ;; Daire 1 - Balkon (sağ üst)
  (command "._rectang" "8000,16500" "10000,18000")
  
  ;; Daire 2 - Balkon (sağ alt)
  (command "._rectang" "18000,-2000" "20000,-500")
  
  ;; Daire 2 - Balkon (sağ üst)
  (command "._rectang" "18000,16500" "20000,18000")
  
  ;; Daire 3 - Balkon (sağ alt)
  (command "._rectang" "28000,-2000" "30000,-500")
  
  ;; Daire 3 - Balkon (sağ üst)
  (command "._rectang" "28000,16500" "30000,18000")

  ;; ============================================================
  ;; YAZILAR / ETİKETLER
  ;; ============================================================
  (setvar "CLAYER" "YAZI")
  
  ;; Daire etiketleri
  (command "._text" "J" "MC" "5000,5250" "400" "0" "DAİRE 1")
  (command "._text" "J" "MC" "5000,13250" "400" "0" "DAİRE 1")
  (command "._text" "J" "MC" "15000,5250" "400" "0" "DAİRE 2")
  (command "._text" "J" "MC" "15000,13250" "400" "0" "DAİRE 2")
  (command "._text" "J" "MC" "25000,5250" "400" "0" "DAİRE 3")
  (command "._text" "J" "MC" "25000,13250" "400" "0" "DAİRE 3")
  
  ;; Oda etiketleri - Daire 1 Alt
  (command "._text" "J" "MC" "2500,1750" "250" "0" "SALON")
  (command "._text" "J" "MC" "7500,1750" "250" "0" "MUTFAK")
  (command "._text" "J" "MC" "2500,5250" "250" "0" "Y.Odası")
  (command "._text" "J" "MC" "7500,5250" "250" "0" "Y.Odası")
  (command "._text" "J" "MC" "8500,6000" "200" "0" "BANYO")
  
  ;; Oda etiketleri - Daire 1 Üst
  (command "._text" "J" "MC" "2500,10750" "250" "0" "SALON")
  (command "._text" "J" "MC" "7500,10750" "250" "0" "MUTFAK")
  (command "._text" "J" "MC" "2500,14250" "250" "0" "Y.Odası")
  (command "._text" "J" "MC" "7500,14250" "250" "0" "Y.Odası")
  (command "._text" "J" "MC" "8500,10000" "200" "0" "BANYO")
  
  ;; Oda etiketleri - Daire 2 Alt
  (command "._text" "J" "MC" "12500,1750" "250" "0" "SALON")
  (command "._text" "J" "MC" "17500,1750" "250" "0" "MUTFAK")
  (command "._text" "J" "MC" "12500,5250" "250" "0" "Y.Odası")
  (command "._text" "J" "MC" "17500,5250" "250" "0" "Y.Odası")
  (command "._text" "J" "MC" "18500,6000" "200" "0" "BANYO")
  
  ;; Oda etiketleri - Daire 2 Üst
  (command "._text" "J" "MC" "12500,10750" "250" "0" "SALON")
  (command "._text" "J" "MC" "17500,10750" "250" "0" "MUTFAK")
  (command "._text" "J" "MC" "12500,14250" "250" "0" "Y.Odası")
  (command "._text" "J" "MC" "17500,14250" "250" "0" "Y.Odası")
  (command "._text" "J" "MC" "18500,10000" "200" "0" "BANYO")
  
  ;; Oda etiketleri - Daire 3 Alt
  (command "._text" "J" "MC" "22500,1750" "250" "0" "SALON")
  (command "._text" "J" "MC" "27500,1750" "250" "0" "MUTFAK")
  (command "._text" "J" "MC" "22500,5250" "250" "0" "Y.Odası")
  (command "._text" "J" "MC" "27500,5250" "250" "0" "Y.Odası")
  (command "._text" "J" "MC" "28500,6000" "200" "0" "BANYO")
  
  ;; Oda etiketleri - Daire 3 Üst
  (command "._text" "J" "MC" "22500,10750" "250" "0" "SALON")
  (command "._text" "J" "MC" "27500,10750" "250" "0" "MUTFAK")
  (command "._text" "J" "MC" "22500,14250" "250" "0" "Y.Odası")
  (command "._text" "J" "MC" "27500,14250" "250" "0" "Y.Odası")
  (command "._text" "J" "MC" "28500,10000" "200" "0" "BANYO")
  
  ;; Koridor etiketi
  (command "._text" "J" "MC" "15000,8000" "300" "0" "KORİDOR")
  
  ;; Merdiven etiketi
  (command "._text" "J" "MC" "14250,8000" "250" "0" "MERDİVEN")
  
  ;; Balkon etiketleri
  (command "._text" "J" "MC" "9000,-1250" "200" "0" "BALKON")
  (command "._text" "J" "MC" "9000,17250" "200" "0" "BALKON")
  (command "._text" "J" "MC" "19000,-1250" "200" "0" "BALKON")
  (command "._text" "J" "MC" "19000,17250" "200" "0" "BALKON")
  (command "._text" "J" "MC" "29000,-1250" "200" "0" "BALKON")
  (command "._text" "J" "MC" "29000,17250" "200" "0" "BALKON")

  ;; ============================================================
  ;; ÖLÇÜLENDİRME
  ;; ============================================================
  (setvar "CLAYER" "OLCU")
  
  ;; Toplam bina genişliği
  (command "._dimlinear" "0,16500" "30000,16500" "15000,17000")
  
  ;; Daire genişlikleri
  (command "._dimlinear" "0,16500" "10000,16500" "5000,17000")
  (command "._dimlinear" "10000,16500" "20000,16500" "15000,17000")
  (command "._dimlinear" "20000,16500" "30000,16500" "25000,17000")
  
  ;; Toplam bina yüksekliği
  (command "._dimlinear" "-1000,0" "-1000,16000" "-2000,8000")
  
  ;; Koridor genişliği
  (command "._dimlinear" "0,7000" "0,9000" "-1000,8000")

  ;; ============================================================
  ;; BAŞLIK VE AÇIKLAMALAR
  ;; ============================================================
  (setvar "CLAYER" "YAZI")
  
  ;; Ana başlık
  (command "._text" "J" "MC" "15000,19000" "600" "0" "3 DAİRELİ KAT PLANI")
  (command "._text" "J" "MC" "15000,18500" "300" "0" "Koridor, Merdiven ve Asansörlü")
  
  ;; Ölçek bilgisi
  (command "._text" "J" "MC" "15000,-3000" "250" "0" "ÖLÇEK: 1/100")
  (command "._text" "J" "MC" "15000,-3500" "200" "0" "Tüm ölçüler milimetredir (mm)")

  (princ)
)

;; Çizimi çalıştır
(c:3_DAIRELI_KAT)
