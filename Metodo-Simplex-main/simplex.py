import numpy as np
class MetodoSimplex:
  #------------------------Método simplex base---------------------------
  def solve(M,sim,H):
    M=np.array(M,dtype="float64")
    #Selecciona el pivote
    ve=np.argmax(M[-1,:-1])
    vs=np.argmin([(i if i>0 else np.inf) for i in M[:-1,-1]/M[:-1,ve]])
    #Hace el remplazo de la variable
    H[vs]=sim[ve]
    M[vs]=M[vs]/M[vs][ve]
    #Hace ceros en la columna del pivote
    for i in range(len(M)):
      #Realiza el procedimiento solo si la fila no es la del pivote
      if i!=vs:
        M[i]=M[i]*M[vs][ve]-M[vs]*M[i][ve]
    [print(i) for i in M.round(2).tolist()]
    print("\n")
    #Verifica si hay numeros positivos en la ultima fila exceptuando el resultado en p
    if len(M[-1,:-1][M[-1,:-1]>0])>0:
      #Si hay positivos mayores a cero llama a la funcion pero con la nueva matriz
      return MetodoSimplex.solve(M,sim,H)
    #a grega a H un valor resultado para devolver un diccionario con los valores
    H.append("Resultado")
    M[-1][-1]=abs(M[-1][-1])
    return {H[i]: M[i][-1] for i in range(len(H))}
  #------------------------Método dual---------------------------
  #Esta funcion permite hacer la division valida del método dual, la cual solo puede hacerse si son de signo opuesto
  def __divsim(a,b):
    k=[]
    for i in range(len(a)):
      if (a[i]>0 and b[i]<0) or (a[i]<0 and b[i]>0):
        k.append(a[i]/b[i])
      else:
        #Como el algoritmo va a pedir el número más grande agrega un menos infinito para asegurar que nunca sea seleccionado
        k.append(-np.inf)
    return np.array(k)

  def dual(M,sim,H):
    M=np.array(M,dtype="float64")
    #Selecciona al pivote
    vs =np.argmin([i for i in M[:-1,-1]])#Toma el minimo de un arreglo clon de la ultima columna de M
    ve=np.argmax(MetodoSimplex.__divsim(M[-1,:-1],M[vs,:-1]))#Selecciona el máximo de la division realizada
    #Hace el remplazo
    H[vs]=sim[ve]
    M[vs]=M[vs]/M[vs][ve]
    #Hace el despeje
    for i in range(len(M)):
      if i!=vs:
        M[i]=M[i]*M[vs][ve]-M[vs]*M[i][ve]
    print(M,"\n")
    #Si hay numeros negativos en la ultima columna vuelve a ejecutar simplex pero con la nueva matriz
    if len(M[:-1,-1][M[:-1,-1]<0])>0:
      return MetodoSimplex.dual(M,sim,H)
    H.append("Resultado")
    M[-1][-1]=abs(M[-1][-1])
    return {H[i]: M[i][-1] for i in range(len(H))}