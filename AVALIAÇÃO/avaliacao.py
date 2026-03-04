from lista_competencias import lista_competencias

soma = 0

for competencias in lista_competencias:
  while True:
    nota = input(f'Qual sua nota para: {competencias}? (B - Bom, R - Regular e I - Ruim) ').upper()

    if nota in ['B', 'R', 'I']:
      if nota == 'B':
        soma += 3
      elif nota == 'R':
        soma += 2
      elif nota == 'I':
        soma += 1
      break 

    else:    
      print(f'Letra inserida incorretamente!')

print("A sua média é: " + str(soma/len(lista_competencias)))