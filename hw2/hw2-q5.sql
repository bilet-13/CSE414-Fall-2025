SELECT N.name as n_number,
      A.num_seats as capacity,
      A.model as model
FROM N_Numbers as N, Aircraft_Types as A
WHERE N.mfr_mdl_code = A.atid AND 
      N.name = 'UNIVERSITY OF WASHINGTON';
