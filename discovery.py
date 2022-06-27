from statistics import median
import log_parser, dfg_utils, stat_utils
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery

def calc_for_order_with_deviations(k,log):
    log = log_parser.prepare_log(log, k)
    log_activities=log_parser.log_activities(log)
    dfg = dfg_discovery.apply(log, variant=dfg_discovery.Variants.FREQUENCY)
    dfg["end", "start"] = 1
    limiting_probabilities = dfg_utils.calculate_limiting_probabilities(dfg, log_activities)
    times = log_parser.calculate_times(log) 
    means = stat_utils.calculate_means(dfg,times,log_activities)
    st_dev = stat_utils.calculate_standard_deviation_times(dfg,times,log_activities)
    deviated = {}
    for i in means:
        deviated[i] = means[i] + st_dev[i]
    real_overall_time = log_parser.calculate_real_overall_time(log) 
    dev_overall_time = 0
    for i in range(0, len(log_activities)):
        dev_overall_time += limiting_probabilities[log_activities[i]]*deviated[log_activities[i]]
    dev_overall_time /= limiting_probabilities['start']
    return real_overall_time, dev_overall_time, len(log_activities), 1, limiting_probabilities, means

    