SELECT N.name as n_number,
      AT.num_seats as capacity,
      AT.model as model
FROM N_Numbers as N, Aircraft_Types as AT
WHERE N.mfr_mdl_code = AT.atid AND 
      N.name = 'UNIVERSITY OF WASHINGTON';
