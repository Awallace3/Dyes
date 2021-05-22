import os
import glob

#a = glob.glob('*/')
a = 'ES/'
#for i in a:
    #    try:
       # print(i)
os.chdir('ES/')
filename = open('ES.out','r')
num = 0
for n, i in enumerate(filename):
        if 'Normal termination' in i:
                print('Done')
                filename = open('ES.out','r')
                for n, i in enumerate(filename):
                        if ' Excitation energies and oscillator strengths:' in i:
                                num = n
filename2 = open('ES.out','r')
ans = filename2.readlines()
print(ans[num+2][51:58]) # nm wavelength
print(ans[num+2][61:70])
          #      os.chdir('../..')
      #  except FileNotFoundError:
      #          print(' ')
      #          print('ERRORRRR')
      #          print(' ')
      #          pass
'''
        try:
                os.chdir(str(i) +'/')
                print(i)
                filename = open('mex.out','r')
                editfile = []
                for i in filename:
                        if 'Normal termination' in i:
                                print('Done')
                                filename2 = open('mex.out','r')
                                for x in filename2:
                                        editfile.append(x)
                        elif 'Error termination' in i:
                                print('Error'+  str(i))
                                pass
'''
                                                                                                                                     

