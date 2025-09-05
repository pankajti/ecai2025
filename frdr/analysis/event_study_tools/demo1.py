from event_study_toolkit import eventstudy as es

ESTPERIOD = 50
GAP = 10
START = 0
END = 1
events = es.open_example_events() # built in method that contains dummy data
data = es.open_example_data() # ^^another one
groups = ['CCAR', 'GSIB']

esTutorial = es.eventstudy(ESTPERIOD, GAP, START, END, data, events, unique_id='subject_id', calType = 'NYSE', groups=groups)
print(esTutorial.runModel('market'))


print(esTutorial.runModel('ret_dlst_adj~mktrf_h15+smb+hml'))

print(esTutorial.getFullSampleTestStatistic('market'))