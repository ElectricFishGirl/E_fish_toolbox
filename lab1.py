import numpy as np
import matplotlib.pyplot as plt
current = np.linspace(0,65,14)
Power20 = [0,0.02, 0.24, 0.57, 0.85, 1.1, 1.38,1.68, 1.86, 2.18, 2.46, 2.75, 3.01, 3.3]
Power25 = [0,0.028, 0.303, 0.499, 0.852, 1.141, 1.430, 1.652, 1.92, 2.22, 2.47 , 2.71, 2.97, 3.24 ]
Power35 = [0,0.03, 0.31, 0.52, 0.84, 1.12, 1.37, 1.68, 1.92, 2.22, 2.49, 2.74, 3, 3.24 ]

plt.figure()
plt.plot(current, Power20, '*' , ls='-', c = 'k', label = 'T = 20')
plt.plot(current, Power25, '*' , ls='-', c = 'r', label = 'T = 25')
plt.plot(current, Power35, '*' , ls='-', c = 'b', label = 'T = 35')
plt.xlabel('Current in mA')
plt.ylabel('Power in micro W')
plt.title('Power vs current ')
plt.legend()

plt.figure()
plt.plot(current, Power35, '*' , ls='-', c = 'b')

plt.xlabel('Current in mA')
plt.ylabel('Power in micro W')
plt.title('Power vs current for T = 35 ')


plt.figure()
plt.plot(current, Power25, '*' , ls='-', c = 'r')
plt.xlabel('Current in mA')
plt.ylabel('Power in micro W]')
plt.title('Power vs current for T = 25')


plt.figure()
plt.plot(current, Power20, '*' , ls='-', c = 'k')
plt.xlabel('Current in mA')
plt.ylabel('Power in micro W]')
plt.title('Power vs current fot T = 20 ')
