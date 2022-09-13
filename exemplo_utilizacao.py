qt_pc = 1

dados_pc = { 
  "proc": "i7",
  "ram": "8GB",
  "tipo_sis": "Baseado em 64x bits",
  "win_edition": "Windows 10 Pro for Workstations",
  "versao": "21H2"
  }

for x in range(0,3):
  print("Endereço {} \n{:<8} {:<8} {:<29} {:<8}".format(qt_pc,dados_pc["proc"], dados_pc["ram"],dados_pc["tipo_sis"],dados_pc["win_edition"]))
  qt_pc+=1

for x in range(0,3):
  print("Endereço {} \n{:<8} {:<8} {:<29} {:<8}".format(qt_pc,dados_pc["proc"], dados_pc["ram"],dados_pc["tipo_sis"],dados_pc["win_edition"]))
  qt_pc+=1