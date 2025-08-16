function frecv_rel=lab3_urna_bile(NrSim, cerinta)
  cnt1 = 0;
  cnt2 = 0;
  for i = 1 : NrSim
    extragere = randsample(["R", "R", "R", "R", "R", "A", "A", "A", "V", "V"], 3, replacement = false);
    if extragere(1) == "R" || extragere(2) == "R" || extragere(3) == "R"
      cnt1++;
      if extragere(1) == "R" && extragere(2) == "R" && extragere(3) == "R"
        cnt2++;
      endif
    endif
  endfor
  if cerinta == 1
    frecv_rel = cnt1/NrSim;
  endif
  if cerinta == 2
    frecv_rel = cnt2/NrSim;
  endif
  if cerinta == 3
    frecv_rel = cnt2/cnt1;
  endif
  if cerinta == 4
    frecv_rel = cnt2/cnt1;
  endif

