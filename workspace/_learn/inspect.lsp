(defun C:DUMP ( / f path la bl ss i e ed typ lay txt cnt blkcnt)
  (setq path (strcat (getvar "DWGPREFIX") "_inventory.txt"))
  (setq f (open path "w"))
  (write-line (strcat "DWG=" (getvar "DWGNAME")) f)
  ;; LAYERS
  (write-line "=== LAYERS ===" f)
  (setq la (tblnext "LAYER" T))
  (while la
    (write-line (strcat "LAYER\t" (cdr (assoc 2 la)) "\tcolor=" (itoa (cdr (assoc 62 la)))) f)
    (setq la (tblnext "LAYER")))
  ;; BLOCKS
  (write-line "=== BLOCKS ===" f)
  (setq bl (tblnext "BLOCK" T))
  (while bl
    (write-line (strcat "BLOCK\t" (cdr (assoc 2 bl))) f)
    (setq bl (tblnext "BLOCK")))
  ;; ENTITY TYPE COUNTS + INSERT names
  (write-line "=== INSERTS (block refs) ===" f)
  (setq ss (ssget "X" '((0 . "INSERT"))))
  (if ss (progn
    (setq i 0)
    (while (< i (sslength ss))
      (setq e (ssname ss i) ed (entget e))
      (write-line (strcat "INSERT\t" (cdr (assoc 2 ed)) "\tlayer=" (cdr (assoc 8 ed))) f)
      (setq i (1+ i)))))
  (close f)
  (princ (strcat "WROTE " path))
  (princ)
)
(C:DUMP)
