import dotenv

from services.simulator import Simulator


dotenv.load_dotenv('bot.env')


if __name__ == '__main__':
    simulator = Simulator()
    simulator.simulate()
    print('simulation success')
