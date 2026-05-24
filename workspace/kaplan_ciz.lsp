;; ============================================
;; KAPLAN ÇİZİMİ - Kaplan Yüzü Portresi
;; AutoCAD üzerinde canlı çizim
;; ============================================

(defun c:kaplan ()
  (setq old_osmode (getvar "osmode"))
  (setvar "osmode" 0)
  (setvar "cmdecho" 0)
  
  ;; Başlangıç noktası
  (setq cx 0 cy 0)
  
  (princ "\n--- Kaplan Çiziliyor... ---")
  
  ;; ========== ANA HATLAR ==========
  
  ;; 1. Kafa dış çemberi (ana hat)
  (command "_.circle" (list cx cy) 100)
  
  ;; 2. Sol kulak
  (command "_.ellipse" (list (- cx 70) (+ cy 80)) (list (- cx 40) (+ cy 80)) 30)
  
  ;; 3. Sağ kulak
  (command "_.ellipse" (list (+ cx 70) (+ cy 80)) (list (+ cx 40) (+ cy 80)) 30)
  
  ;; 4. Sol kulak içi
  (command "_.ellipse" (list (- cx 65) (+ cy 78)) (list (- cx 45) (+ cy 78)) 18)
  
  ;; 5. Sağ kulak içi
  (command "_.ellipse" (list (+ cx 65) (+ cy 78)) (list (+ cx 45) (+ cy 78)) 18)
  
  ;; ========== GÖZLER ==========
  
  ;; 6. Sol göz dış
  (command "_.ellipse" (list (- cx 35) (+ cy 25)) (list (- cx 20) (+ cy 25)) 15)
  
  ;; 7. Sağ göz dış
  (command "_.ellipse" (list (+ cx 35) (+ cy 25)) (list (+ cx 20) (+ cy 25)) 15)
  
  ;; 8. Sol göz bebeği
  (command "_.circle" (list (- cx 30) (+ cy 25)) 7)
  (command "_.hatch" "_SOLID" (entlast) "")
  
  ;; 9. Sağ göz bebeği
  (command "_.circle" (list (+ cx 30) (+ cy 25)) 7)
  (command "_.hatch" "_SOLID" (entlast) "")
  
  ;; 10. Sol göz ışıltı
  (command "_.circle" (list (- cx 27) (+ cy 28)) 2.5)
  (command "_.hatch" "_SOLID" (entlast) "")
  
  ;; 11. Sağ göz ışıltı
  (command "_.circle" (list (+ cx 33) (+ cy 28)) 2.5)
  (command "_.hatch" "_SOLID" (entlast) "")
  
  ;; ========== BURUN ==========
  
  ;; 12. Burun (üçgenimsi)
  (command "_.pline"
    (list (- cx 12) (- cy 5))
    (list cx (- cy 15))
    (list (+ cx 12) (- cy 5))
    "c"
  )
  (command "_.hatch" "_SOLID" (entlast) "")
  
  ;; 13. Burun delikleri
  (command "_.circle" (list (- cx 5) (- cy 8)) 2)
  (command "_.circle" (list (+ cx 5) (- cy 8)) 2)
  
  ;; ========== AĞIZ ==========
  
  ;; 14. Ağız çizgisi
  (command "_.pline"
    (list (- cx 15) (- cy 18))
    (list cx (- cy 25))
    (list (+ cx 15) (- cy 18))
    ""
  )
  
  ;; 15. Alt çene hattı
  (command "_.pline"
    (list (- cx 20) (- cy 20))
    (list cx (- cy 35))
    (list (+ cx 20) (- cy 20))
    ""
  )
  
  ;; ========== Bıyıklar ==========
  
  ;; 16. Sol bıyıklar (3 adet)
  (command "_.line" (list (- cx 15) (- cy 5)) (list (- cx 70) (- cy 15)) "")
  (command "_.line" (list (- cx 15) (- cy 8)) (list (- cx 70) (- cy 8)) "")
  (command "_.line" (list (- cx 15) (- cy 11)) (list (- cx 70) (- cy 1)) "")
  
  ;; 17. Sağ bıyıklar (3 adet)
  (command "_.line" (list (+ cx 15) (- cy 5)) (list (+ cx 70) (- cy 15)) "")
  (command "_.line" (list (+ cx 15) (- cy 8)) (list (+ cx 70) (- cy 8)) "")
  (command "_.line" (list (+ cx 15) (- cy 11)) (list (+ cx 70) (- cy 1)) "")
  
  ;; ========== KAPLAN ÇİZGİLERİ (alın) ==========
  
  ;; 18. Alın çizgileri - "W" şeklinde
  (command "_.pline"
    (list (- cx 30) (+ cy 55))
    (list (- cx 15) (+ cy 45))
    (list cx (+ cy 55))
    (list (+ cx 15) (+ cy 45))
    (list (+ cx 30) (+ cy 55))
    ""
  )
  
  (command "_.pline"
    (list (- cx 25) (+ cy 60))
    (list (- cx 10) (+ cy 50))
    (list cx (+ cy 60))
    (list (+ cx 10) (+ cy 50))
    (list (+ cx 25) (+ cy 60))
    ""
  )
  
  ;; 19. Yanak çizgileri
  (command "_.line" (list (- cx 50) (- cy 10)) (list (- cx 40) (- cy 20)) "")
  (command "_.line" (list (- cx 55) (- cy 5)) (list (- cx 45) (- cy 15)) "")
  (command "_.line" (list (+ cx 50) (- cy 10)) (list (+ cx 40) (- cy 20)) "")
  (command "_.line" (list (+ cx 55) (- cy 5)) (list (+ cx 45) (- cy 15)) "")
  
  ;; ========== ÇENE ==========
  
  ;; 20. Çene altı tüyleri
  (command "_.line" (list (- cx 15) (- cy 40)) (list (- cx 5) (- cy 50)) "")
  (command "_.line" (list (+ cx 15) (- cy 40)) (list (+ cx 5) (- cy 50)) "")
  (command "_.line" (list cx (- cy 42)) (list cx (- cy 52)) "")
  
  ;; ========== KAŞLAR ==========
  
  ;; 21. Kaşlar
  (command "_.pline"
    (list (- cx 50) (+ cy 40))
    (list (- cx 35) (+ cy 45))
    (list (- cx 20) (+ cy 40))
    ""
  )
  
  (command "_.pline"
    (list (+ cx 50) (+ cy 40))
    (list (+ cx 35) (+ cy 45))
    (list (+ cx 20) (+ cy 40))
    ""
  )
  
  ;; ========== RENKLENDİRME ==========
  
  ;; Kafa ana rengi - turuncu/sarı
  (command "_.circle" (list cx cy) 100)
  (setq head_ent (entlast))
  (command "_.hatch" "_SOLID" head_ent "")
  (command "_.chprop" head_ent "" "_color" 40 "")  ;; Turuncu renk
  
  ;; Kulak içleri - pembe
  ;; (Not: Hatch işlemleri için layer yönetimi)
  
  (setvar "osmode" old_osmode)
  (setvar "cmdecho" 1)
  (princ "\n--- Kaplan çizimi tamamlandı! ---")
  (princ)
)

;; Çizimi çalıştır
(c:kaplan)
