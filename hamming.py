parola1 = "cane"
parola2 = "cqne"
count = 0
j=0

for i in range(0,len(parola1)):
 if parola1[i]==parola2[j]:
  count+=0
  j+=1
 else:
  count+=1
  j+=1
  
if count > 0:
 print("ERROR")