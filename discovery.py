from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.dfg.exporter import exporter as dfg_exporter
import log_parser 
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.statistics.start_activities.log import get as start_activities
from pm4py.statistics.end_activities.log import get as end_activities


variant = xes_importer.Variants.ITERPARSE
parameters = {variant.value.Parameters.TIMESTAMP_SORT: True}
log = xes_importer.apply('Documents/TS Discovery/bpi_challenge_2013_incidents.xes', 
    variant=variant, parameters=parameters)
log = log_parser.parse(log, 3)
sa = start_activities.get_start_activities(log)
ea = end_activities.get_end_activities(log)


dfg = dfg_discovery.apply(log, variant=dfg_discovery.Variants.FREQUENCY)

for start in sa:
    for end in ea:
        dfg[end, start] += sa[start]

dfg_exporter.apply(dfg, 'Documents/TS Discovery/output.dfg', parameters={dfg_exporter.Variants.CLASSIC.value.Parameters.START_ACTIVITIES: sa,
                                   dfg_exporter.Variants.CLASSIC.value.Parameters.END_ACTIVITIES: ea})
