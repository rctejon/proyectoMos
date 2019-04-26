import pyomo.environ as pyomo

model = pyomo.AbstractModel()

#Conjunto de canciones
model.canciones = pyomo.Set()

#Parametros del problema
model.tiempos = pyomo.Param(model.canciones)
model.sat = pyomo.Param(model.canciones)
model.repMin = pyomo.Param(model.canciones)
model.repMax = pyomo.Param(model.canciones)
model.horasMax = pyomo.Param()
model.horasMin = pyomo.Param()
model.populares = pyomo.Param(model.canciones)
model.rock = pyomo.Param(model.canciones)
model.clasicas = pyomo.Param(model.canciones)
model.rockMin = 1
model.rockMax = 3
model.popuMin = 1
model.popuMax = 3
model.clasMin = 1
model.clasMax = 3

#Variable del problema
model.X = pyomo.Var(model.canciones, within=pyomo.NonNegativeIntegers)

#Función objetivo
def SatisfaccionTotal(model):
    return sum(model.X[i]*model.sat[i] for i in model.canciones)

model.satTotal = pyomo.Objective(rule=SatisfaccionTotal, sense=pyomo.maximize)

#Restricciones
def HorasMin(model):
    return sum(model.X[i]*model.tiempos[i] for i in model.canciones) >= model.horasMin
model.horasMinContraint = pyomo.Constraint(rule=HorasMin)

def HorasMax(model):
    return sum(model.X[i]*model.tiempos[i] for i in model.canciones) <= model.horasMax
model.horasMaxContraint = pyomo.Constraint(rule=HorasMax)

def RockMin(model):
    return sum(model.X[i]*model.rock[i] for i in model.canciones) >= model.rockMin
model.rockMinContraint = pyomo.Constraint(rule=RockMin)

def RockMax(model):
    return sum(model.X[i]*model.rock[i] for i in model.canciones) <= model.rockMax
model.rockMaxContraint = pyomo.Constraint(rule=RockMax)

def ClasicasMin(model):
    return sum(model.X[i]*model.clasicas[i] for i in model.canciones) >= model.clasMin
model.clasicasMinContraint = pyomo.Constraint(rule=ClasicasMin)

def ClasicasMax(model):
    return sum(model.X[i]*model.clasicas[i] for i in model.canciones) <= model.clasMax
model.clasicasMaxContraint = pyomo.Constraint(rule=ClasicasMax)

def PopularesMin(model):
    return sum(model.X[i]*model.populares[i] for i in model.canciones) >= model.popuMin
model.popularesMinContraint = pyomo.Constraint(rule=PopularesMin)

def PopularesMax(model):
    return sum(model.X[i]*model.populares[i] for i in model.canciones) <= model.popuMax
model.popularesMaxContraint = pyomo.Constraint(rule=PopularesMax)

def RepMin(model,cancion):
    return model.X[cancion] >= model.repMin[cancion]
model.repMinContraint = pyomo.Constraint(model.canciones,rule=RepMin)

def RepMax(model,cancion):
    return model.X[cancion] <= model.repMax[cancion]
model.repMaxContraint = pyomo.Constraint(model.canciones,rule=RepMax)

solvername='glpk'
solverpath_folder='.\\glpk\\w64' #does not need to be directly on c drive
solverpath_exe='.\\glpk\\w64\\glpsol' #does not need to be directly on c drive

instance = model.create_instance('dataModel1.dat')
opt=pyomo.SolverFactory(solvername,executable=solverpath_exe)
solver_results = opt.solve(instance)

instance.pprint()
print(solver_results)
instance.X.pprint()
