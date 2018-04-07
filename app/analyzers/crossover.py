def analyze_crossover(self, historical_data, hot_thresh=None, cold_thresh=None,
                        period_count=(15, 21), all_data=False):
    """Performs an EMA crossover analysis on the historical data

    Args:
        historical_data (list): A matrix of historical OHCLV data.
        hot_thresh (float, optional): Defaults to None. The threshold at which this might be
            good to purchase.
        cold_thresh (float, optional): Defaults to None. The threshold at which this might be
            good to sell.
        period_count (tuple of (2) ints, optional): Defaults to (15, 21). Each number in the tuple
            contains the period count of an ema to be used in the crossover analysis
        all_data (bool, optional): Defaults to False. If True, we return the EMA associated
            with each data point in our historical dataset. Otherwise just return the last one.

    Returns:
        dict: A dictionary containing a tuple of indicator values and booleans for buy / sell
            indication.
    """

    dataframe = self.convert_to_dataframe(historical_data)
    ema_one_values = abstract.EMA(dataframe, period_count[0])
    ema_two_values = abstract.EMA(dataframe, period_count[1])
    combined_data = pandas.concat([dataframe, ema_one_values, ema_two_values], axis=1)
    combined_data.rename(columns={0: 'ema_value_one', 1: 'ema_value_two'}, inplace=True)

    rows = list(combined_data.iterrows())

    # List of 4-tuples containing: (old_ema_one, old_ema_two, current_ema_one, current_ema_two)

    analyzed_data = [
        (math.nan, math.nan, rows[1][1]['ema_value_one'], rows[1][1]['ema_value_two'])
    ]

    # We keep track of the old values as to assign a "hot" value when the first ema crosses over
    # the second one, and assign a "cold" value when the second ema crosses over the first

    for i in range(1, len(rows)):
        analyzed_data.append(
            (
                analyzed_data[i-1][2],
                analyzed_data[i-1][3],
                rows[i][1]['ema_value_one'],
                rows[i][1]['ema_value_two']
            )
        )

    return self.analyze_results(
        analyzed_data,
        is_hot=lambda o1, o2, c1, c2: o1 < o2 and c1 > c2 if hot_thresh else False,
        is_cold=lambda o1, o2, c1, c2: o1 > o2 and c1 < c2 if cold_thresh else False,
        all_data=all_data
    )


def analyze_crossover(self, historical_data, hot_thresh=None, cold_thresh=None,
                      period_count=(15, 21), all_data=False):
    """Performs a SMA crossover analysis on the historical data

    Args:
        historical_data (list): A matrix of historical OHCLV data.
        hot_thresh (float, optional): Defaults to None. The threshold at which this might be
            good to purchase.
        cold_thresh (float, optional): Defaults to None. The threshold at which this might be
            good to sell.
        period_count (tuple of (2) ints, optional): Defaults to (15, 21). Each number in the tuple
            contains the period count of an sma to be used in the crossover analysis
        all_data (bool, optional): Defaults to False. If True, we return the SMA associated
            with each data point in our historical dataset. Otherwise just return the last one.

    Returns:
        dict: A dictionary containing a tuple of indicator values and booleans for buy / sell
            indication.
    """

    dataframe = self.convert_to_dataframe(historical_data)
    sma_one_values = abstract.SMA(dataframe, period_count[0])
    sma_two_values = abstract.SMA(dataframe, period_count[1])
    combined_data = pandas.concat([dataframe, sma_one_values, sma_two_values], axis=1)
    combined_data.rename(columns={0: 'sma_value_one', 1: 'sma_value_two'}, inplace=True)

    rows = list(combined_data.iterrows())

    # List of 4-tuples containing: (old_sma_one, old_sma_two, current_sma_one, current_sma_two)

    analyzed_data = [
        (math.nan, math.nan, rows[1][1]['sma_value_one'], rows[1][1]['sma_value_two'])
    ]

    # We keep track of the old values as to assign a "hot" value when the first sma crosses over
    # the second one, and assign a "cold" value when the second sma crosses over the first

    for i in range(1, len(rows)):
        analyzed_data.append(
            (
                analyzed_data[i-1][2],
                analyzed_data[i-1][3],
                rows[i][1]['sma_value_one'],
                rows[i][1]['sma_value_two']
            )
        )

    return self.analyze_results(
        analyzed_data,
        is_hot=lambda o1, o2, c1, c2: o1 < o2 and c1 > c2 if hot_thresh else False,
        is_cold=lambda o1, o2, c1, c2: o1 > o2 and c1 < c2 if cold_thresh else False,
        all_data=all_data
    )
