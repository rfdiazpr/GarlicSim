from garlicsim.general_misc.infinity import Infinity
from garlicsim.general_misc import binary_search

import garlicsim.data_structures


class State(garlicsim.data_structures.State):
    
    def __init__(self):
        pass
    
    @staticmethod
    def history_step(history_browser):
        assert isinstance(
            history_browser,
            garlicsim.misc.base_history_browser.BaseHistoryBrowser
        )
        first_state = history_browser[0]
        last_state = history_browser[-1]
        assert last_state is history_browser.get_last_state()
        n_states = len(history_browser)
        # todo: If ever doing `BaseHistoryBrowser.__iter__`, should test it here
        # and compare to other methods.
        assert last_state is history_browser[n_states - 1]
        assert first_state is history_browser[-n_states]
        if n_states >= 2:
            second_state = history_browser[1]
            second_to_last_state = history_browser[-2]
            assert first_state.clock < second_state.clock <= \
                second_to_last_state.clock <= last_state.clock
            assert second_state is history_browser[- n_states + 1]
            assert second_to_last_state is history_browser[n_states - 2]
            
        assert history_browser.get_state_by_clock(-Infinity) is first_state
        assert history_browser.get_state_by_clock(Infinity) is last_state
        
        assert history_browser.get_state_by_clock(
            -Infinity,
            binary_search.roundings.BOTH
        ) == (None, first_state)
        assert history_browser.get_state_by_clock(
            Infinity,
            binary_search.roundings.BOTH
        ) == (last_state, None)
        
            
        
        return State()
        
    @staticmethod
    def create_root():
        return State()
    