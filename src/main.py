from simulation import Simulation
from scenario import Scenario

if __name__ == '__main__':

    scenario = Scenario()                         # Um cenário é criado, com todas as condições iniciais.
    world = scenario.create_world()               # Um mundo (cenário, mas a cada instante) é criado pelo cenário e todas as informações vão le ser passadas.

    simulation = Simulation(world)                # A simulação recebe o mundo. A forma mais simples de a simulação não daber de nada sobre o programa, só sabe que existe um mundo.

    world.print_state()

    simulation.start()

    simulation.step()

    world.print_state()
