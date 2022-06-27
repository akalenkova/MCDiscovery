from pm4py.objects.log.importer.xes import importer as xes_importer
import discovery, numpy, time, sys
numpy.warnings.filterwarnings('ignore', category=numpy.VisibleDeprecationWarning)                 

""""
This code compares the mean time for the semi-Markov process flow
dicovered from the log and the mean time for the same semi-Markov process flow 
when states' waiting times deviate from the mean value (mean + standard deviation).

Parameters:
- event log (xes file name)
- order k 
"""

sizes, accuracies, calc_times = [], [], []
variant = xes_importer.Variants.ITERPARSE
parameters = {variant.value.Parameters.TIMESTAMP_SORT: True}
log = xes_importer.apply(sys.argv[1], variant=variant, parameters=parameters)
number_of_chunks = len(log)
estimated_times = []
real_times = []
start_time = round(time.time()*1000)

# cut the log to get better precision
for traces in numpy.array_split(log, number_of_chunks):
    real_overall_time, dev_overall_time, size, accuracy, limiting_probabilities, means = discovery.calc_for_order_with_deviations(int(sys.argv[2]), traces)
    estimated_times.append(dev_overall_time)
    real_times.append(real_overall_time)
estimated_time = numpy.average(estimated_times)
real_time = numpy.average(real_times)
accuracy = 1 - (estimated_time - real_time) / real_time
calc_time = round(time.time()*1000) - start_time

print('----------------------------------')
print('calc time:')
print(calc_time)
print("accuracy:")
print(accuracy)
print("mean time:")
print(str(round(real_time//86400)) + 'd ' + str(round(real_time%86400//3600)) + 'h ' + str(round(real_time%3600//60)) + 'm ' + str(round(real_time%60)) + 's ')
print("deviated time:")
print(str(round(estimated_time//86400)) + 'd ' + str(round(estimated_time%86400//3600)) + 'h ' + str(round(estimated_time%3600//60)) + 'm ' + str(round(estimated_time%60)) + 's ')
