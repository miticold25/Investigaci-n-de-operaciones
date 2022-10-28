import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

class Condicion:
  MENOR_IGUAL=0
  MAYOR_IGUAL=1
  MENOR=2
  MAYOR=3
  def __init__(self,coeficiente:float,corte:float, tipo:int=MENOR, en='y'):

    self.coeficiente=coeficiente
    self.corte=corte
    self.tipo=tipo
    self.en=en
    self.funcion=None

  def __add__(self,other):
    '''
    Estas operaciones no se supone deban usarse por el usuario, son solo para poder hacer calculos sobre las intersecciones entre dos funciones.
    '''
    return Condicion(self.coeficiente+other.coeficiente,self.corte+other.corte,self.tipo)

  def __sub__(self,other):
    '''
    Estas operaciones no se supone deban usarse por el usuario, son solo para poder hacer calculos sobre las intersecciones entre dos funciones.
    '''
    return Condicion(self.coeficiente-other.coeficiente,self.corte-other.corte,self.tipo)

  def __repr__(self):
    #Muestra la funcion
    if self.en=='y':
      return "y {} {}x+({})".format(["<=",">=","<",">"][self.tipo],self.coeficiente,self.corte)
    return "x {} ({})".format(["<=",">=","<",">"][self.tipo],self.corte)

  def condicion(valor:float, tipo:int, en:str):
    '''
    Es un método que permite hacer una condicion simple por ejemplo y<3 o x>=5
    '''
    return Condicion(0,valor,tipo,en)

  def getCorte(self):
    #Retorna los puntos de corte con el eje horizontal y el eje vertical
    return ((0,self.corte),((-self.corte)/self.coeficiente,0))

  def __evaluar(self,x):
    #Evalua un valor como si fuera una igualdad
    if self.en=='x':
      return np.nan
        
    if self.funcion==None:
      self.funcion=lambda x:self.coeficiente*x+self.corte
    return self.funcion(x)

  
  def evaluar(self,x):
    #Evalua un valor como si fuera una igualdad, pero retorna la salida que mejor se ajuste a la solucion dada, por ejemplo si es una recta vertical
    #retorna en x el punto en el que es valido y para y dos puntos que la describen
    if self.en=='x':
      return np.array(2*[self.corte]), np.array([-1000,1000])
        
    if self.funcion==None:
      self.funcion=lambda x:self.coeficiente*x+self.corte
    return x,self.funcion(x)

  def evaluarCondicion(self,x,y=0):
    #evalua si se cumple la condicion para un numero dado, redondeado a 5 decimales.
    f=[lambda a,b: a<=b,lambda a,b: a>=b][self.tipo%2]
    if self.en=='y':
      return f(round(y,5),round(self.__evaluar(x),5))
    else:
      return f(x,self.corte)

  def getInterseccion(self, other):
    #Calcula la interseccion de dos rectas
    #Si una interseccion no es posible se retorna None
    if ((self.en=='x' or other.en=='x') and not(self.en=='x' and other.en=='x')):
      a,b=(self,other) if self.en=='x' else (other,self)
      return a.corte, b.__evaluar(a.corte)
    

    if (self.en=='y' and other.en=='y'):
      p=(self-other).getCorte()[1][0]
      return p,self.__evaluar(p)
    return 0,np.nan


    class Solver:
  def __init__(self, condiciones):
    '''
    Solver se encargará de hallar los vertices y de optimizar la funcion objetivo,
    sin embargo no se va a pedir la funcion objetivo en el constructor
    '''
    self.condiciones=condiciones
  def __puntos(self):
    #Retorna todas las intersecciones, pues se quiere poder utilizarlas para optimizar la funcion objetivo
    k=self.condiciones
    p=[]
    #Pasa por todas las posibles interseccionas y guarda los puntos en p
    for i in range(len(k)):
      for j in range(i+1,len(k)):
        try:
          p.append(k[i].getInterseccion(k[j]))
        except:
          pass
    return p

  def vertices(self):
    #Vertices es una funcion que solo retorna las intersecciones válidas que cumplan todas las condiciones
    p=self.__puntos()
    s=p[:]
    for i in self.condiciones:
      for j in p:
        #Si el vertice no cumple la condicion es eliminado de s
        try:
          if (not i.evaluarCondicion(j[0],j[1])):
            if j in s:
              s.remove(j)
        except:
          pass
    return s
  
  def optimizar(self,funcionObjetivo=lambda x,y: x+y, modo='max',integer=False):
    #optimizar es una funcion que dado un conjunto de puntos evalua la funcion objetivo y determina cual es el maximo o el minimo
    puntos=self.vertices()
    valores=[]
    #Evalua la funcion objetivo en todos los puntos validos
    for i in range(len(puntos)):
      if integer:
        puntos[i]=(int(puntos[i][0]),int(puntos[i][1]))
    for i in puntos:
      valores.append(funcionObjetivo(i[0],i[1]))
    valores=np.array(valores)
    #Retorna un valor u otro dependiendo del modo, si es min el minimo y si es max el maximo
    for i in range(len(valores)):
      print(puntos[i],valores[i])
    if modo=='max':
      return puntos[np.argmax(valores)], valores.max()
    else:
      return puntos[np.argmax(-valores)], valores.min()

      class Graficador:
  def __init__(self,condiciones,solver,xlims,ylims):
    self.condiciones=condiciones
    self.xlims=xlims
    self.ylims=ylims
    self.solver=solver
  def plot(self):
    #Grafica la región solucion y tambien las rectas que lo definen
    condiciones,xlims,ylims,solver=self.condiciones,self.xlims,self.ylims,self.solver

    #Para colorear la región solucion se crea un mapa de puntos del espacio del plano utilizado
    X__=[np.linspace(xlims[0],xlims[1],300),np.linspace(ylims[0],ylims[1],300)]
    Y__=None
    #se asigna un valor de altura en cada caso si cumple la condicion, el area de altura 0 es la solucion y todo por debajo de eso, no.
    for i in condiciones:
      temp=np.array([[i.evaluarCondicion(x0,x1) for x0 in X__[0]] for x1 in X__[1]],dtype="int64")
      if type(Y__)==type(None):
        Y__=-temp
        continue
      Y__-=temp
    #crea un color map que determina un color blanco para los puntos cuya altura sea mas pequeña y cyan para aquellos que sea mas alta
    cmap = ListedColormap(["white","cyan"])
    plt.figure(figsize=(7,7))
    #Se crea la rejilla de color utilizando una función -ReLu modificada
    plt.pcolormesh(X__[0],X__[1],-np.minimum(Y__.min()+1,Y__),cmap=cmap)
    plt.xlim(xlims[0],xlims[1])
    plt.ylim(ylims[0],ylims[1])

    #Toma el eje horizontal del mapa
    x=X__[0]

    y=np.array(solver.vertices()).T
    #Dibuja los vetices válidos
    plt.scatter(xlims[0]-1,0,color="cyan",label="Región Solución")
    if len(y)>0:
      plt.scatter(y[0],y[1],color="red")
    plt.grid()
    #Dibuja las diferentes rectas
    for i in condiciones:
        xi,yi=i.evaluar(x)
        plt.plot(xi,yi)
    plt.legend()

    
class MetodoGrafico:
  #Guarda todos los procedimiento de forma reducida
  def visualizacion(condiciones, xlims, ylims):
    #Crea un solver de las condiciones dadas
    solver=Solver(condiciones)
    #Grafica la situación
    graf=Graficador(condiciones,solver,xlims,ylims).plot()
  
  def optimizar(condiciones,funcionObjetivo,modo,integer=False):
    #optimiza según el modo creando el solver y pasando el modo de solucion
    solver=Solver(condiciones)
    try:
      return solver.optimizar(funcionObjetivo,modo,integer=integer)
    except:
      return 0
  def vertices(condiciones):
    solver=Solver(condiciones)
    return solver.vertices()