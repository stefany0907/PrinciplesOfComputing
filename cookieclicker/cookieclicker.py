"""
Cookie Clicker Simulator
"""

#import simpleplot
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    import SimpleGUICS2Pygame.simpleplot as simpleplot
import math
# Used to increase the timeout, if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0


# SIM_TIME = 3000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        self._tot_cookie = 0.0
        self._cur_cookie = 0.0
        self._cur_time = 0.0
        self._cur_cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]

    def __str__(self):
        """
        Return human readable state
        """
        # print type(self._history[0])
        return "Time:" + str(self._cur_time) + ", Current cookies:" + str(self._cur_cookie) + ", CPS:" + str(
            self._cur_cps) + ", Total Cookies:" + str(self._tot_cookie)

    def get_cookies(self):
        """
        Return current number of cookies
        (not total number of cookies)

        Should return a float
        """
        return self._cur_cookie

    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cur_cps

    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._cur_time

    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        history_clone = self._history
        return history_clone

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._cur_cookie >= cookies:
            return float(0.0)
        else:
            return float(math.ceil((cookies - self._cur_cookie) / self._cur_cps))

    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0:
            self._cur_time += time
            self._cur_cookie += self._cur_cps * time
            self._tot_cookie += self._cur_cps * time

    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._cur_cookie >= cost:
            self._cur_cookie -= cost
            self._cur_cps += additional_cps
            # self._tot_cookie += self._cur_cps * time
            self._history.append((self._cur_time, item_name, cost, self._tot_cookie))
            # print self._history


def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    _currentstate = ClickerState()
    build_info1 = build_info.clone()
    current_cookies = _currentstate.get_cookies()
    #    current_cps = _currentstate.get_cps()
    history = _currentstate.get_history()
    #    time_left = duration - _currentstate.get_time()
    current_time = _currentstate.get_time()

    while current_time <= duration:
        item = strategy(current_cookies, _currentstate.get_cps(), history, (duration - _currentstate.get_time()),
                        build_info1)
        #        print "item=", item
        if item == None:
            #            print "None"
            #            print _currentstate.get_cookies(), _currentstate.get_cps(), time_left, build_info1.get_cost("Cursor")
            break
        if current_cookies >= build_info1.get_cost(item):
            time_wait = 0
        else:
            time_wait = _currentstate.time_until(build_info1.get_cost(item))
        #            print "time_wait=", time_wait
        if current_time + time_wait <= duration:
            _currentstate.wait(time_wait)
            _currentstate.buy_item(item, build_info1.get_cost(item), build_info1.get_cps(item))
            build_info1.update_item(item)
            current_cookies = _currentstate.get_cookies()
            #            print "current_time=", current_time
            #            print "current_cps=", _currentstate.get_cps()
            current_time += time_wait
        else:
            break
        # print "current_time, duration", current_time, duration
    #        print

    _currentstate.wait(duration - current_time)
    #    print build_info1.build_items()
    #    for item in build_info1.build_items():
    #        print item, build_info1.get_cost(item)
    return _currentstate


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"


def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None


def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    cheapest_item = build_info.build_items()[0]
    cheapest_val = build_info.get_cost(build_info.build_items()[0])
    for item in build_info.build_items():
        if build_info.get_cost(item) < cheapest_val:
            cheapest_val = build_info.get_cost(item)
            cheapest_item = item
    if time_left >= 0:
        if cookies + time_left * cps >= cheapest_val:
            return cheapest_item
        else:
            return None


def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    afford_lst = []
    for item in build_info.build_items():
        if cookies + time_left * cps >= build_info.get_cost(item):
            afford_lst.append(item)
    if len(afford_lst) != 0:
        exp_item = afford_lst[0]
        exp_val = build_info.get_cost(afford_lst[0])
        for item in afford_lst:
            if build_info.get_cost(item) > exp_val:
                exp_item = item
                exp_val = build_info.get_cost(item)
    else:
        exp_item = None
    if time_left >= 0:
        return exp_item
    else:
        return None


def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    afford_lst = []
    for item in build_info.build_items():
        if cookies + time_left * cps >= build_info.get_cost(item):
            afford_lst.append(item)
    if len(afford_lst) != 0:
        max_cpsc = (build_info.get_cps(afford_lst[0]) / build_info.get_cost(afford_lst[0]))
        max_cpsc_item = afford_lst[0]
        for item in afford_lst:
            if (build_info.get_cps(item) / build_info.get_cost(item)) > max_cpsc:
                max_cpsc_item = item
                max_cpsc = (build_info.get_cps(item) / build_info.get_cost(item))
    else:
        max_cpsc_item = None
    if time_left >= 0:
        return max_cpsc_item
    else:
        return None


def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    #    if state.get_cookies() > 1.3e+10:
    #        state._tot_cookie *= 10
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    print history
    history = [(item[0], item[3]) for item in history]

    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)


def run():
    """
    Run the simulator.
    """
    # run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)


run()

# print simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 0.10000000000000001]}, 1.15), 5000.0, strategy_none)
# print simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 100.0000000000000001]}, 1.1), 500.0, strategy_cursor_broken)
# obj = ClickerState()
# obj.wait(45.0)
# obj.buy_item('item', 1.0, 3.5)
# print obj.time_until(49.0)
# obj = ClickerState()
# obj.wait(78.0)
# obj.buy_item('item', 1.0, 1.0)
# print obj.time_until(22.0)
# print len(provided.BuildInfo().build_items())
# print strategy_cheap(500000.0, 1.0, [(0.0, None, 0.0, 0.0)], 5.0, provided.BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15))
# print strategy_cheap(0.0, 1.0, [(0.0, None, 0.0, 0.0)], 5.0, provided.BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15))
# print strategy_expensive(0.0, 1.0, [(0.0, None, 0.0, 0.0)], 5.0, provided.BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15))
# print simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 0.10000000000000001], 'Portal': [1666666.0, 6666.0], 'Shipment': [40000.0, 100.0], 'Grandma': [100.0, 0.5], 'Farm': [500.0, 4.0], 'Time Machine': [123456789.0, 98765.0], 'Alchemy Lab': [200000.0, 400.0], 'Factory': [3000.0, 10.0], 'Antimatter Condenser': [3999999999.0, 999999.0], 'Mine': [10000.0, 40.0]}, 1.15), 10000000000.0, strategy_expensive)

# print simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 0.10000000000000001]}, 1.15), 5000.0, strategy_none)