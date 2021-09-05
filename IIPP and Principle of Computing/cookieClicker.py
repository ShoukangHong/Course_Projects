"""
Cookie Clicker Simulator
It won't score 100, I think there are something broken in the code.
"""

import simpleplot
import math
# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(5)

import poc_clicker_provided as provided

# Constants
#SIM_TIME = 10000000000.0
SIM_TIME = 50000.0
class ClickerState:
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        self._sum_cook = 0.0
        self._current_cook = 0.0
        self._time = 0.0
        self._speed = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
    def __str__(self):
        """
        Return human readable state
        """
        return str([self.get_time(), 'speed' + str(self.get_cps()),
                    'current' + str(self.get_cookies()), 'sum' + str(self._sum_cook),
                   self._history[len(self._history) -1]])
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cook
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._speed
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies <= self._current_cook:
            return 0.0
        else:
            needed = cookies - self._current_cook
            return math.floor(needed / self._speed) + 1.0
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0:
            added = self._speed * time
            self._time += time
            self._sum_cook += added
            self._current_cook += added
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cook >= cost:
            self._current_cook -= cost
            self._speed += additional_cps
            self._history.append((self._time, item_name, cost, self._sum_cook))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    clicker = ClickerState()
    info = build_info.clone()
    while duration - clicker.get_time() > 0:
        rtime = duration - clicker.get_time()
        item = strategy(clicker.get_cookies(), 
               clicker.get_cps(), clicker.get_history(), 
               rtime, info)
        #print rtime, item, int(info.get_cost(item)), int(clicker.get_cookies()), int(clicker.get_cookies() + clicker.get_cookies() + rtime * clicker.get_cps())
        if item != None:
            cost = info.get_cost(item)
            time = min(clicker.time_until(cost), rtime)
            #print time, rtime, clicker.time_until(cost)
            clicker.wait(time)
            clicker.buy_item(item, cost, info.get_cps(item))
            info.update_item(item)
        else:
            clicker.wait(rtime)
    return clicker


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
    items = build_info.build_items()
    cheapest = None
    minval = build_info.get_cost(items[0])
    for item in items:
        cost = build_info.get_cost(item)
        #print cost, item
        if cost <= minval and cost <= cookies + time_left * cps:
            cheapest = item
            minval = cost
    return cheapest

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    items = build_info.build_items()
    maxval = 0
    most_exp = None
    rcookies = cookies + time_left * cps
    for item in items:
        cost = build_info.get_cost(item)
        if rcookies >= cost > maxval:
            most_exp = item
            maxval = build_info.get_cost(most_exp)
    #print most_exp, rcookies, build_info.get_cost(most_exp)
    return most_exp

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    items = build_info.build_items()
    items = sorted(items, key = lambda item:  (build_info.get_cps(item) / build_info.get_cost(item)),
                   reverse = True)
    #print items
    remove = []
    for item in items:
        if build_info.get_cost(item) / build_info.get_cps(item) > time_left:
            remove.append(item)
    for item in remove:
        items.remove(item)
    if len(items) <= 0:
        return None
    best = items[0]
    flag = False
    while flag == False:
        flag = True
        cost = build_info.get_cost(best)
        alltime = cost / cps
        #print best, cost, alltime
        ritems = [item for item in items if build_info.get_cost(item) < cost]
        #print ritems
        for item in ritems:
            rcps = build_info.get_cps(item)
            rtime = build_info.get_cost(item) / cps
            if rtime * cps + (cps + rcps) * (alltime - rtime) - build_info.get_cost(item) > cost:
                best = item
                flag = False
                break
    #print best
    return best
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    #history = state.get_history()
    #history = [(item[0], item[3]) for item in history]
    #simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    #run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    #run_strategy("Cheap", SIM_TIME, strategy_cheap)
    #run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
run()