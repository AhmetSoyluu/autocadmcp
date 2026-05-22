

  (defun v+ (a b) (mapcar '+ a b))
  (defun v- (a b) (mapcar '- a b))
  (defun v* (v s) (mapcar '(lambda (x) (* x s)) v))
  (defun vlen (v) (distance '(0 0 0) v))
  (defun vunit (v / l)
    (setq l (vlen v))
    (if (> l 0.0)
      (v* v (/ 1.0 l))
      '(0 0 0)
    )
  )
  (defun vperp (v) (list (- (cadr v)) (car v) 0.0))
  (defun midpt (a b) (v* (v+ a b) 0.5))

  (defun rect-from-centerline (p1 p2 thk / dir n off a b c d)
    (setq dir (vunit (v- p2 p1)))
    (setq n   (v* (vperp dir) (/ thk 2.0)))
    (setq a (v+ p1 n))
    (setq b (v+ p2 n))
    (setq c (v- p2 n))
    (setq d (v- p1 n))
    (list a b c d)
  )

  (defun bbox-overlap-p (b1 b2 / a1 a2 b1p b2p)
    (setq a1 (car b1) a2 (cadr b1) b1p (car b2) b2p (cadr b2))
    (not
      (or
        (> (car a1) (car b2p))
        (> (car b1p) (car a2))
        (> (cadr a1) (cadr b2p))
        (> (cadr b1p) (cadr a2))
      )
    )
  )

  (defun make-bbox (pts / xs ys)
    (setq xs (mapcar 'car pts))
    (setq ys (mapcar 'cadr pts))
    (list
      (list (apply 'min xs) (apply 'min ys) 0.0)
      (list (apply 'max xs) (apply 'max ys) 0.0)
    )
  )

  (defun ensure-layer (name color / doc layers)
    (setq doc (vla-get-ActiveDocument (vlax-get-acad-object)))
    (setq layers (vla-get-Layers doc))
    (if (not (tblsearch "LAYER" name))
      (progn
        (setq lay (vla-Add layers name))
        (vla-put-Color lay color)
      )
    )
  )

  (defun setup-layers ()
    (ensure-layer "Duvar" 7)
    (ensure-layer "Kapi_Pencere" 2)
    (ensure-layer "Tefris" 3)
    (ensure-layer "Aks" 4)
  )

  (defun set-layer (name) (setvar "CLAYER" name))

  (defun draw-lwpoly (pts closed / data)
    (command "_.PLINE")
    (foreach p pts (command p))
    (if closed (command "_C") (command ""))
  )

  (defun draw-wall (p1 p2 thk / pts)
    (set-layer "Duvar")
    (setq pts (rect-from-centerline p1 p2 thk))
    (draw-lwpoly pts T)
    pts
  )

  (defun draw-axis (p1 p2 label / m)
    (set-layer "Aks")
    (command "_.LINE" p1 p2 "")
    (setq m (midpt p1 p2))
    (command "_.TEXT" "_J" "_MC" m 20 0 label)
  )

  (defun opening-points (wall-p1 wall-p2 start-dist width / dir pA pB)
    (setq dir (vunit (v- wall-p2 wall-p1)))
    (setq pA (v+ wall-p1 (v* dir start-dist)))
    (setq pB (v+ pA (v* dir width)))
    (list pA pB)
  )

  (defun draw-door (wall-p1 wall-p2 wall-thk start-dist door-w swing-side / op pA pB dir n jamb1 jamb2 leaf-end arcpt)
    (set-layer "Kapi_Pencere")
    (setq op  (opening-points wall-p1 wall-p2 start-dist door-w))
    (setq pA  (car op))
    (setq pB  (cadr op))
    (setq dir (vunit (v- wall-p2 wall-p1)))
    (setq n   (v* (vperp dir) (/ wall-thk 2.0)))
    (if (= swing-side "R") (setq n (v* n -1.0)))

    (setq jamb1 (list (v+ pA n) (v- pA n)))
    (setq jamb2 (list (v+ pB n) (v- pB n)))

    (command "_.LINE" (car jamb1) (cadr jamb1) "")
    (command "_.LINE" (car jamb2) (cadr jamb2) "")

    (setq leaf-end (v+ pA (v* dir door-w)))
    (command "_.LINE" pA leaf-end "")
    (setq arcpt (v+ pA (v* n door-w)))
    (command "_.ARC" leaf-end arcpt pA)

    (list pA pB)
  )

  (defun draw-window (wall-p1 wall-p2 wall-thk start-dist win-w sill-depth / op pA pB dir n o1 o2 s1 s2)
    (set-layer "Kapi_Pencere")
    (setq op  (opening-points wall-p1 wall-p2 start-dist win-w))
    (setq pA  (car op))
    (setq pB  (cadr op))
    (setq dir (vunit (v- wall-p2 wall-p1)))
    (setq n   (v* (vperp dir) (/ wall-thk 2.0)))

    (setq o1 (v+ pA n))
    (setq o2 (v+ pB n))
    (setq s1 (v- pA n))
    (setq s2 (v- pB n))

    (command "_.LINE" o1 o2 "")
    (command "_.LINE" s1 s2 "")

    (setq dn (vunit n))
    (command "_.LINE"
             (v- (midpt pA pB) (v* dn sill-depth))
             (v+ (midpt pA pB) (v* dn sill-depth))
             "")
    (list pA pB)
  )

  (defun room-clear-zone (room-min room-max offset)
    (list
      (list (+ (car room-min) offset) (+ (cadr room-min) offset) 0.0)
      (list (- (car room-max) offset) (- (cadr room-max) offset) 0.0)
    )
  )

  (defun rect-pts (pmin pmax)
    (list
      pmin
      (list (car pmax) (cadr pmin) 0.0)
      pmax
      (list (car pmin) (cadr pmax) 0.0)
    )
  )

  (defun place-furniture-rect (pmin pmax placed-list / box ok)
    (setq box (list pmin pmax))
    (setq ok T)
    (foreach b placed-list
      (if (bbox-overlap-p box b) (setq ok nil))
    )
    (if ok
      (progn
        (set-layer "Tefris")
        (draw-lwpoly (rect-pts pmin pmax) T)
        box
      )
      nil
    )
  )

  (defun smart-place-furniture (room-min room-max furn-size circulation placed-list / clear zmin zmax fx fy cand)
    (setq clear  circulation)
    (setq zmin (list (+ (car room-min) clear) (+ (cadr room-min) clear) 0.0))
    (setq zmax (list (- (car room-max) clear) (- (cadr room-max) clear) 0.0))

    (setq fx (car furn-size))
    (setq fy (cadr furn-size))

    (setq candidates
      (list
        (list zmin (list (+ (car zmin) fx) (+ (cadr zmin) fy) 0.0))
        (list (list (- (car zmax) fx) (cadr zmin) 0.0) (list (car zmax) (+ (cadr zmin) fy) 0.0))
        (list (list (car zmin) (- (cadr zmax) fy) 0.0) (list (+ (car zmin) fx) (cadr zmax) 0.0))
        (list (list (- (car zmax) fx) (- (cadr zmax) fy) 0.0) zmax)
      )
    )

    (setq result nil)
    (foreach c candidates
      (if (and (not result)
               (setq cand (place-furniture-rect (car c) (cadr c) placed-list)))
        (setq result cand)
      )
    )
    result
  )

  (defun c:MIMARI_ORNEK ( / disThk icThk placed room1-min room1-max room2-min room2-max)
    (setup-layers)

    (setq disThk 20.0) ; cm
    (setq icThk  10.0) ; cm

    ; Akslar
    (draw-axis '(0 0 0) '(0 800 0) "A")
    (draw-axis '(500 0 0) '(500 800 0) "B")
    (draw-axis '(1000 0 0) '(1000 800 0) "C")

    (draw-axis '(0 0 0) '(1000 0 0) "1")
    (draw-axis '(0 400 0) '(1000 400 0) "2")
    (draw-axis '(0 800 0) '(1000 800 0) "3")

    ; Dış duvarlar
    (draw-wall '(0 0 0) '(1000 0 0) disThk)
    (draw-wall '(1000 0 0) '(1000 800 0) disThk)
    (draw-wall '(1000 800 0) '(0 800 0) disThk)
    (draw-wall '(0 800 0) '(0 0 0) disThk)

    ; İç duvarlar
    (draw-wall '(500 0 0) '(500 800 0) icThk)
    (draw-wall '(0 400 0) '(500 400 0) icThk)

    ; Kapı ve pencere
    (draw-door '(500 0 0) '(500 800 0) icThk 120 90 "L")
    (draw-window '(0 800 0) '(1000 800 0) disThk 150 140 10)
    (draw-window '(1000 0 0) '(1000 800 0) disThk 250 120 10)

    ; Oda sınırları
    (setq room1-min '(20 20 0))
    (setq room1-max '(490 390 0))
    (setq room2-min '(510 20 0))
    (setq room2-max '(980 780 0))

    (setq placed '())

    ; Salon/Yatak odası tipi tefriş
    (setq bed (smart-place-furniture room2-min room2-max '(160 200) 90 placed))
    (if bed (setq placed (cons bed placed)))

    (setq wardrobe (smart-place-furniture room2-min room2-max '(60 180) 90 placed))
    (if wardrobe (setq placed (cons wardrobe placed)))

    ; Oturma/masa örneği
    (setq sofa (smart-place-furniture room1-min room1-max '(90 220) 80 placed))
    (if sofa (setq placed (cons sofa placed)))

    (setq table (smart-place-furniture room1-min room1-max '(90 160) 80 placed))
    (if table (setq placed (cons table placed)))

    (princ "\nMimari taslak olusturuldu.")
    (princ)
  )