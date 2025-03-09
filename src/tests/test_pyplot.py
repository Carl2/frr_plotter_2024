import unittest
import pandas as pd
import numpy as np
from col.plot.plot import (make_plot_handler,
                           filter_by)
from functools import reduce
from icecream import ic
from pdb import set_trace

class TestPyPlot(unittest.TestCase):
    data = {
        'x': [1, 2, 3, 4],
        'y': [10, 20, 25, 30]
    }
    df = pd.DataFrame(data)

    def test_filter_by(self):

        # create a filter function:
        # This will take a Pandas dataframe
        # match the field 'x' == ? and
        # output field 'y'
        filter_fn = filter_by(
            match_field='x',
            output_field='y'
        )
        # Now that we have the function we can use the
        # data field and match with 2.
        out_val = filter_fn(self.df, 2)
        self.assertEqual(out_val.iloc[0], 20)

        self.assertEqual(filter_fn(self.df, 3).iloc[0], 25)
        self.assertEqual(filter_fn(self.df, 4).iloc[0], 30)
        self.assertEqual(filter_fn(self.df, 1).iloc[0], 10)

        #lets do it the other way
        filter_fn= filter_by(match_field='y', output_field='x')
        self.assertEqual(filter_fn(self.df, 30).iloc[0], 4)
        self.assertEqual(filter_fn(self.df, 10).iloc[0], 1)
        self.assertEqual(filter_fn(self.df, 20).iloc[0], 2)
        self.assertEqual(filter_fn(self.df, 25).iloc[0], 3)

        # In case there is no match, the return is a empty
        # DataFrame
        out = filter_fn(self.df, 0)
        self.assertEqual(len(out), 0)


    def test_handler_fn(self):
        # To use this we need both a converter function
        # and a filter function.
        filter_fn = filter_by(
            match_field='x',
            output_field='y'
        )

        # converter , basically an id fn
        def converter(val: int):
            return val

        handler_fn = make_plot_handler(converter, filter_fn)
        # The values to fill in
        values = np.full(len(self.df['x']), np.nan)
        # out = handler_fn(
        #     {'data': self.df,
        #      'value': values,
        #      'index': 'x'
        #      }
        #     , self.df

        # )

        # ic(out)



    # def test_plot_handler(self):
    #     def converter(val: int):
    #         return val

    #     handler = make_plot_handler(converter, "y")
    #     values = np.full(len(self.df['x']), np.nan)
    #     set_trace()
    #     out = reduce(handler, self.data['x'], {
    #         "data": self.df,
    #         "value": values,
    #         "index": 1
    #     })
    #     ic(out)

    #     # Create a simple pandas DataFrame for the test
