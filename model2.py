import pyomo.environ as pyomo

model = pyomo.AbstractModel()

#Conjunto de canciones
model.canciones = pyomo.Set()
model.posiciones = pyomo.Set()

#Parametros del problema
model.numRep = pyomo.Param(model.canciones)
model.sat = pyomo.Param(model.canciones)
model.k = pyomo.Param()

#Variable del problema
model.Y = pyomo.Var(model.canciones,model.posiciones, within=pyomo.Binary)

#Función objetivo
def SatisfaccionTotal(model):
    return sum(model.Y[i,j]
                for i in model.canciones
                for j in model.posiciones)

model.satTotal = pyomo.Objective(rule=SatisfaccionTotal, sense=pyomo.maximize)

#Restricciones
def Rep(model,cancion):
    return sum(model.Y[cancion,j] for j in model.posiciones) == model.numRep[cancion]
model.repContraint = pyomo.Constraint(model.canciones,rule=Rep)

def RepPos(model,posicion):
    return sum(model.Y[i,posicion] for i in model.canciones)  == 1
model.repPosContraint = pyomo.Constraint(model.posiciones,rule=RepPos)

def RepK(model,cancion,posicion):
    val=model.k.value
    if val+posicion>len(model.posiciones):
        val=len(model.posiciones)-posicion
    return (0,sum(model.Y[cancion,posicion+s] for s in range(0,val)),1)
model.repKContraint = pyomo.Constraint(model.canciones,model.posiciones,rule=RepK)

solvername='glpk'
solverpath_folder='.\\glpk\\w64' #does not need to be directly on c drive
solverpath_exe='.\\glpk\\w64\\glpsol' #does not need to be directly on c drive

instance = model.create_instance('dataModel2.dat')
opt=pyomo.SolverFactory(solvername,executable=solverpath_exe)
solver_results = opt.solve(instance)

#instance.pprint()
#print(solver_results)
instance.Y.pprint()
