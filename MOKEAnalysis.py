import csv
import matplotlib.pyplot as plt
import math

# Delta and conversion factor!!!
delta = 0.4
conv = 542

function = input('Do you want a plot of all the loops (l), a plot of coercivity (c), or a plot of remanence (r)? (l/c/r) ')

sloping = 'N'

# Putting all file paths in a list
filePaths=["/Users/vedantaryan/Downloads/test_data_38.xlsx - sheet1.csv",
"/Users/vedantaryan/Downloads/test_data_39.xlsx - sheet1.csv",
"/Users/vedantaryan/Downloads/test_data_40.xlsx - sheet1.csv",
"/Users/vedantaryan/Downloads/test_data_41.xlsx - sheet1.csv",
"/Users/vedantaryan/Downloads/test_data_42.xlsx - sheet1.csv",
"/Users/vedantaryan/Downloads/test_data_43_RAWDATA.xlsx - sheet1.csv",
"/Users/vedantaryan/Downloads/Test 44 Raw Data - Sheet1.csv",
"/Users/vedantaryan/Downloads/test_data_45 - Sheet1.csv",
"/Users/vedantaryan/Downloads/test_data_46.xlsx - sheet1.csv",
"/Users/vedantaryan/Downloads/test_data_47.xlsx - sheet1.csv",
"/Users/vedantaryan/Downloads/test_data_48.xlsx - sheet1.csv",
"/Users/vedantaryan/Downloads/test_data_49.xlsx - sheet1.csv",
"/Users/vedantaryan/Downloads/test_data_50.xlsx - sheet1.csv",
"/Users/vedantaryan/Downloads/test_data_51.xlsx - sheet1.csv",
"/Users/vedantaryan/Downloads/test_data_53.xlsx - sheet1.csv",
"/Users/vedantaryan/Downloads/test_data_54.xlsx - sheet1.csv",
"/Users/vedantaryan/Downloads/test_data_55.xlsx - sheet1.csv",
"/Users/vedantaryan/Downloads/test_data_57.xlsx - sheet1.csv"]

theta = [30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200]

H_correctedData = []
Phi_correctedData = []
coercivityData = []
remanenceData = []

for path in filePaths:
    # opening CSV file
    with open(path, 'r') as file:
        csvreader = csv.reader(file)
        # with open("/Users/vedantaryan/Downloads/test_data_53.xlsx - sheet1.csv", 'r') as file2:
        #         csvreader2 = csv.reader(file2)


                # Initializing empty arrays.
                # data=entire csv in one row.
                # h=x axis (external field)
                # i = y axis (some unit)

        data = []
        H = []
        H_corrected = []
        I = []
        phi = []
        phi_closed = []
        phi_corrected = []

        # turning csv file into a single list. removing first untitled element. replace #ev with third element
        for row in csvreader:
            data.append(row[0])
        data.remove('Untitled')
        data[1] = data[3]
        # print(data)

        # filtering huge list into sublists of h and i
        for i in range(len(data)):
            if i % 2 == 0:
                H.append(float(data[i]))
            else:
                I.append(float(data[i]))

        # print(H)
        # print(I)

        I_initial = sum(I) / len(I)

        # Converting h into real h????
        for h in H:
            hNew = h * conv
            H_corrected.append(hNew)

        # Converting current into kerr angle
        for i in I:
            phi_kerr = (i / I_initial - 1) * delta * math.pi / 180 / 2
            phi.append(phi_kerr)



        # print(phi)
        # Correcting noise/drift with linear drift cancellation
        run = 4 * max(H)
        rise = phi[len(phi) - 1] - phi[0]
        # Excel has -2 somehow
        slope = rise / run
        midpoint = H.index(max(H))

        # print(run)
        # print(rise)
        # print(slope)

        for i in range(len(phi)):
            if i <= midpoint:
                phiKerrClosed = phi[i] - (H[i] * slope + slope * run / 4)
                phi_closed.append(phiKerrClosed)
            else:
                phiKerrClosed = phi[i] - (H[i] * (-1) * slope + slope * run / 2)
                phi_closed.append(phiKerrClosed)
        # print(phi_closed)

        # Correcting correction for some reason
        centerClosed = sum(phi_closed) / len(phi_closed)
        # print(centerClosed)

        for phiClosed in phi_closed:
            phiNew = phiClosed - centerClosed
            phi_corrected.append(phiNew)

        # Finding coercivity
        for i in range(0, len(H) - 1):
            if (phi_corrected[i] < 0 and phi_corrected[i+1] > 0):
                corRHS = H_corrected[i]
            elif (phi_corrected[i] > 0 and phi_corrected[i+1] < 0):
                corLHS = H_corrected[i]
        coercivity = (abs(corRHS) + abs(corLHS)) / 2

        # print('Coercivity: ' + str(coercivity))

        #Finding remanence
        for i in range(0, len(H) - 1):
            if (H[i] == 0 and H[i+1] < 0):
                yIntercept = phi_corrected[i]
        remanence = 100 * (yIntercept / max(phi_corrected))
        # print('Remanence: ' + str(remanence) + '%')

        H_correctedData.append(H_corrected)
        Phi_correctedData.append(phi_corrected)
        coercivityData.append(coercivity)
        remanenceData.append(remanence)

# Printing Coercivity and Remanence
for i in range(len(coercivityData)):
    print('Theta: ' + str(theta[i]) + ' Coercivity: ' + str(round(coercivityData[i],2)) + ' Remanence ' + str(round(remanenceData[i],2)))

# Plotting each of the hysteresis loops
if function == 'l':
    for i in range(len(H_correctedData)):
        plt.plot(H_correctedData[i], Phi_correctedData[i], label=theta[i])

    plt.title("H vs Kerr Angle")
    plt.xlabel("H")
    plt.ylabel("Kerr Angle")
    plt.tight_layout()
    plt.legend()

    plt.axvline(x=0, c='black')
    plt.axhline(y=0, c='black')
    plt.show()

if function == 'c':
    plt.plot(theta, coercivityData, label='Coercivity')

    plt.title("Coercivity vs Theta")
    plt.xlabel("Theta")
    plt.ylabel("Coercivity")
    plt.tight_layout()
    plt.legend()

    plt.axvline(x=0, c='black')
    plt.axhline(y=0, c='black')
    plt.show()

# Plotting remanence vs theta
if function == 'r':
    plt.plot(theta, remanenceData, label='Remanence')

    plt.title("Remanence vs Theta")
    plt.xlabel("Theta")
    plt.ylabel("Remanence")
    plt.tight_layout()
    plt.legend()

    plt.axvline(x=0, c='black')
    plt.axhline(y=0, c='black')
    plt.show()
